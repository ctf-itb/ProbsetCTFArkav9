FROM python:3.12-slim

COPY src/requirements.txt /tmp/requirements.txt

RUN pip install --no-cache-dir -r /tmp/requirements.txt \
  && rm /tmp/requirements.txt

RUN addgroup --system app \
  && adduser \
  --disabled-password \
  --gecos "" \
  --home "/app" \
  --ingroup "app" \
  --uid 1337 "app"

COPY src /app

RUN chown -R root:root /app \
  && chmod 0755 /app \
  && chmod -R 0644 /app/* \
  && chmod 0755 /app/templates

WORKDIR /app

USER app

ENTRYPOINT ["python3", "app.py"]
