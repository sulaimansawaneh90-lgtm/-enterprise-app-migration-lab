# ==========================================
# Stage 1: Dependency installation
# ==========================================
FROM python:3.12-slim AS builder

WORKDIR /build

ENV VIRTUAL_ENV=/opt/venv
ENV PATH="${VIRTUAL_ENV}/bin:${PATH}"

COPY requirements.txt .

RUN python -m venv "$VIRTUAL_ENV" \
    && pip install --no-cache-dir -r requirements.txt \
    && python -m pip uninstall -y pip


# ==========================================
# Stage 2: Runtime image
# ==========================================
FROM python:3.12-slim AS runtime

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="${VIRTUAL_ENV}/bin:${PATH}"

# Apply operating-system security updates
RUN apt-get update \
    && apt-get upgrade -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Copy dependencies from builder stage
COPY --from=builder /opt/venv /opt/venv

# Copy application code
COPY backend/ ./backend/

# Create dedicated non-root user
RUN groupadd --gid 10001 appuser \
    && useradd --uid 10001 --gid 10001 --create-home appuser \
    && chown -R appuser:appuser /app

USER 10001:10001

EXPOSE 5002

CMD ["gunicorn", "--bind", "0.0.0.0:5002", "backend.app:app"]
