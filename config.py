import os

# Base directory for markdown files
# Change this to the directory containing your markdown files
MARKDOWN_DIR = os.environ.get('MD_READER_DIR', os.path.join(os.path.dirname(__file__), 'docs'))

# Multi-root markdown directories (optional).
# Example: MD_READER_DIRS=/data/md/team-a,/data/md/team-b
# Priority:
#   1) MD_READER_DIRS (comma/semicolon separated)
#   2) MD_READER_DIR
_markdown_dirs_raw = os.environ.get('MD_READER_DIRS', '').strip()
if _markdown_dirs_raw:
    _normalized = _markdown_dirs_raw.replace(';', ',').replace('\n', ',')
    MARKDOWN_DIRS = [p.strip() for p in _normalized.split(',') if p.strip()]
else:
    MARKDOWN_DIRS = [MARKDOWN_DIR]

# Secret key for session management
SECRET_KEY = os.environ.get('MD_READER_SECRET', 'change-this-to-a-random-secret-key')

# Users configuration: username -> password hash
# Passwords are stored as werkzeug security hashes
# Default user: admin / admin123
USERS = {
    'admin': 'pbkdf2:sha256:600000$default$e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
}

# Server settings
HOST = '0.0.0.0'
PORT = int(os.environ.get('MD_READER_PORT', 5000))
DEBUG = os.environ.get('MD_READER_DEBUG', 'true').lower() == 'true'
