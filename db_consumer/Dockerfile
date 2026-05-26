FROM python:3.12-slim

WORKDIR /app

# Copy service code
COPY db_consumer/ ./

# Copy shared models
COPY models/ ./models

# Copy pyproject (needed before install)
COPY db_consumer/pyproject.toml .

# Set Python path BEFORE install (safer for build-time imports)
ENV PYTHONPATH=/app

# Install dependencies
RUN pip install --no-cache-dir .

# Entrypoint
RUN chmod +x entrypoint.sh

CMD ["./entrypoint.sh"]