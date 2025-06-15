from datetime import datetime, timezone

from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from typing import Optional
import os
from sqlalchemy.orm import Session
from models.database import get_db, Admin, User

# JWT配置
ALGORITHM = "HS256"

class BaseContext:
    current_user_id: Optional[int] = None

def get_token_from_request(request: Request) -> Optional[str]:
    """从请求中获取token"""
    token = request.headers.get("token")
    if token:
        return token
    return None

def verify_token(token: str, password: str) -> dict:
    """验证token并返回payload"""
    try:
        # 先不验证签名，获取audience
        unverified_payload = jwt.get_unverified_claims(token)
        audience = unverified_payload.get("aud")
        if not audience:
            raise Exception("Missing aud")

        # 使用用户密码验证token
        payload = jwt.decode(token, key=password, audience=audience, algorithms=[ALGORITHM])

        return payload
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token verification failed",
            headers={"WWW-Authenticate": "Bearer"},
        )

def get_user_password(user_id: int, role: str) -> Optional[str]:
    """根据用户ID和角色获取用户密码"""
    db: Session = next(get_db())
    try:
        if role == "ADMIN":
            # 从admin表获取密码
            admin = db.query(Admin).filter(Admin.id == user_id).first()
            if admin:
                return admin.password
        elif role == "USER":
            # 从user表获取密码
            user = db.query(User).filter(User.id == user_id).first()
            if user:
                return user.password
        return None
    finally:
        db.close()

async def jwt_auth_middleware(request: Request, call_next):
    """JWT认证中间件"""
    # 跳过无需认证的接口
    if request.url.path.startswith("/docs") or request.url.path.startswith("/openapi.json"):
        return await call_next(request)

    token = get_token_from_request(request)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        # 解析token获取用户信息
        unverified_payload = jwt.get_unverified_claims(token)
        audience = unverified_payload.get("aud")
        if not audience:
            raise Exception("Missing aud")

        # 解析用户ID和角色
        user_id_str, role = audience.split("-")
        user_id = int(user_id_str)

        # 根据角色获取用户密码
        user_password = get_user_password(user_id, role)
        if not user_password:
            raise Exception("User not found")

        # 验证token
        payload = verify_token(token, user_password)

        # 保存user_id到上下文
        BaseContext.current_user_id = user_id

        # 给后续处理过程挂载payload
        request.state.user_payload = payload

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token invalid: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return await call_next(request) 