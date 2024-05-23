FROM python:3.11

WORKDIR /app

ENV worker_count=8
ENV port=8000
ENV timeout=60

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install uvicorn

COPY . .
