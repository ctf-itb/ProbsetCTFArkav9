FROM debian:bookworm-slim
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y --no-install-recommends socat curl && \
    rm -rf /var/cache/apt/archives /var/lib/apt/lists

COPY chall /app/chall
COPY flag.txt /app/flag.txt
COPY run.sh /app/run.sh
COPY redpwnpow /app/redpwnpow

RUN chmod 644 /app/flag.txt && \
    chmod 755 /app/run.sh && \
    chmod 755 /app/redpwnpow


WORKDIR /app

RUN curl -kL https://gist.github.com/msfir/4a09f8a540277e9213e7e0882b5bf06a/raw/30a63c1c7a0354becf29c1e1fa34f6d92c280ef2/wasmtime.b64 | base64 -d > /bin/wasmtime && chmod +x /bin/wasmtime
RUN mkdir -p /nonexistent/.cache/wasmtime

CMD ["socat", "tcp-l:8010,reuseaddr,fork", "EXEC:./run.sh,stderr,su=nobody"]
