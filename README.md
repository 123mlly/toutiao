# AI头条项目

Multilingual README: [中文](#中文) · [English](#english) · [日本語](#日本語)

This project is licensed under the [MIT License](LICENSE).

---

## 中文

基于 **FastAPI** 的新闻阅读后端：分类与新闻列表、用户注册登录、收藏与浏览历史，以及对接 **OpenAI 兼容协议**（如阿里云 DashScope）的 **流式 AI 聊天**。

### 技术栈

| 类别 | 选型 |
|------|------|
| Web | FastAPI、Uvicorn |
| 数据库 | MySQL，**异步** SQLAlchemy 2.x + aiomysql |
| 缓存 | Redis（如新闻分类等） |
| 安全 | bcrypt 密码哈希、Bearer Token |
| AI | `openai` 官方 SDK（`base_url` 指向兼容网关） |

### 功能概览

- **新闻**：分类分页、按分类新闻列表与分页、新闻详情；部分数据可走 Redis 缓存。
- **用户**：注册、登录（Token）、个人信息查询与修改、修改密码。
- **收藏**：检查/添加/取消收藏、收藏列表、清空收藏（需登录）。
- **历史记录**：添加浏览记录、分页列表、单条删除、清空（需登录）。
- **AI 聊天**：`POST` 流式返回 SSE，请求体为 OpenAI 风格的 `messages` 列表。

统一 JSON 封装见 `utils/response.py`（如 `ok` / `fail`）；需登录接口在请求头携带：`Authorization: Bearer <token>`。

### 环境要求

- Python 3.10+
- MySQL 5.7+ / 8.x
- Redis（使用缓存相关功能时需要）

### 快速开始

```bash
cd aitutiao
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env_example .env        # 编辑 .env
```

按 `models/` 在 MySQL 中建表后启动：

```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

- 健康检查：<http://127.0.0.1:8000/>
- Swagger UI：<http://127.0.0.1:8000/docs>

环境变量说明见 **`.env_example`**。`main.py` 使用 `load_dotenv(..., override=True)`；修改 `.env` 后请重启进程。

### API 前缀

| 模块 | 前缀 |
|------|------|
| 新闻 | `/api/news` |
| 用户 | `/api/user` |
| 收藏 | `/api/favorite` |
| 历史记录 | `/api/history` |
| AI 聊天 | `/api/aichat` |

### 项目结构（简要）

```text
main.py       # 入口、.env、路由与异常
config/       # 数据库、Redis
routes/ crud/ models/ schemas/ utils/ cache/
```

### 许可

本项目采用 **MIT License**，全文见仓库根目录 [`LICENSE`](LICENSE) 文件。

---

## English

**aitoutiao** is a **FastAPI** backend for a news-style app: categories & news listing, user registration/login, favorites & read history, plus **streaming AI chat** via an **OpenAI-compatible API** (e.g. Alibaba Cloud DashScope).

### Stack

| Layer | Choice |
|--------|--------|
| Web | FastAPI, Uvicorn |
| DB | MySQL, async SQLAlchemy 2.x + aiomysql |
| Cache | Redis (e.g. news categories) |
| Security | bcrypt, Bearer token |
| AI | Official `openai` Python SDK with a compatible `base_url` |

### Features

- **News**: paginated categories, news by category, detail; optional Redis cache.
- **Users**: register, login (token), profile read/update, change password.
- **Favorites**: check/add/remove, list, clear (auth required).
- **History**: add view, paginated list, delete one, clear all (auth required).
- **AI chat**: `POST` with SSE stream; body uses OpenAI-style `messages`.

JSON helpers: `utils/response.py` (`ok` / `fail`). Protected routes: header `Authorization: Bearer <token>`.

### Requirements

- Python 3.10+
- MySQL 5.7+ / 8.x
- Redis (if using cache features)

### Quick start

```bash
cd aitutiao
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env_example .env        # edit .env
```

Create tables from `models/` in MySQL, then:

```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

- Health: <http://127.0.0.1:8000/>
- OpenAPI UI: <http://127.0.0.1:8000/docs>

See **`.env_example`** for variables. `main.py` calls `load_dotenv(..., override=True)`; restart after changing `.env`.

### API prefixes

| Area | Prefix |
|------|--------|
| News | `/api/news` |
| User | `/api/user` |
| Favorites | `/api/favorite` |
| History | `/api/history` |
| AI chat | `/api/aichat` |

### License

Licensed under the **MIT License** — see [`LICENSE`](LICENSE).

---

## 日本語

**aitoutiao** は **FastAPI** 製のニュース系バックエンドです。カテゴリ・記事一覧、ユーザー登録／ログイン、お気に入り・閲覧履歴、**OpenAI 互換 API**（例：Alibaba DashScope）向けの **ストリーミング AI チャット** に対応します。

### 技術スタック

| 区分 | 採用技術 |
|------|-----------|
| Web | FastAPI、Uvicorn |
| DB | MySQL、非同期 SQLAlchemy 2.x + aiomysql |
| キャッシュ | Redis（カテゴリ等） |
| セキュリティ | bcrypt、Bearer トークン |
| AI | 公式 `openai` SDK（互換 `base_url`） |

### 機能概要

- **ニュース**：カテゴリページング、カテゴリ別記事一覧・詳細（Redis キャッシュ利用可）。
- **ユーザー**：登録、ログイン（トークン）、プロフィール取得・更新、パスワード変更。
- **お気に入り**：確認／追加／削除、一覧、全削除（要ログイン）。
- **履歴**：閲覧追加、ページング一覧、1件削除、全削除（要ログイン）。
- **AI チャット**：`POST` で SSE ストリーム。リクエストは OpenAI 形式の `messages`。

共通 JSON 形式は `utils/response.py`。要認証 API は `Authorization: Bearer <token>`。

### 動作環境

- Python 3.10+
- MySQL 5.7+ / 8.x
- Redis（キャッシュ利用時）

### クイックスタート

```bash
cd aitutiao
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env_example .env        # .env を編集
```

MySQL で `models/` に沿ってテーブル作成後：

```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

- ヘルス：<http://127.0.0.1:8000/>
- API ドキュメント：<http://127.0.0.1:8000/docs>

変数の説明は **`.env_example`**。`main.py` は `load_dotenv(..., override=True)` を使用。`.env` 変更後はプロセスを再起動してください。

### API プレフィックス

| モジュール | プレフィックス |
|------------|----------------|
| ニュース | `/api/news` |
| ユーザー | `/api/user` |
| お気に入り | `/api/favorite` |
| 履歴 | `/api/history` |
| AI チャット | `/api/aichat` |

### ライセンス

**MIT License** で提供します。全文はリポジトリルートの [`LICENSE`](LICENSE) を参照してください。
