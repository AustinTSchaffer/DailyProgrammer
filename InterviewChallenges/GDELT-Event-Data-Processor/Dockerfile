FROM python:3-slim

EXPOSE 5000

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

ENV FLASK_APP=app.py

COPY config.ini .
COPY app.py .
COPY gdelt_data_processor gdelt_data_processor
COPY templates templates

CMD [ "python", "-m", "flask", "run", "--host=0.0.0.0", "--port=5000" ]
