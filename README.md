# 📖 Markdown 知识库阅读器

一个基于 Flask 的 Web 端 Markdown 知识库阅读器。支持目录浏览、文件渲染、代码高亮和用户认证。

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0-green?logo=flask&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ 功能特性

| 功能 | 说明 |
|------|------|
| 📂 文件树浏览 | 支持单目录或多根目录（根分组）展示 `.md` 文件，支持多级目录折叠 |
| 📖 Markdown 渲染 | 支持表格、代码块、引用、列表、目录等 GFM 扩展语法 |
| 🎨 代码高亮 | 基于 Pygments 的语法高亮（Monokai 主题），支持数十种语言 |
| ⬇️ 文件下载 | 支持直接下载当前查看的 Markdown 原文件 |
| 🔍 文件搜索 | 侧边栏实时搜索过滤文件名 |
| 🔐 用户认证 | 登录 / 注册 / 退出，密码使用 Werkzeug 安全哈希存储 |
| 📱 响应式设计 | 桌面和移动端自适应布局 |
| 🛡️ 路径安全 | 防止路径遍历攻击，仅允许访问配置目录内的文件 |

## 📸 预览

```
┌──────────────────────────────────────────────────┐
│  📖 Markdown 知识库阅读器             👤 admin   │
├────────────┬─────────────────────────────────────┤
│ 🔍 搜索... │  📄 欢迎.md                         │
│            │                                     │
│ 📄 欢迎.md │  # 欢迎使用 Markdown 知识库阅读器     │
│ 📁 指南    │                                     │
│   📄 使用  │  这是一个示例文档，用于展示           │
│   📄 语法  │  Markdown 知识库阅读器的功能。        │
│            │                                     │
└────────────┴─────────────────────────────────────┘
```

## 🚀 快速开始

### 环境要求

- Python 3.10+

### 安装

```bash
# 克隆项目
git clone <repo-url>
cd md_reader

# 创建虚拟环境（推荐）
python -m venv .venv

# 激活虚拟环境
# Windows
.venv\Scripts\activate
# Linux / macOS
source .venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 启动

```bash
python app.py
```

启动后访问 **http://localhost:5000**

## 🔑 默认账户

| 用户名 | 密码 |
|--------|------|
| `admin` | `Webank@123` |

> ⚠️ **安全提示**：生产环境中请务必修改默认密码。

### 修改默认管理员密码

编辑 `app.py` 中第 38 行：

```python
_users['admin'] = generate_password_hash('Webank@123')
#                                         ^^^^^^^^^^^^ 修改为你的密码
```

### 注册新用户

访问 http://localhost:5000/register 即可注册新用户（密码至少 6 位）。

> **注意**：当前用户数据存储在内存中，服务重启后注册的用户会丢失，仅保留默认的 admin 账号。

## ⚙️ 配置

### 配置文件

编辑 `config.py`：

```python
# Markdown 文件所在目录
MARKDOWN_DIR = '/path/to/your/markdown/files'

# 会话密钥（请修改为随机字符串）
SECRET_KEY = 'your-random-secret-key'

# 服务监听地址与端口
HOST = '0.0.0.0'
PORT = 5000

# 调试模式
DEBUG = True
```

### 环境变量

也可以通过环境变量覆盖配置（优先级高于配置文件）：

| 环境变量 | 说明 | 默认值 |
|----------|------|--------|
| `MD_READER_DIRS` | 多个 Markdown 根目录（逗号/分号分隔） | 空 |
| `MD_READER_DIR` | Markdown 文件目录 | `./docs` |
| `MD_READER_PORT` | 服务端口 | `5000` |
| `MD_READER_SECRET` | 会话密钥 | 内置默认值 |
| `MD_READER_DEBUG` | 调试模式 (`true`/`false`) | `true` |

目录优先级：`MD_READER_DIRS` > `MD_READER_DIR`。

示例：

```bash
# Linux / macOS
export MD_READER_DIRS=/data/md/team-a,/data/md/team-b
export MD_READER_DIR=/home/user/notes
export MD_READER_PORT=8080
python app.py

# Windows PowerShell
$env:MD_READER_DIRS = "D:\md\team-a;D:\md\team-b"
$env:MD_READER_DIR = "D:\my-notes"
$env:MD_READER_PORT = "8080"
python app.py
```

## 📁 项目结构

```
md_reader/
├── app.py                 # Flask 主应用（路由、API、用户认证）
├── config.py              # 配置文件
├── requirements.txt       # Python 依赖
├── gunicorn.conf.py       # Gunicorn 生产服务器配置
├── Dockerfile             # Docker 镜像构建
├── docker-compose.yml     # Docker Compose 编排
├── .env.example           # 环境变量模板
├── templates/
│   ├── base.html          # 基础模板（通用样式、Flash 消息）
│   ├── login.html         # 登录页面
│   ├── register.html      # 注册页面
│   └── index.html         # 主界面（侧边文件树 + Markdown 阅读区）
├── deploy/
│   ├── nginx.conf         # Nginx 反向代理配置（HTTPS）
│   └── md-reader.service  # Systemd 服务配置文件
├── log/                   # 运行日志（自动生成，已 gitignore）
│   ├── access.log
│   ├── error.log
│   └── gunicorn.pid
└── docs/                  # 示例 Markdown 文件（默认阅读目录）
    ├── 欢迎.md
    └── 指南/
        ├── 使用指南.md
        └── Markdown语法参考.md
```

## 🔌 API 接口

所有 API 需要登录后才能访问。

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/files` | 获取 Markdown 文件树（JSON，支持多根分组） |
| GET | `/api/read?path=<相对路径>` | 读取并渲染指定 Markdown 文件（多根模式下为 `根名/文件.md`） |
| GET | `/api/download?path=<相对路径>` | 下载 Markdown 原文件 |
| GET | `/api/pygments.css` | 获取代码高亮 CSS 样式 |

### 响应示例

**GET** `/api/files`

单根目录示例：

```json
[
  { "name": "欢迎.md", "type": "file", "path": "欢迎.md" },
  {
    "name": "指南",
    "type": "directory",
    "path": "指南",
    "children": [
      { "name": "使用指南.md", "type": "file", "path": "指南/使用指南.md" }
    ]
  }
]
```

多根目录示例：

```json
[
  {
    "name": "team-a",
    "type": "directory",
    "path": "team-a",
    "children": [
      { "name": "A.md", "type": "file", "path": "team-a/A.md" }
    ]
  },
  {
    "name": "team-b",
    "type": "directory",
    "path": "team-b",
    "children": [
      { "name": "B.md", "type": "file", "path": "team-b/B.md" }
    ]
  }
]
```

**GET** `/api/read?path=欢迎.md`

```json
{
  "filename": "欢迎.md",
  "path": "欢迎.md",
  "raw": "# 欢迎使用 ...",
  "html": "<h1>欢迎使用 ...</h1>",
  "toc": "<div class=\"toc\">...</div>"
}
```

## 🚢 生产部署
### 方式一：Docker（推荐）

```bash
# 编辑 docker-compose.yml 中的卷路径和环境变量，然后：
docker compose up -d
```

### 方式二：Gunicorn 直接部署

```bash
# 安装依赖
pip install -r requirements.txt gunicorn

# 配置环境变量
cp .env.example .env
# 编辑 .env 填入实际值

# 后台启动（日志输出到 log/ 目录）
gunicorn -c gunicorn.conf.py app:app --daemon
```

### 日志管理

日志自动写入 `log/` 目录：

```
log/
├── access.log      # 访问日志
├── error.log       # 错误日志
└── gunicorn.pid    # 进程 PID 文件
```

常用命令：

```bash
# 查看实时日志
tail -f log/access.log
tail -f log/error.log

# 优雅重启（不中断服务）
kill -HUP $(cat log/gunicorn.pid)

# 停止服务
kill $(cat log/gunicorn.pid)
```

### 方式三：Systemd 服务（Linux 开机自启）

项目已提供配置文件 `deploy/md-reader.service`，部署步骤：

```bash
# 1. 复制服务文件到 systemd 目录
sudo cp deploy/md-reader.service /etc/systemd/system/

# 2. 按需编辑路径（默认 /data/appsystems/MD_READER）
sudo vim /etc/systemd/system/md-reader.service

# 3. 重载 systemd 配置
sudo systemctl daemon-reload

# 4. 启用并启动服务（开机自启）
sudo systemctl enable --now md-reader
```

服务管理命令：

```bash
sudo systemctl start md-reader       # 启动
sudo systemctl stop md-reader        # 停止
sudo systemctl restart md-reader     # 重启
sudo systemctl reload md-reader      # 优雅重载（不中断连接）
sudo systemctl status md-reader      # 查看状态

# 查看服务日志
journalctl -u md-reader -f               # 实时日志
journalctl -u md-reader --since today    # 今天的日志
```

> 服务文件包含安全加固配置（`PrivateTmp`、`ProtectSystem=strict` 等），异常退出 5 秒后自动重启。
> 若 Markdown 目录位于 `/home/...`，请保持 `ProtectHome=false`（服务文件中已配置）。

### 生产检查清单

| 项目 | 操作 |
|------|------|
| ⚠️ 修改密钥 | 设置 `MD_READER_SECRET` 为随机 32+ 字符 |
| ⚠️ 修改密码 | 编辑 `app.py` 中默认 admin 密码 |
| ⚠️ 关闭调试 | 设置 `MD_READER_DEBUG=false` |
| 🔒 启用 HTTPS | 使用 Nginx + Let's Encrypt（参考 `deploy/nginx.conf`） |
| 📁 挂载数据 | 单目录用 `MD_READER_DIR`，多目录用 `MD_READER_DIRS` |

## 🛠️ 技术栈

| 组件 | 技术 |
|------|------|
| 后端框架 | [Flask 3.0](https://flask.palletsprojects.com/) |
| 生产服务器 | [Gunicorn](https://gunicorn.org/) |
| 用户认证 | [Flask-Login](https://flask-login.readthedocs.io/) |
| 密码加密 | [Werkzeug Security](https://werkzeug.palletsprojects.com/) |
| Markdown 渲染 | [Python-Markdown](https://python-markdown.github.io/) |
| 代码高亮 | [Pygments](https://pygments.org/) |
| 前端 | 原生 HTML / CSS / JavaScript（无框架依赖） |
| 容器化 | Docker / Docker Compose |

## 📝 License

MIT
