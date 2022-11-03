FROM python:3.7-slim

RUN mkdir /app

WORKDIR /app

COPY . .

RUN pip3 install -r requirements.txt --no-cache-dir

CMD ["gunicorn", "api_yamdb.wsgi:application", "--bind", "8000:8000" ]