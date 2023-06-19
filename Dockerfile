FROM python:3.9-slim

LABEL description="post_man image"

WORKDIR /usr/src/app

COPY . .

RUN apt-get update
RUN apt install postgresql11-server
RUN pip install pipenv
RUN pipenv install
RUN PATH=$PATH:/usr/pgsql-11/bin/

ENTRYPOINT ["pipenv", "run", "python", "./main.py"]