import multiprocessing
import os

# Gunicorn production config
# Usage:
#   foreground: gunicorn -c gunicorn.conf.py app:app
#   daemon:     gunicorn -c gunicorn.conf.py app:app --daemon

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_DIR, 'log')
os.makedirs(LOG_DIR, exist_ok=True)

bind = f"0.0.0.0:{os.environ.get('MD_READER_PORT', '5000')}"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "gthread"
threads = 2
timeout = 120
keepalive = 5

# Logging — output to log/ directory
accesslog = os.path.join(LOG_DIR, 'access.log')
errorlog = os.path.join(LOG_DIR, 'error.log')
loglevel = "info"

# Daemon mode PID file
pidfile = os.path.join(LOG_DIR, 'gunicorn.pid')

# Security
limit_request_line = 8190
limit_request_fields = 100
