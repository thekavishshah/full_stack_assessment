FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt && \
    python -m spacy download en_core_web_sm

COPY . .
EXPOSE 8000
CMD ["uvicorn", "nlp_server:app", "--host", "0.0.0.0", "--port", "8000"]