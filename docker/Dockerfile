# ---------- Stage 1: build the React frontend ----------
FROM node:20-alpine AS frontend-build

WORKDIR /build
COPY frontend/package.json frontend/package-lock.json* ./
RUN npm ci --production=false 2>/dev/null || npm install
COPY frontend/ .
RUN npm run build

# ---------- Stage 2: Python API + static assets ----------
FROM python:3.14-slim

LABEL maintainer="EDGE"

RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .
COPY --from=frontend-build /build/build /app/static

RUN mkdir -p /tmp/migrations && chown appuser:appuser /tmp/migrations

USER appuser

ENV FLASK_ENV=production
ENV MIGRATION_STATE_DIR=/tmp/migrations
ENV LOG_LEVEL=INFO

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/healthz')" || exit 1

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120", "app:create_app()"]
