FROM python:3.13.2-slim

RUN apt-get update && apt-get install -y socat

RUN adduser -uid 1001 --shell /bin/bash --disabled-password --gecos "" ctf

COPY ./requirements.txt /home/ctf/requirements.txt
RUN pip install -r /home/ctf/requirements.txt

COPY ./chall.py /home/ctf/chall.py
COPY ./run.sh /home/ctf/run.sh

RUN chmod +x /home/ctf/run.sh

USER ctf
WORKDIR /home/ctf

CMD ["./run.sh"]