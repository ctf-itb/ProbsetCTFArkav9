FROM python:3.12.8-alpine

RUN apk add --no-cache libc6-compat socat

COPY chall /app/chall

RUN chmod 755 /app/chall

WORKDIR /app

CMD ["socat", "tcp-l:1337,reuseaddr,fork", "EXEC:./chall,stderr,pty"]
