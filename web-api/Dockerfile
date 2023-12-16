FROM python:3.10-slim

WORKDIR /test

COPY requirements.txt .

RUN pip install  -r requirements.txt

COPY . /test


CMD ["uvicorn", "web_service:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]