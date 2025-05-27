# Full-Stack Engineer – AI on FHIR

## Setup & Run

### Backend
```bash
cd backend
pip install -r requirements.txt
python -m spacy download en_core_web_sm
uvicorn nlp_server:app --reload

# AI on FHIR – Full‑Stack Assessment (Run Guide)

### Quick start with Docker Compose
```bash
# from repo root
cp .env.example .env        # optional – tweak ports or API URL here
docker compose up --build   # brings up http://localhost:3000 (UI) + :8000 (API)


Example: "Show me all diabetic patients over 50"
→ Returns simulated FHIR bundle with condition: diabetic and age.gt: 50
```

### Notes

**Focus Areas:**
- Prioritized clean separation of backend NLP processing and frontend UI.
- Used `spaCy` for fast development of entity and pattern-based intent recognition.
- Ensured Docker compatibility for reproducible environment and easy setup.

**Improvements with More Time:**
- Expand NLP to handle more diverse query formats (e.g., negation, synonyms).
- Add filters and sorting on the frontend (e.g., by age range, condition severity).
- Integrate with a real FHIR server (currently uses simulated output).
- Add unit tests for NLP parsing and API routes.
- Improve accessibility and add i18n (multi-language support).
