FROM python:3.12.8-slim
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y --no-install-recommends socat && \
    rm -rf /var/cache/apt/archives /var/lib/apt/lists

COPY chall /app/chall

RUN chmod 755 /app/chall

WORKDIR /app

CMD ["socat", "tcp-l:1337,reuseaddr,fork", "EXEC:./chall,stderr,pty"]
