import os
import markdown
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, abort
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from pygments.formatters import HtmlFormatter

import config

app = Flask(__name__)
app.secret_key = config.SECRET_KEY

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = '请先登录'
login_manager.login_message_category = 'warning'

# -------------------------------------------------------------------
# User model
# -------------------------------------------------------------------
class User(UserMixin):
    def __init__(self, username):
        self.id = username
        self.username = username


# In-memory user store – initialised from config on first run, but
# the /register endpoint can add users at runtime.
_users: dict[str, str] = {}          # username -> password_hash


def _ensure_users_loaded():
    """Lazy-load default users from config (only once)."""
    if not _users:
        # Always create the default admin with a *usable* hash
        _users['admin'] = generate_password_hash('Webank@123')
        # Merge any extra entries from config
        for uname, phash in config.USERS.items():
            if uname not in _users:
                _users[uname] = phash


@login_manager.user_loader
def load_user(username):
    _ensure_users_loaded()
    if username in _users:
        return User(username)
    return None


# -------------------------------------------------------------------
# Auth routes
# -------------------------------------------------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        _ensure_users_loaded()

        if username in _users and check_password_hash(_users[username], password):
            user = User(username)
            login_user(user, remember=True)
            next_page = request.args.get('next')
            flash('登录成功！', 'success')
            return redirect(next_page or url_for('index'))
        else:
            flash('用户名或密码错误', 'danger')

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        confirm  = request.form.get('confirm', '')

        _ensure_users_loaded()

        if not username or not password:
            flash('用户名和密码不能为空', 'danger')
        elif len(password) < 6:
            flash('密码长度至少6位', 'danger')
        elif password != confirm:
            flash('两次密码输入不一致', 'danger')
        elif username in _users:
            flash('用户名已存在', 'danger')
        else:
            _users[username] = generate_password_hash(password)
            flash('注册成功，请登录', 'success')
            return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('已退出登录', 'info')
    return redirect(url_for('login'))


# -------------------------------------------------------------------
# Helpers
# -------------------------------------------------------------------
def get_markdown_roots() -> dict[str, str]:
    """Return stable root-name -> absolute directory mapping."""
    roots: dict[str, str] = {}
    for idx, directory in enumerate(config.MARKDOWN_DIRS, start=1):
        real_dir = os.path.realpath(directory)
        base_name = os.path.basename(os.path.normpath(real_dir)) or f'root{idx}'
        name = base_name
        suffix = 2
        while name in roots:
            name = f'{base_name}-{suffix}'
            suffix += 1
        roots[name] = real_dir
    return roots


def get_safe_path(base_dir: str, rel_path: str) -> str | None:
    """Resolve *rel_path* under *base_dir* and reject path traversal."""
    base = os.path.realpath(base_dir)
    full = os.path.realpath(os.path.join(base, rel_path))
    if full != base and not full.startswith(base + os.sep):
        return None
    return full


def list_markdown_tree(directory: str, rel: str = '') -> list[dict]:
    """Return a nested list of markdown files and directories."""
    items = []
    try:
        entries = sorted(os.listdir(directory), key=lambda x: (not os.path.isdir(os.path.join(directory, x)), x.lower()))
    except OSError:
        return items

    for entry in entries:
        full = os.path.join(directory, entry)
        entry_rel = os.path.join(rel, entry).replace('\\', '/')

        if os.path.isdir(full):
            children = list_markdown_tree(full, entry_rel)
            if children:  # only show dirs that contain .md files
                items.append({
                    'name': entry,
                    'type': 'directory',
                    'path': entry_rel,
                    'children': children,
                })
        elif entry.lower().endswith('.md'):
            items.append({
                'name': entry,
                'type': 'file',
                'path': entry_rel,
            })
    return items


# -------------------------------------------------------------------
# Page routes
# -------------------------------------------------------------------
@app.route('/')
@login_required
def index():
    return render_template('index.html')


# -------------------------------------------------------------------
# API routes
# -------------------------------------------------------------------
@app.route('/api/files')
@login_required
def api_files():
    """Return the markdown file tree as JSON."""
    roots = get_markdown_roots()

    # Keep old response shape for single root
    if len(roots) == 1:
        root_dir = next(iter(roots.values()))
        return jsonify(list_markdown_tree(root_dir))

    # For multi-root, group by root folder name
    grouped_tree = []
    for root_name, root_dir in roots.items():
        grouped_tree.append({
            'name': root_name,
            'type': 'directory',
            'path': root_name,
            'children': list_markdown_tree(root_dir, root_name),
        })
    return jsonify(grouped_tree)


@app.route('/api/read')
@login_required
def api_read():
    """Read and render a markdown file. Query param: ?path=relative/path.md"""
    rel_path = request.args.get('path', '').strip().replace('\\', '/')
    if not rel_path:
        return jsonify({'error': '缺少 path 参数'}), 400

    roots = get_markdown_roots()

    # Single-root compatibility: keep old path format
    if len(roots) == 1:
        base_dir = next(iter(roots.values()))
        inner_rel_path = rel_path
    else:
        clean_path = rel_path.strip('/')
        parts = clean_path.split('/', 1)
        root_name = parts[0] if parts else ''
        inner_rel_path = parts[1] if len(parts) > 1 else ''

        if root_name not in roots or not inner_rel_path:
            return jsonify({'error': '无效路径，请使用 根目录/文件.md 格式'}), 400

        base_dir = roots[root_name]

    full_path = get_safe_path(base_dir, inner_rel_path)
    if full_path is None or not os.path.isfile(full_path):
        return jsonify({'error': '文件不存在'}), 404

    if not full_path.lower().endswith('.md'):
        return jsonify({'error': '仅支持 Markdown 文件'}), 400

    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            raw = f.read()
    except Exception as e:
        return jsonify({'error': f'读取文件失败: {e}'}), 500

    md = markdown.Markdown(extensions=[
        'extra',
        'codehilite',
        'toc',
        'tables',
        'fenced_code',
        'sane_lists',
    ], extension_configs={
        'codehilite': {
            'css_class': 'codehilite',
            'linenums': False,
        },
    })

    html = md.convert(raw)
    toc  = getattr(md, 'toc', '')

    return jsonify({
        'filename': os.path.basename(full_path),
        'path': rel_path,
        'raw': raw,
        'html': html,
        'toc': toc,
    })


@app.route('/api/pygments.css')
@login_required
def pygments_css():
    """Return syntax highlight CSS."""
    formatter = HtmlFormatter(style='monokai')
    css = formatter.get_style_defs('.codehilite')
    return css, 200, {'Content-Type': 'text/css'}


# -------------------------------------------------------------------
# Main
# -------------------------------------------------------------------
if __name__ == '__main__':
    # Ensure markdown directories exist
    for md_dir in config.MARKDOWN_DIRS:
        os.makedirs(md_dir, exist_ok=True)
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)
