FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        curl \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Instalar uv (gestor de dependencias) y dejarlo en PATH
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:/root/.cargo/bin:${PATH}"

# Usuario no root
RUN useradd --create-home --home /home/appuser --shell /bin/bash appuser

# Instalar dependencias con uv (sin base de datos ni redis)
COPY pyproject.toml ./
RUN uv pip install --system --no-cache flask==3.0.2 gunicorn==21.2.0

COPY . .

RUN chown -R appuser:appuser /app
USER appuser

ENV FLASK_APP=app.py
EXPOSE 5000
HEALTHCHECK --interval=30s --timeout=5s --retries=3 CMD python -c "import socket; s=socket.socket(); s.connect(('127.0.0.1',5000)); s.close()"

CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
