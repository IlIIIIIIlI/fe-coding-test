# app/api/websocket.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from ..services.chat import ChatManager
from ..core.logging import websocket_logger, error_logger

router = APIRouter()
chat_manager = ChatManager()

@router.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str):
    """WebSocket connection endpoint"""
    try:
        # Establish connection
        connection_successful = await chat_manager.connect(websocket, username)
        if not connection_successful:
            return
        
        # Send welcome message
        await chat_manager.broadcast("System", f"{username} has joined the chat")
        
        # Process messages
        while True:
            try:
                message = await websocket.receive_text()
                websocket_logger.debug(f"Received message from '{username}': {message[:100]}...")
                await chat_manager.broadcast(username, message)
                
            except WebSocketDisconnect:
                raise
                
            except Exception as e:
                error_logger.error(f"Error processing message from '{username}': {str(e)}")
                continue
                
    except WebSocketDisconnect:
        await chat_manager.handle_disconnection(username)
        
    except Exception as e:
        error_logger.error(f"WebSocket error for user '{username}': {str(e)}")
        try:
            await websocket.close(code=1011, reason=str(e))
        except:
            pass