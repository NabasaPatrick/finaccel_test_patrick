import logging
import time
import traceback

from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from src.core.database import Base
from src.modules.router import router

app_name = "Test Finaccel"
db_url = "postgresql://postgres:admin@db:5432/finaccel_test_patrick"

logger = logging.getLogger(__name__)
app = FastAPI(
    title=app_name,
    openapi_url="/openapi.json",
    docs_url="/docs"
)
app.add_middleware(
    DBSessionMiddleware,
    db_url=db_url,
    engine_args=dict(pool_pre_ping=True)
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)

@app.middleware("http")
async def add_http_middleware(request: Request, call_next):
    start_time = time.time()
    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response
    except:
        msg = traceback.format_exc()
        logger.error(msg)

    return JSONResponse({
        'success': False,
        'message': 'Internal Server Error',
        'description': 'This error has been reported to the System Administrator'
    }, status_code=500)
