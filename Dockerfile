FROM ubuntu:14.04.1

RUN apt-get update && apt-get install -yq python-dev python-pip libpq-dev libmysqlclient-dev

ADD . /code
WORKDIR /code

RUN pip install -q -r requirements.txt

EXPOSE 5000

CMD python wsgi.py
