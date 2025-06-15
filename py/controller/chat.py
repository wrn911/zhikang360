# ==== 1. 在文件开头添加导入 ====
from fastapi import APIRouter, Request, HTTPException, status, UploadFile, File, WebSocket, WebSocketDisconnect
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional, List
import asyncio
import json
from datetime import datetime
from sqlalchemy.orm import Session
from utils.jwt import BaseContext
from models.database import get_db, ChatHistory, UserKnowledgeFile, ChatSession
from services.health_agent_service import init_agent, MyCallbackHandler, query_with_user_knowledge, init_memory
from services.intent_recognizer import recognize_intent, get_all_intents  # 新增导入


# 在您的路由文件开头（import语句后）添加智能体配置
AGENTS = {
    "general": {
        "name": "健康助手",
        "icon": "🏥",
        "prompt": "你是一个专业的健康助手，提供全面的健康咨询和建议。请用专业但易懂的语言回答用户的健康问题，重点关注准确性和实用性。"
    },
    "nutritionist": {
        "name": "营养师",
        "icon": "🥗",
        "prompt": "你是一位专业的营养师，专门提供饮食营养建议。请从营养学角度分析问题，提供科学的膳食指导，包括食物搭配、营养摄入、饮食计划等。回答要专业且实用，注重营养均衡。"
    },
    "trainer": {
        "name": "健身教练",
        "icon": "💪",
        "prompt": "你是一位专业的健身教练，专门提供运动健身指导。请提供科学的运动建议、训练计划、动作指导，帮助用户达到健身目标。注重安全性和可操作性，考虑用户的身体状况。"
    },
    "psychologist": {
        "name": "心理咨询师",
        "icon": "🧠",
        "prompt": "你是一位温和的心理咨询师，专门帮助用户处理情绪和心理健康问题。请用同理心倾听，提供专业的心理支持和建议，语气要温暖且有耐心。注重保护用户隐私。"
    }
}

router = APIRouter(prefix="/chat", tags=["chat"])

# 初始化共享记忆
shared_memory = init_memory()

# 初始化不同模型的链
default_chain = init_agent(memory=shared_memory)
deepthink_chain = init_agent(model="DeepSeek-R1", base_url='http://10.2.8.77:3000/v1', api_key='sk-93nWYhI8SrnXad5m9932CeBdDeDf4233B21d93D217095f22', memory=shared_memory)


# ==== 2. 修改ChatRequest模型（如果需要的话） ====
class ChatRequest(BaseModel):
    question: str
    session_id: Optional[int] = None
    title: Optional[str] = None
    model: Optional[str] = "glm-4-flash"
    agent_id: Optional[str] = "general"  # 如果您已经实现了智能体
    system_prompt: Optional[str] = None


# ==== 3. 添加获取会话智能体的辅助函数 ====
def get_session_agent(session_id: int, db: Session, user_id: int) -> str:
    """获取会话绑定的智能体ID"""
    if not session_id:
        return "general"

    session = db.query(ChatSession).filter(
        ChatSession.id == session_id,
        ChatSession.user_id == user_id
    ).first()

    if session and hasattr(session, 'agent_id'):
        return session.agent_id
    return "general"


async def load_chat_history(user_id: int, session_id: Optional[int], db: Session):
    """从数据库加载对话历史到内存"""
    # 清除当前内存
    shared_memory.clear()
    
    # 只有在指定了会话ID时才加载历史记录
    if session_id:
        # 构建查询条件
        query = db.query(ChatHistory).filter(
            ChatHistory.user_id == user_id,
            ChatHistory.session_id == session_id
        )
        
        # 从数据库获取最近的10条历史记录
        chat_histories = query.order_by(ChatHistory.created_at.desc()).limit(10).all()
        
        # 按时间顺序加载到内存
        for item in reversed(chat_histories):
            shared_memory.save_context({"input": item.question}, {"output": item.answer})


# ==== 3. 修改generate_stream函数 ====
async def generate_stream(
        question: str,
        user_id: int,
        session_id: Optional[int],
        db: Session,
        title: Optional[str] = None,
        model: str = "glm-4-flash",
        agent_id: str = "general",
        system_prompt: Optional[str] = None
):
    """生成流式响应"""
    queue = asyncio.Queue()
    callback = MyCallbackHandler(queue)

    # 根据模型选择使用的chain
    chain = deepthink_chain if model == "DeepSeek-R1" else default_chain

    # 处理智能体提示词（如果已实现智能体功能）
    if system_prompt:
        final_prompt = system_prompt
        enhanced_question = f"系统角色设定：{final_prompt}\n\n用户问题：{question}"
    else:
        enhanced_question = question

    # 创建一个变量来存储完整的回答
    full_answer = []
    new_session = None

    try:
        # 如果没有会话ID且有标题，创建新会话
        if not session_id and title:
            new_session = ChatSession(
                user_id=user_id,
                title=title
            )
            db.add(new_session)
            db.commit()
            db.refresh(new_session)
            session_id = new_session.id

        # 异步执行查询，传入 callback
        task = asyncio.create_task(
            query_with_user_knowledge(chain, shared_memory, enhanced_question, user_id, [callback]))

        # 流式返回结果
        while True:
            try:
                token = await queue.get()
                if token is None:  # 收到结束信号
                    # 保存对话历史到数据库
                    answer_text = ''.join(full_answer)
                    if answer_text:  # 只在有回答时保存
                        chat_history = ChatHistory(
                            user_id=user_id,
                            session_id=session_id,
                            question=question,
                            answer=answer_text,
                            created_at=datetime.now()
                        )
                        db.add(chat_history)
                        db.commit()

                        # 更新内存中的对话历史
                        shared_memory.save_context({"input": question}, {"output": answer_text})

                    # ==== 新增：意图识别 ====
                    intent_result = recognize_intent(question)

                    # 发送结束标记，包含意图信息
                    response_data = {
                        'token': '',
                        'end': True,
                        'intent': intent_result  # 新增意图信息
                    }
                    if new_session:
                        response_data['session'] = {
                            'id': new_session.id,
                            'title': new_session.title
                        }
                    yield f"data: {json.dumps(response_data, ensure_ascii=False)}\n\n"
                    break

                full_answer.append(token)
                yield f"data: {json.dumps({'token': token, 'end': False}, ensure_ascii=False)}\n\n"

            except asyncio.CancelledError:
                yield f"data: {json.dumps({'error': 'Stream cancelled'}, ensure_ascii=False)}\n\n"
                break

        # 等待任务完成
        await task

    except Exception as e:
        # 发送错误信息
        yield f"data: {json.dumps({'error': str(e)}, ensure_ascii=False)}\n\n"
    finally:
        # 清理资源
        if not task.done():
            task.cancel()
        db.close()

@router.get("/history")
async def get_chat_history(
    page: int = 1,
    page_size: int = 10
):
    """获取对话历史"""
    user_id = BaseContext.current_user_id
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authenticated"
        )
        
    db = next(get_db())
    try:
        # 从数据库获取历史记录
        total = db.query(ChatHistory).filter(
            ChatHistory.user_id == user_id
        ).count()
        
        chat_histories = db.query(ChatHistory).filter(
            ChatHistory.user_id == user_id
        ).order_by(ChatHistory.created_at.asc())\
         .offset((page - 1) * page_size)\
         .limit(page_size)\
         .all()

        # 转换为所需格式
        history = [
            {
                "question": item.question,
                "answer": item.answer,
                "timestamp": item.created_at.isoformat()
            }
            for item in chat_histories
        ]

        return {
            "chat_history": history,
            "total": total,
            "page": page,
            "page_size": page_size
        }
    finally:
        db.close()

@router.post("/clear")
async def clear_chat_history():
    """清除对话历史"""
    user_id = BaseContext.current_user_id
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authenticated"
        )
        
    db = next(get_db())
    try:
        # 清除数据库中的历史记录
        db.query(ChatHistory).filter(ChatHistory.user_id == user_id).delete()
        db.commit()

        # 清除内存中的历史记录
        shared_memory.clear()

        return {"message": "对话历史已清除"}
    finally:
        db.close()

@router.get("/test")
async def test():
    return {"message": "测试成功"}


# ==== 4. 修改WebSocket处理函数 ====
@router.websocket("/ws_chat")
async def websocket_chat(websocket: WebSocket):
    await websocket.accept()
    db = next(get_db())
    try:
        while True:
            data = await websocket.receive_text()
            try:
                req = json.loads(data)
                user_id = BaseContext.current_user_id
                question = req.get("question")
                session_id = req.get("session_id")
                title = req.get("title")
                model = req.get("model", "glm-4-flash")
                agent_id = req.get("agent_id", "general")  # 新增：获取智能体ID

                # 加载历史
                await load_chat_history(user_id, session_id, db)

                # ==== 核心修改：确定要使用的智能体 ====
                if session_id:
                    # 现有会话：使用会话绑定的智能体
                    current_agent_id = get_session_agent(session_id, db, user_id)
                else:
                    # 新会话：使用前端传来的智能体
                    current_agent_id = agent_id

                # 获取智能体配置并构建系统提示词
                agent_config = AGENTS.get(current_agent_id, AGENTS["general"])
                system_prompt = agent_config["prompt"]
                enhanced_question = f"系统角色设定：{system_prompt}\n\n用户问题：{question}"

                # 生成流式响应
                queue = asyncio.Queue()
                callback = MyCallbackHandler(queue)
                chain = deepthink_chain if model == "DeepSeek-R1" else default_chain
                full_answer = []
                new_session = None

                # ==== 新会话处理：保存智能体信息 ====
                if not session_id and title:
                    new_session = ChatSession(
                        user_id=user_id,
                        title=title,
                        agent_id=current_agent_id  # 重要：保存智能体ID
                    )
                    db.add(new_session)
                    db.commit()
                    db.refresh(new_session)
                    session_id = new_session.id

                # 启动异步任务
                task = asyncio.create_task(
                    query_with_user_knowledge(chain, shared_memory, enhanced_question, user_id, [callback]))
                try:
                    while True:
                        token = await queue.get()
                        if token is None:
                            answer_text = ''.join(full_answer)
                            if answer_text:
                                chat_history = ChatHistory(
                                    user_id=user_id,
                                    session_id=session_id,
                                    question=question,  # 保存原始问题
                                    answer=answer_text,
                                    created_at=datetime.now()
                                )
                                db.add(chat_history)
                                db.commit()
                                shared_memory.save_context({"input": question}, {"output": answer_text})

                            # 意图识别（如果您已实现）
                            try:
                                intent_result = recognize_intent(question)
                            except:
                                intent_result = None

                            # 发送结束信号
                            response_data = {
                                "token": "",
                                "end": True,
                                "intent": intent_result
                            }
                            if new_session:
                                response_data["session"] = {
                                    "id": new_session.id,
                                    "title": new_session.title,
                                    "agent_id": new_session.agent_id,  # 新增
                                    "agent_name": agent_config["name"],  # 新增
                                    "agent_icon": agent_config["icon"]  # 新增
                                }

                            await websocket.send_json(response_data)
                            break
                        full_answer.append(token)
                        await websocket.send_json({"token": token, "end": False})
                    await task
                except Exception as e:
                    await websocket.send_json({"error": str(e)})
                finally:
                    if not task.done():
                        task.cancel()
            except Exception as e:
                await websocket.send_json({"error": str(e)})
    except WebSocketDisconnect:
        pass
    finally:
        db.close()


# ==== 5. 新增：获取意图列表的接口（可选） ====
@router.get("/intents")
async def get_intent_list():
    """获取所有可用的意图列表"""
    return get_all_intents()


# 添加获取智能体列表的接口（可选）
@router.get("/agents")
async def get_agents():
    """获取可用的智能体列表"""
    return {"agents": AGENTS}