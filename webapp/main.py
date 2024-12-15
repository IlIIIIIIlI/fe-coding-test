# main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.core.logging import setup_logging
from app.core.config import Settings
from app.api.websocket import router as websocket_router

def create_application() -> FastAPI:
    settings = Settings()
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.PROJECT_VERSION,
        description=settings.PROJECT_DESCRIPTION
    )
    

    setup_logging(app)
    app.include_router(websocket_router)
    app.mount("/static", StaticFiles(directory="static"), name="static")
    
    @app.get("/")
    async def root():
        return FileResponse("static/index.html")
    
    return app

app = create_application()