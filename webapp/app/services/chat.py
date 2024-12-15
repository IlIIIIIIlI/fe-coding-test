# app/services/chat.py
from fastapi import WebSocket
from typing import Dict, Set
from ..core.logging import websocket_logger, error_logger

class ChatManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.connected_users: Set[str] = set()
    
    async def connect(self, websocket: WebSocket, username: str) -> bool:
        """Handling new WebSocket connections"""
        if username in self.connected_users:
            websocket_logger.warning(f"Connection rejected - Username '{username}' already taken")
            await websocket.close(code=1008, reason="Username already taken")
            return False
        
        await websocket.accept()
        self.active_connections[username] = websocket
        self.connected_users.add(username)
        websocket_logger.info(f"User '{username}' connected")
        return True
    
    def disconnect(self, username: str) -> None:
        """Handling WebSocket disconnections"""
        if username in self.active_connections:
            del self.active_connections[username]
            self.connected_users.remove(username)
            websocket_logger.info(f"User '{username}' disconnected")
    
    async def broadcast(self, sender: str, message: str) -> None:
        """Broadcast message to all connected clients"""
        if not message.strip():
            return
            
        formatted_message = f"{sender}: {message}"
        websocket_logger.info(f"Broadcasting message from '{sender}': {message[:100]}...")
        
        for username, connection in self.active_connections.items():
            try:
                await connection.send_text(formatted_message)
            except Exception as e:
                error_logger.error(f"Error sending message to '{username}': {str(e)}")
                await self.handle_disconnection(username)
    
    async def handle_disconnection(self, username: str) -> None:
        """Handle client abnormal disconnection"""
        self.disconnect(username)
        await self.broadcast("System", f"{username} has left the chat")