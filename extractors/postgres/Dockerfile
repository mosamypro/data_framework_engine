FROM python:3.9-slim
RUN pip install psycopg2-binary requests
COPY postgres_extractor.py /app/postgres_extractor.py
WORKDIR /app
CMD ["python", "postgres_extractor.py"]
