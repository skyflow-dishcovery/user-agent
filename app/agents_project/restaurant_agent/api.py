from fastapi import APIRouter, Depends
from agents_project.restaurant_agent.main import main, Agent, Runner, set_tracing_disabled, set_default_openai_api,  set_default_openai_client
from pydantic import BaseModel
import json
from agents_project.restaurant_agent.main import mock_restaurants  
from auth.deps import get_current_user


router = APIRouter(prefix="/agent", tags=["Restaurant Agent"])

# Request body schema
class RestaurantQuery(BaseModel):
    prompt: str

@router.post("/restaurant-agent")
async def restaurant_agent(query: RestaurantQuery, current_user: str = Depends(get_current_user)):
    # Define agent on each call (to allow async reusability and fresh state)
    agent = Agent(
        name="Restaurant_Assistant",
        instructions=(
            "You are a Restaurant assistant. "
            "You will help users find their desired dishes based on their preferences. "
            "Use the mock_restaurants list below to determine the best match.\n\n"
            f"{json.dumps(mock_restaurants, indent=2)}\n\n"
            "If no suitable match exists, respond with 'No Restaurants have food that matches your criteria.'"
        ),
        model="llama-3.3-70b-versatile",
    )

    # Run the agent with the input
    result = await Runner.run(agent, input=query.prompt, max_turns=10)

    return {"result": result.final_output}






