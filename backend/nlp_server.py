from fastapi import FastAPI, Query as FQuery
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import spacy
from spacy.matcher import Matcher
from spacy.pipeline import EntityRuler

# ---------------------------------------------------------------------------
# 1.  NLP pipeline setup (unchanged, but moved into its own function)
# ---------------------------------------------------------------------------

def setup_nlp():
    nlp = spacy.load("en_core_web_sm")

    # Custom entities for common conditions
    ruler = EntityRuler(nlp, overwrite_ents=True)
    ruler.add_patterns([
        {"label": "COND", "pattern": "diabetic"},
        {"label": "COND", "pattern": "hypertensive"},
        {"label": "COND", "pattern": "asthmatic"},
        {"label": "COND", "pattern": "pregnant"},
        {"label": "COND", "pattern": "smoker"},
    ])
    nlp.add_pipe(ruler, before="ner")

    matcher = Matcher(nlp.vocab)
    matcher.add("AGE_OVER", [[{"LOWER": {"IN": ["over", "above"]}}, {"LIKE_NUM": True}]])
    matcher.add("AGE_UNDER", [[{"LOWER": {"IN": ["under", "below"]}}, {"LIKE_NUM": True}]])

    return nlp, matcher

# ---------------------------------------------------------------------------
# 2.  Parsing helpers
# ---------------------------------------------------------------------------

nlp, matcher = setup_nlp()

class Query(BaseModel):
    text: str

conditions_ref = ["diabetic", "hypertensive", "asthmatic", "pregnant", "smoker"]


def parse_query(text: str):
    doc = nlp(text)
    filters = {"age": {}, "condition": None}

    # entity scan
    for ent in doc.ents:
        if ent.label_ == "COND":
            filters["condition"] = ent.text.lower()

    # pattern‑based age scan
    matches = matcher(doc)
    for match_id, start, end in matches:
        label = nlp.vocab.strings[match_id]
        num = int(doc[end - 1].text)
        if label == "AGE_OVER":
            filters["age"]["gt"] = num
        else:
            filters["age"]["lt"] = num

    return filters


def map_to_fhir(filters):
    """Turn our tiny filter structure into a FHIR‑ish search JSON."""

    bundle = {
        "resourceType": "Bundle",
        "type": "searchset",
        "total": 1,
        "entry": [
            {
                "resource": {
                    "resourceType": "Patient",
                    "name": [{"text": "Simulated Patient"}],
                    "age": filters.get("age"),
                    "condition.code:text": filters.get("condition"),
                }
            }
        ],
    }
    return bundle

# ---------------------------------------------------------------------------
# 3.  FastAPI app
# ---------------------------------------------------------------------------

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/query")
async def query_fhir(q: Query):
    filters = parse_query(q.text)
    return map_to_fhir(filters)["entry"]  # just send array to the UI

@app.get("/autocomplete")
async def autocomplete(prefix: str = FQuery(..., min_length=1)):
    p = prefix.lower()
    return [c for c in conditions_ref if c.startswith(p)]

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("nlp_server:app", host="0.0.0.0", port=8000, reload=True)