FROM python:3.9-slim

LABEL description="post_man image"

WORKDIR /usr/src/app

COPY . .

RUN apt-get update
RUN apt install postgresql postgresql-contrib
RUN pip install pipenv
RUN pipenv install

ENTRYPOINT ["pipenv", "run", "python", "./main.py"]