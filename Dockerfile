FROM python:latest

RUN pip install tk Pillow

WORKDIR /usr/src/app

COPY . .

CMD [ "sh" ]
