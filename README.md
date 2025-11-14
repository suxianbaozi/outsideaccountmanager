# 账号管理系统

一个基于 Vue 3 和 FastAPI 的账号管理系统，支持用户注册、登录和账号信息的增删改查。

## 技术栈

### 后端
- FastAPI - Python Web 框架
- SQLAlchemy - ORM
- SQLite - 数据库
- JWT - 身份认证
- Pydantic - 数据验证

### 前端
- Vue 3 - 前端框架
- Vue Router - 路由管理
- Pinia - 状态管理
- Axios - HTTP 客户端
- Vite - 构建工具

## 项目结构

```
.
├── backend/          # FastAPI 后端
│   ├── app/
│   │   ├── routers/  # API 路由
│   │   ├── models.py # 数据库模型
│   │   ├── schemas.py # Pydantic 模式
│   │   └── security.py # 安全相关
│   ├── main.py      # 应用入口
│   └── requirements.txt
├── frontend/         # Vue 前端
│   ├── src/
│   │   ├── views/    # 页面组件
│   │   ├── stores/   # Pinia 状态管理
│   │   ├── router/   # 路由配置
│   │   └── api/      # API 封装
│   └── package.json
└── README.md
```

## 快速开始

### 后端设置

1. 进入后端目录：
```bash
cd backend
```

2. 创建虚拟环境（推荐）：
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. 安装依赖：
```bash
pip install -r requirements.txt
```

4. 配置环境变量（可选）：
```bash
cp .env.example .env
# 编辑 .env 文件设置 SECRET_KEY
```

5. 启动后端服务：
```bash
uvicorn main:app --reload --port 8000
```

后端 API 文档访问地址：http://localhost:8000/docs

### 前端设置

1. 进入前端目录：
```bash
cd frontend
```

2. 安装依赖：
```bash
npm install
```

3. 启动开发服务器：
```bash
npm run dev
```

前端应用访问地址：http://localhost:5173

## 功能特性

- ✅ 用户注册和登录
- ✅ JWT 身份认证
- ✅ 账号信息的增删改查
- ✅ 响应式设计
- ✅ 数据验证和错误处理

## API 端点

### 认证相关
- `POST /api/auth/register` - 用户注册
- `POST /api/auth/login` - 用户登录
- `GET /api/auth/me` - 获取当前用户信息

### 账号管理
- `GET /api/accounts/` - 获取账号列表
- `POST /api/accounts/` - 创建新账号
- `GET /api/accounts/{id}` - 获取单个账号
- `PUT /api/accounts/{id}` - 更新账号
- `DELETE /api/accounts/{id}` - 删除账号

## 使用说明

1. 首次使用需要注册账号
2. 登录后可以添加、编辑和删除账号信息
3. 所有账号信息都加密存储在数据库中
4. 每个用户只能看到和管理自己的账号

## 注意事项

- 默认使用 SQLite 数据库，生产环境建议使用 PostgreSQL 或 MySQL
- 请在生产环境中修改 `SECRET_KEY`
- 前端代理配置在 `vite.config.js` 中，确保后端服务运行在 8000 端口
