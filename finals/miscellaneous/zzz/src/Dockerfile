FROM ziglings/ziglang:0.12.0

COPY chall /app/chall
COPY flag.txt /app/flag.txt
COPY socat /usr/bin/socat

RUN chmod 644 /app/flag.txt \
    && chmod 755 /app/chall

RUN chmod +x /usr/bin/socat

WORKDIR /app

CMD ["socat", "TCP-LISTEN:1337,reuseaddr,fork", "EXEC:/app/chall,stderr,pty,echo=0"]
