FROM python:3

RUN mkdir /code
WORKDIR /code

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

COPY ./requirements.txt /code/requirements.txt

RUN pip install -r requirements.txt

COPY . /code/db/

CMD sleep 5 && uvicorn db.main:app --host 0.0.0.0 --port 80