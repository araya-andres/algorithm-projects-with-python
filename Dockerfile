FROM python:latest

RUN pip install tk

WORKDIR /usr/src/app

COPY . .

CMD [ "sh" ]
