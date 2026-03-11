import multiprocessing
import os

# Gunicorn production config
# Usage: gunicorn -c gunicorn.conf.py app:app

bind = f"0.0.0.0:{os.environ.get('MD_READER_PORT', '5000')}"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "gthread"
threads = 2
timeout = 120
keepalive = 5

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"

# Security
limit_request_line = 8190
limit_request_fields = 100
