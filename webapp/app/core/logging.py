# app/core/logging.py
import logging
from logging.handlers import RotatingFileHandler
import time
from pathlib import Path
from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware

from .config import Settings

settings = Settings()

def setup_logger(name: str, log_file: str, level: int = logging.INFO) -> logging.Logger:
    """Set up logger"""
    log_dir = Path(settings.LOG_DIR)
    log_dir.mkdir(exist_ok=True)
    
    formatter = logging.Formatter(settings.LOG_FORMAT)
    
    # file processor
    file_handler = RotatingFileHandler(
        log_dir / log_file,
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    
    # console processor
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    # Configure logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

# Create logger
access_logger = setup_logger('access', 'access.log')
error_logger = setup_logger('error', 'error.log', logging.ERROR)
websocket_logger = setup_logger('websocket', 'websocket.log')

class LoggingMiddleware(BaseHTTPMiddleware):
    """HTTP request log middleware"""
    
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        request_id = str(int(start_time * 1000))
        
        try:
            # Logging request starts
            access_logger.info(
                f"Request {request_id} started | "
                f"{request.method} {request.url.path} | "
                f"Client: {request.client.host if request.client else 'unknown'}"
            )
            
            response = await call_next(request)
            
            # Logging request completed
            process_time = (time.time() - start_time) * 1000
            access_logger.info(
                f"Request {request_id} completed | "
                f"Status: {response.status_code} | "
                f"Time: {process_time:.2f}ms"
            )
            
            return response
            
        except Exception as e:
            error_logger.error(
                f"Request {request_id} failed | "
                f"Error: {str(e)}",
                exc_info=True
            )
            raise

def setup_logging(app: FastAPI) -> None:
    """Configure the application’s logging system"""
    app.add_middleware(LoggingMiddleware)