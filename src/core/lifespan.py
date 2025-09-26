from typing import AsyncGenerator, Any

from fastapi import FastAPI
from contextlib import asynccontextmanager

from core import db_helper


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, Any]:
    yield
    await db_helper.dispose()
