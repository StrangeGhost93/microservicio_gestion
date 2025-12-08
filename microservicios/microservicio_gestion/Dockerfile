FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
	PIP_NO_CACHE_DIR=1

WORKDIR /app

# System deps needed for psycopg2 / gunicorn and health checks
RUN apt-get update \ 
	&& apt-get install -y --no-install-recommends \ 
		build-essential \ 
		libpq-dev \ 
		netcat-traditional \ 
	&& rm -rf /var/lib/apt/lists/*

# Non-root user
RUN useradd --create-home --home /home/appuser --shell /bin/bash appuser

COPY requirements.txt ./
RUN pip install --upgrade pip \ 
	&& pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chown -R appuser:appuser /app
USER appuser

ENV FLASK_APP=app.py
EXPOSE 5000
HEALTHCHECK --interval=30s --timeout=5s --retries=3 CMD python -c "import socket; s=socket.socket(); s.connect(('127.0.0.1',5000)); s.close()"

CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
