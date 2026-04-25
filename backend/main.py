from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.jobs.scheduler import scheduler
from app.api.routes import router
from app.db.db import init_db
import os
import logging

origins = [o.strip() for o in os.getenv("ALLOWED_ORIGINS", "").split(",") if o.strip()]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing Database...")
    init_db()
    logger.info("Database initialized!")
    scheduler.start()
    logger.info("Scheduler started!")
    yield
    scheduler.shutdown()
    logger.info("Scheduler shut down!")

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)