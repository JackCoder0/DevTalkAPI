from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.api import api_router

app = FastAPI(
    title="DevTalk API",
    description="API para o projeto da Faculdade Anhanguera",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
