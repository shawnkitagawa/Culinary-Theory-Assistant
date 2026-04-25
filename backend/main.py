from fastapi import FastAPI, Request
from app.database.db import Document, Chunk 
from app.database.base import engine, Base
from app.routers.documents import router as document_router
from app.routers.answer import router as answer_router
from fastapi.templating import Jinja2Templates
from app.routers.ui import router as ui_router
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from app.core.config import limiter
from fastapi.responses import JSONResponse




app = FastAPI()

app.state.limiter = limiter 
app.add_middleware(SlowAPIMiddleware)


@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={
            "detail": "Too many requests. Please wait a moment before trying again."
        },
    )

# app.include_router(document_router)
app.include_router(answer_router)
app.include_router(ui_router)

Base.metadata.create_all(bind = engine )


@app.get("/health")
def health_check():
    return {"status": "ok"}