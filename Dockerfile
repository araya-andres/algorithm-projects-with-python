FROM python:3.11.4-bullseye AS base
WORKDIR /usr/src/algorithms
ENV PYTHONPATH=/usr/src/algorithms
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

FROM base AS dev
RUN apt update -y && \
    apt install less tig vim -y
RUN git config --global core.editor vim && \
    git config --global core.hooksPath .githooks
RUN mkdir /root/.ssh
RUN pip install -r requirements.dev.txt
CMD [ "sh" ]

FROM base AS prod
CMD [ "sh" ]
