FROM python:3.11-slim

RUN apt-get update && apt-get install -y socat

RUN adduser --uid 1001 --shell /bin/bash --disabled-password --gecos "" ctf

RUN mkdir /home/ctf/chall

COPY ./requirements.txt /home/ctf/chall/requirements.txt
RUN pip install -r /home/ctf/chall/requirements.txt

COPY ./chall.py /home/ctf/chall/chall.py
COPY ./param.py /home/ctf/chall/param.py
COPY ./Variety1.py /home/ctf/chall/Variety1.py
COPY ./Variety2.py /home/ctf/chall/Variety2.py
COPY ./flag.txt /home/ctf/chall/flag.txt
COPY ./run.sh /home/ctf/chall/run.sh
RUN chmod +x /home/ctf/chall/run.sh

USER ctf
WORKDIR /home/ctf/chall

CMD ["./run.sh"]