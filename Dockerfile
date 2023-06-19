FROM python:3.9-slim

LABEL description="post_man image"

WORKDIR /usr/src/app

COPY . .

# musl-dev is a "general" C compiler
RUN apt-get update && apt-get install -y libpq-dev gcc
RUN pip install pipenv
RUN pipenv install


ENTRYPOINT ["pipenv", "run", "python", "./main.py"]