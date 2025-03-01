FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y --no-install-recommends socat && \
    rm -rf /var/cache/apt/archives /var/lib/apt/lists

COPY chall /app/chall
COPY flag.txt /app/flag.txt

RUN chmod 644 /app/flag.txt && \
    chmod 755 /app/chall

WORKDIR /app

CMD socat -T30 -t30 tcp-l:1337,reuseaddr,fork EXEC:"./chall",stderr,su=nobody
