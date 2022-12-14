FROM python:3.6-slim-stretch

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN apt-get update --fix-missing && apt-get install -y build-essential && apt-get install -y procps && apt install -y curl
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . .

CMD python3 manage.py migrate --settings django_study.dev \
    && uwsgi -w django_study.wsgi -s :8000 --env DJANGO_SETTINGS_MODULE=django_study.dev --processes=4
