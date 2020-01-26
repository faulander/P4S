FROM python:3.7.6-alpine

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk --no-cache add build-base
RUN apk --no-cache add postgresql-dev
RUN python3 -m pip install psycopg2

# set working directory
WORKDIR /usr/src/app


# add and install requirements
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

# add entrypoint.sh
COPY ./entrypoint.sh /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

# switch to non-root user
USER user

# add app
COPY . /usr/src/app


# run server
ENTRYPOINT ["usr/src/app/entrypoint.sh"]