FROM python:3.12

COPY app/ /app/

WORKDIR /app

RUN pip install -r requirements.txt

WORKDIR ..

CMD ["gunicorn", "app.application:app", "-c", "app/gunicorn_conf.py"]