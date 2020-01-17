

FROM python:3.7-stretch
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV SONARR_URL http://192.168.1.1:8989/
ENV SONARR_APIKEY 1283324727347

RUN mkdir /code
WORKDIR /code
COPY requirements.txt .
RUN pip3 install wheel --no-cache-dir -r requirements.txt

EXPOSE 8000
COPY . /code/
WORKDIR /code/src

RUN python3 manage.py migrate
RUN python3 manage.py loaddata settings.json
RUN python3 manage.py run_huey & python3 manage.py runserver && fg