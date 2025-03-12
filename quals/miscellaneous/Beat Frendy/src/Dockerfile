FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    wget \
    socat \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN wget https://github.com/official-stockfish/Stockfish/releases/latest/download/stockfish-ubuntu-x86-64-avx2.tar -O /stockfish.tar \
    && tar -xvf /stockfish.tar -C / \
    && rm /stockfish.tar

WORKDIR /app

COPY chall.py .

RUN pip install --no-cache-dir chess

EXPOSE 1337

ENTRYPOINT ["socat", "TCP-LISTEN:1337,reuseaddr,fork,nodelay,su=nobody", "EXEC:'timeout 200 python3 chall.py'"]
