FROM python:3.12-alpine3.20

RUN apk update && apk add socat && adduser -D -h /home/chall -s /bin/bash chall
COPY app.py /home/chall/app.py
USER chall