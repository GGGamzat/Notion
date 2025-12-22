from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.router.user import auth_router
from app.router.task import task_router

app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# CORS для React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Можно заменить на конкретный домен позже
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, tags=["Users"])
app.include_router(task_router, tags=["Tasks"])