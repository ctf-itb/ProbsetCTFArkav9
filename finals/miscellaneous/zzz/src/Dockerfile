FROM ziglings/ziglang:0.12.0

COPY chall /app/chall
COPY flag.txt /app/flag.txt

RUN chmod 644 /app/flag.txt \
    && chmod 755 /app/chall

RUN wget --no-check-certificate -O /usr/bin/socat \
    https://github.com/andrew-d/static-binaries/raw/refs/heads/master/binaries/linux/x86_64/socat \
    && chmod +x /usr/bin/socat

WORKDIR /app

CMD ["socat", "TCP-LISTEN:1337,reuseaddr,fork", "EXEC:/app/chall,stderr,pty,echo=0"]
