from fastapi import APIRouter, Depends
from agents_project.skyflow_agent.main import main, Agent, Runner, set_tracing_disabled, set_default_openai_api,  set_default_openai_client
from pydantic import BaseModel
import json
from agents_project.skyflow_agent.main import mock_flights  
from auth.deps import get_current_user


router = APIRouter(prefix="/agent", tags=["Flight Agent"])

# Request body schema
class FlightQuery(BaseModel):
    prompt: str

@router.post("/airline-agent")
async def airline_agent(query: FlightQuery, current_user: str = Depends(get_current_user)):
    # Define agent on each call (to allow async reusability and fresh state)
    agent = Agent(
        name="Flight_Assistant",
        instructions=(
            "You are a flight booking assistant. "
            "You will help users find flights based on their preferences. "
            "Use the mock_flights list below to determine the best match.\n\n"
            f"{json.dumps(mock_flights, indent=2)}\n\n"
            "If no suitable match exists, respond with 'No flights found matching your criteria.'"
        ),
        model="llama-3.3-70b-versatile",
    )

    # Run the agent with the input
    result = await Runner.run(agent, input=query.prompt, max_turns=10)

    return {"result": result.final_output}






