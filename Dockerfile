FROM python:3.8-slim

WORKDIR /app

COPY app /app

COPY requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

CMD ["python", "app.py"]