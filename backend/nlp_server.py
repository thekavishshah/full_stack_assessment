from fastapi import FastAPI
from pydantic import BaseModel
import spacy
from spacy.matcher import Matcher
from spacy.pipeline import EntityRuler

# 1. Setup NLP pipeline

def setup_nlp():
    nlp = spacy.load("en_core_web_sm")
    # Entity ruler for medical conditions
    ruler = EntityRuler(nlp, overwrite_ents=True)
    condition_patterns = [
        {"label": "COND", "pattern": "diabetic"},
        {"label": "COND", "pattern": "hypertensive"},
        {"label": "COND", "pattern": "asthmatic"},
        # …add more patterns here
    ]
    ruler.add_patterns(condition_patterns)
    nlp.add_pipe(ruler, before="ner")

    # Matcher for age filters
    matcher = Matcher(nlp.vocab)
    matcher.add(
        "AGE_OVER",
        [[{"LOWER": {"IN": ["over", "above"]}}, {"LIKE_NUM": True}]],
    )
    matcher.add(
        "AGE_UNDER",
        [[{"LOWER": {"IN": ["under", "below"]}}, {"LIKE_NUM": True}]],
    )
    return nlp, matcher

# 2. Parsing and mapping functions

class Query(BaseModel):
    text: str

nlp, matcher = setup_nlp()


def parse_query(text: str):
    doc = nlp(text)
    filters = {}
    # Extract condition
    for ent in doc.ents:
        if ent.label_ == "COND":
            filters["condition"] = ent.text
    # Extract age filters
    for match_id, start, end in matcher(doc):
        label = nlp.vocab.strings[match_id]
        span = doc[start:end]
        num = next((int(tok.text) for tok in span if tok.like_num), None)
        if num is not None:
            if label == "AGE_OVER":
                filters["age"] = {"gt": num}
            else:
                filters["age"] = {"lt": num}
    return filters


def map_to_fhir(filters: dict):
    q = {"resourceType": "Patient"}
    if filters.get("condition"):
        q["condition.code:text"] = filters["condition"]
    if filters.get("age"):
        q["age"] = filters["age"]
    return q

# 3. FastAPI app

app = FastAPI()

@app.post("/query")
async def query_fhir(q: Query):
    filters = parse_query(q.text)
    return map_to_fhir(filters)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("nlp_server:app", host="0.0.0.0", port=8000, reload=True)