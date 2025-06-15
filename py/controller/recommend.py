from fastapi import APIRouter, Request, HTTPException, status, UploadFile, File
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional, List
import asyncio
import json
from datetime import datetime
from sqlalchemy.orm import Session
from utils.jwt import BaseContext
from models.database import get_db, FoodInfo, UserInfo, SleepInfo, SportInfo, IllnessInfo, User
from datetime import datetime
from datetime import timedelta
from services.health_agent_service import init_agent, MyCallbackHandler, query_with_user_knowledge, init_memory
from services.file_loader import load_user_knowledge
import os
import shutil


async def recommend():
    # 获取数据库会话
    db = next(get_db())

    try:
        # 如果指定了会话ID，验证会话所有权
        user_id = 2
        now = datetime.now() #获取当天时间
        #two_days_later = now + timedelta(days=2) 两天后时间的获取方法




    except Exception as e:
        db.close()
        raise e