FROM python:3.10-slim

WORKDIR app/
RUN apt-get update \
    && apt-get -y install libpq-dev gcc
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN apt-get autoremove -y gcc
COPY . .
CMD python manage.py runserver 0.0.0.0:8000