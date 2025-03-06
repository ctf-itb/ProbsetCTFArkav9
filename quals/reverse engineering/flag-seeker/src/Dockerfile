FROM python:3.12.8-alpine

RUN apk add --no-cache openssh libc6-compat

RUN mkdir -p -m 0755 /var/run/sshd && ssh-keygen -A

RUN adduser -D "4TAdcJskoyJ9ZVYlYDr5cCsY3ueyNljDAaCxl0slmARpclxRPNle6EG1GUAjsnl9Siy0ktk" && echo "4TAdcJskoyJ9ZVYlYDr5cCsY3ueyNljDAaCxl0slmARpclxRPNle6EG1GUAjsnl9Siy0ktk:8niRFzMctZvc9okrQ0cUFecn0bXM6" | chpasswd

RUN { \
    echo "Match User 4TAdcJskoyJ9ZVYlYDr5cCsY3ueyNljDAaCxl0slmARpclxRPNle6EG1GUAjsnl9Siy0ktk"; \
    echo "    ForceCommand /app/run.sh"; \
    echo "    PasswordAuthentication yes"; \
    echo "    AllowTcpForwarding no"; \
} >> /etc/ssh/sshd_config

RUN { \
    echo "PermitRootLogin no"; \
    echo "PubkeyAuthentication no"; \
    echo "PasswordAuthentication yes"; \
    echo "PermitEmptyPasswords no"; \
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
