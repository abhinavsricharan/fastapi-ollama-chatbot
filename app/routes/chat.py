from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import StreamingResponse
from app.models.schemas import ChatRequest, ChatResponse, HistoryResponse, Message
from app.services import memory_service, llm_service

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Non-streaming REST chat endpoint."""
    history = memory_service.get_history(request.session_id)
    memory_service.add_message(request.session_id, "user", request.message)

    try:
        response_text = await llm_service.chat(history, request.message)
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"LLM error: {str(e)}")

    memory_service.add_message(request.session_id, "assistant", response_text)

    return ChatResponse(session_id=request.session_id, response=response_text)


@router.websocket("/ws/chat/{session_id}")
async def websocket_chat(websocket: WebSocket, session_id: str):
    """Streaming WebSocket chat endpoint."""
    await websocket.accept()
    try:
        while True:
            user_message = await websocket.receive_text()
            if not user_message.strip():
                continue

            history = memory_service.get_history(session_id)
            memory_service.add_message(session_id, "user", user_message)

            full_response = ""
            try:
                async for token in llm_service.stream_chat(history, user_message):
                    full_response += token
                    await websocket.send_text(token)

                # Signal end of response
                await websocket.send_text("[DONE]")
                memory_service.add_message(session_id, "assistant", full_response)

            except Exception as e:
                await websocket.send_text(f"[ERROR] {str(e)}")

    except WebSocketDisconnect:
        pass


@router.get("/history/{session_id}", response_model=HistoryResponse)
async def get_history(session_id: str):
    """Retrieve conversation history for a session."""
    messages = memory_service.get_history(session_id)
    return HistoryResponse(
        session_id=session_id,
        messages=[Message(**m) for m in messages]
    )


@router.delete("/history/{session_id}")
async def clear_history(session_id: str):
    """Clear conversation history for a session."""
    existed = memory_service.clear_history(session_id)
    if not existed:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"message": f"History cleared for session '{session_id}'"}
