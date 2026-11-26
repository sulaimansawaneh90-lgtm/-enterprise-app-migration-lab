FROM python:3.12-slim


WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Apply operating-system security updates
RUN apt-get update \
    && apt-get upgrade -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY authentication/ ./authentication/

# Create a dedicated non-root user with fixed UID/GID
RUN groupadd --gid 10001 appuser \
    && useradd --uid 10001 --gid 10001 --create-home appuser \
    && chown -R appuser:appuser /app

USER 10001:10001

EXPOSE 5001

CMD ["gunicorn", "--bind", "0.0.0.0:5001", "authentication.app:app"]
