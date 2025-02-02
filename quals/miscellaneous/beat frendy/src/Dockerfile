FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    wget \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN wget https://github.com/official-stockfish/Stockfish/releases/latest/download/stockfish-ubuntu-x86-64-avx2.tar -O /stockfish.tar \
    && tar -xvf /stockfish.tar -C / \
    && rm /stockfish.tar

WORKDIR /app

COPY chall.py .
COPY solver.py .

RUN pip install --no-cache-dir chess

EXPOSE 3000

CMD ["python", "-u", "chall.py"]
