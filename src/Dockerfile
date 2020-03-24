FROM python:3.7-stretch
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/
RUN chmod +x /code/start.sh
ENTRYPOINT ["/bin/bash", "/code/start.sh"]