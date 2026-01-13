FROM python:3.12-slim

COPY requirements.txt .
RUN pip install -r requirements.txt

RUN mkdir -p data

COPY historical/extract.py .
COPY historical/transform.py .
COPY /historical/create_parquet.py .
COPY historical/upload_to_s3.py .
COPY historical/pipeline.py .

CMD ["python3.12", "pipeline.py"]