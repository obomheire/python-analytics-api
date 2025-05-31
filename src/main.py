from contextlib import asynccontextmanager
from typing import Union

from fastapi import FastAPI, Header, status
from server.db_session import init_db
from events import router as event_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # before app startup up
    print("Server is starting...")
    init_db()
    yield
    # clean up
    print("Server is shutting down...")
    
app = FastAPI(lifespan=lifespan)
app.include_router(event_router, prefix='/api/events')
# /api/events

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


# GET /get_headers (get headers)
@app.get("/get_headers", status_code=status.HTTP_200_OK)
async def get_headers(
    accept: str = Header(None),
    content_type: str = Header(None),
    user_agent: str = Header(None),
    host: str = Header(None),
):
    request_headers = {}
    request_headers["Accept"] = accept
    request_headers["Content-Type"] = content_type
    request_headers["User-Agent"] = user_agent
    request_headers["Host"] = host
    return request_headers


@app.get("/healthz")
def read_api_health():
    return {"status": "ok"}
