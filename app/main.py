from fastapi import FastAPI
from auth.auth_router import router as auth_router
from database import Base, engine
from agents.input_agent.main import router as input_agent_router
from agents.intent_agent import router as intent_agent_router
from agents.response_agent import router as response_agent_router

app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)

# Routes
app.include_router(auth_router)
app.include_router(input_agent_router)
app.include_router(intent_agent_router)
app.include_router(response_agent_router)


