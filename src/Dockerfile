FROM python:3.11.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

RUN apt-get -y update
RUN apt-get -y install curl

COPY . ./

EXPOSE 4000

CMD python main.py