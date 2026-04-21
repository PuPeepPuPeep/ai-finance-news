from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.jobs.scheduler import scheduler
from app.api.routes import router
import os
import logging

origins = os.getenv("ALLOWED_ORIGINS", "").split(",")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
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