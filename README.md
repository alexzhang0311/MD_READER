# 📖 Markdown Reader

一个基于 Flask 的 Web 端 Markdown 文件阅读器。支持目录浏览、文件渲染、代码高亮和用户认证。

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0-green?logo=flask&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ 功能特性

| 功能 | 说明 |
|------|------|
| 📂 文件树浏览 | 递归展示指定目录下所有 `.md` 文件，支持多级目录折叠 |
| 📖 Markdown 渲染 | 支持表格、代码块、引用、列表、目录等 GFM 扩展语法 |
| 🎨 代码高亮 | 基于 Pygments 的语法高亮（Monokai 主题），支持数十种语言 |
| 🔍 文件搜索 | 侧边栏实时搜索过滤文件名 |
| 🔐 用户认证 | 登录 / 注册 / 退出，密码使用 Werkzeug 安全哈希存储 |
| 📱 响应式设计 | 桌面和移动端自适应布局 |
| 🛡️ 路径安全 | 防止路径遍历攻击，仅允许访问配置目录内的文件 |

## 📸 预览

```
┌──────────────────────────────────────────────────┐
│  📖 KYC 知识库                   👤 admin   │
├────────────┬─────────────────────────────────────┤
│ 🔍 搜索... │  📄 欢迎.md                         │
│            │                                     │
│ 📄 欢迎.md │  # 欢迎使用 KYC 知识库          │
│ 📁 指南    │                                     │
│   📄 使用  │  这是一个示例文档，用于展示            │
│   📄 语法  │  KYC 知识库的功能。              │
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
| `admin` | `admin123` |

> ⚠️ **安全提示**：生产环境中请务必修改默认密码。

### 修改默认管理员密码

编辑 `app.py` 中第 40 行：

```python
_users['admin'] = generate_password_hash('admin123')
#                                         ^^^^^^^^ 修改为你的密码
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
| `MD_READER_DIR` | Markdown 文件目录 | `./docs` |
| `MD_READER_PORT` | 服务端口 | `5000` |
| `MD_READER_SECRET` | 会话密钥 | 内置默认值 |
| `MD_READER_DEBUG` | 调试模式 (`true`/`false`) | `true` |

示例：

```bash
# Linux / macOS
export MD_READER_DIR=/home/user/notes
export MD_READER_PORT=8080
python app.py

# Windows PowerShell
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
├── templates/
│   ├── base.html          # 基础模板（通用样式、Flash 消息）
│   ├── login.html         # 登录页面
│   ├── register.html      # 注册页面
│   └── index.html         # 主界面（侧边文件树 + Markdown 阅读区）
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
| GET | `/api/files` | 获取 Markdown 文件树（JSON） |
| GET | `/api/read?path=<相对路径>` | 读取并渲染指定 Markdown 文件 |
| GET | `/api/pygments.css` | 获取代码高亮 CSS 样式 |

### 响应示例

**GET** `/api/files`

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

## 🛠️ 技术栈

| 组件 | 技术 |
|------|------|
| 后端框架 | [Flask 3.0](https://flask.palletsprojects.com/) |
| 用户认证 | [Flask-Login](https://flask-login.readthedocs.io/) |
| 密码加密 | [Werkzeug Security](https://werkzeug.palletsprojects.com/) |
| Markdown 渲染 | [Python-Markdown](https://python-markdown.github.io/) |
| 代码高亮 | [Pygments](https://pygments.org/) |
| 前端 | 原生 HTML / CSS / JavaScript（无框架依赖） |

## 📝 License

MIT
