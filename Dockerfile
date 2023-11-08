# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /server

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
RUN python3 create_database.py

#RUN python3 api.py
ENV FLASK_APP=api.py
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
