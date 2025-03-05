FROM python:3.13-alpine3.20

RUN apk update && apk add socat && adduser -D -h /home/chall -s /bin/bash chall
COPY app.py /home/chall/app.py
USER chall
#ENTRYPOINT ["socat", "TCP-LISTEN:1337,reuseaddr,fork", "EXEC:\"python /home/chall/app.py\""]