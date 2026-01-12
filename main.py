from fastapi import FastAPI
from source.databases.db import Base, engine
from fastapi.middleware.cors import CORSMiddleware
from source.models.models import User, Question, Answer, Score, DiagnosisResult, Assesment, Rule, Admin
from source.controllers import forward_chainning, admin_controllers, auth

app = FastAPI(
    title="Mental Health Disease Detection",
    description="API for Mental Health Disease Detection",
    version="1.0.0"
)

origins = [
    "http://localhost:5173",   
    "http://localhost:3000",  
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

routing = [
    forward_chainning,
    admin_controllers,
    auth
]

for route in routing:
    app.include_router(route.router)

