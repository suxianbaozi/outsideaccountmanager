from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, accounts
from app.database import engine, Base

# 创建数据库表
Base.metadata.create_all(bind=engine)

app = FastAPI(title="账号管理系统", version="1.0.0")

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth.router, prefix="/api/auth", tags=["认证"])
app.include_router(accounts.router, prefix="/api/accounts", tags=["账号管理"])


@app.get("/")
async def root():
    return {"message": "账号管理系统API"}


@app.get("/api/health")
async def health():
    return {"status": "ok"}
