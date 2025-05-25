# Full-Stack Engineer – AI on FHIR

## Setup & Run

### Backend
```bash
cd backend
pip install -r requirements.txt
python -m spacy download en_core_web_sm
uvicorn nlp_server:app --reload