from fastapi import FastAPI
from auth.auth_router import router as auth_router
from database import Base, engine
from agents_project.input_agent.main import router as input_agent_router
from agents_project.intent_agent import router as intent_agent_router
from agents_project.response_agent import router as response_agent_router
from agents_project.skyflow_agent.api import router as skyflow_agent_router
from agents_project.restaurant_agent.api import router as restaurant_agent_router
from agents_project.hotel_agent.api import router as hotel_agent_router
from agents_project.multi_agent_router import router as multi_agent_router


app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)

# Routes
app.include_router(auth_router)
app.include_router(input_agent_router)
app.include_router(intent_agent_router)
app.include_router(response_agent_router)
app.include_router(skyflow_agent_router)
app.include_router(restaurant_agent_router)
app.include_router(hotel_agent_router)
app.include_router(multi_agent_router)



