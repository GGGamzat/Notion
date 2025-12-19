from fastapi import FastAPI
from app.router.user import auth_router

app = FastAPI()
app.include_router(auth_router, tags=["Users"])