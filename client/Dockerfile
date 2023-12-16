FROM python:3.10-slim

WORKDIR /test

COPY requirements.txt .

RUN pip install  -r requirements.txt

COPY . /test

CMD ["python3", "client_service.py"]

