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
