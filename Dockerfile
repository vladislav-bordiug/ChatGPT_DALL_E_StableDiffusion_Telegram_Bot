FROM python:3.12

COPY app/ /app/

WORKDIR /app

RUN pip install -r requirements.txt

WORKDIR ..

CMD ["python", "-c", "from app.application import run; run()"]