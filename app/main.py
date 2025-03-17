from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.database import create_tables, delete_tables
from app.routes import router as projects_router

@asynccontextmanager
async def lifespan(app: FastAPI):
   await create_tables()
   print("Database created")
   yield
   await delete_tables()
   print("Database deleted")

app = FastAPI(lifespan=lifespan)
app.include_router(projects_router)