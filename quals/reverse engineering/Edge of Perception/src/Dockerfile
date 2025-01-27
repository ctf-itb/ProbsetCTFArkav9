FROM python:3.12.8-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    openssh-server \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p -m0755 /var/run/sshd

RUN useradd -r ctf
RUN passwd -d ctf


RUN { \
    echo "Match User ctf"; \
    echo "    ForceCommand /app/run.sh"; \
    echo "    PasswordAuthentication yes"; \
    echo "    AllowTcpForwarding no"; \
} >> /etc/ssh/sshd_config

RUN { \
    echo "PermitRootLogin no"; \
    echo "PubkeyAuthentication no"; \
    echo "PasswordAuthentication yes"; \
    echo "PermitEmptyPasswords yes"; \
} >> /etc/ssh/sshd_config


COPY chall /app/chall
RUN chmod +x /app/chall

RUN { \
    echo "#!/bin/bash"; \
    echo "exec timeout --foreground 300 /app/chall"; \
} > /app/run.sh
RUN chmod +x /app/run.sh

EXPOSE 22

CMD ["/usr/sbin/sshd", "-D"]
