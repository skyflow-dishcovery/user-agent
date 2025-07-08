from fastapi import APIRouter, Depends
from agents_project.hotel_agent.main import main, Agent, Runner, set_tracing_disabled, set_default_openai_api,  set_default_openai_client
from pydantic import BaseModel
import json
from agents_project.hotel_agent.main import mock_hotels  
from auth.deps import get_current_user


router = APIRouter(prefix="/agent", tags=["Hotel Agent"])

# Request body schema
class HotelQuery(BaseModel):
    prompt: str

@router.post("/hotel-agent")
async def airline_agent(query: HotelQuery, current_user: str = Depends(get_current_user)):
    # Define agent on each call (to allow async reusability and fresh state)
    agent = Agent(
        name="Hotel_Assistant",
        instructions=(
            "You are a hotel booking assistant. "
            "You will help users find hotels based on their preferences. "
            "Use the mock_hotels list below to determine the best match.\n\n"
            f"{json.dumps(mock_hotels, indent=2)}\n\n"
            "If no suitable match exists, respond with 'No hotels found matching your criteria.'"
        ),
        model="llama-3.3-70b-versatile",
    )

    # Run the agent with the input
    result = await Runner.run(agent, input=query.prompt, max_turns=10)

    return {"result": result.final_output}






