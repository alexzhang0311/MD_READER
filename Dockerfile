FROM python:3.12-slim

WORKDIR /app

# Install dependencies first (cache layer)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copy application code
COPY app.py config.py gunicorn.conf.py ./
COPY templates/ templates/

# Create default docs directory
RUN mkdir -p /data/markdown

# Default environment
ENV MD_READER_DEBUG=false \
    MD_READER_DIR=/data/markdown \
    MD_READER_PORT=5000 \
    MD_READER_SECRET=change-me-in-production

EXPOSE 5000

# Run with Gunicorn (production WSGI server)
CMD ["gunicorn", "-c", "gunicorn.conf.py", "app:app"]
