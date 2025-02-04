FROM python:3.12.8-alpine

RUN apk add --no-cache openssh libc6-compat

RUN mkdir -p -m 0755 /var/run/sshd

RUN ssh-keygen -A

RUN adduser -D ctf

RUN passwd -u ctf

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
    echo "#!/bin/sh"; \
    echo "exec timeout 300 /app/chall"; \
} > /app/run.sh
RUN chmod +x /app/run.sh

EXPOSE 22

CMD ["/usr/sbin/sshd", "-D"]
