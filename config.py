import os

# Base directory for markdown files
# Change this to the directory containing your markdown files
MARKDOWN_DIR = os.environ.get('MD_READER_DIR', os.path.join(os.path.dirname(__file__), 'docs'))

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
