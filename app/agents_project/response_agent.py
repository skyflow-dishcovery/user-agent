from fastapi import APIRouter, Form, Depends
from auth.deps import get_current_user
from agents_project.input_agent.utils import llama_query
from utils.history import fetch_user_history
from utils.db_store import update_user_history
from utils.location import get_location_from_coords

router = APIRouter(prefix="/agent", tags=["Response Agent"])

@router.post("/response")
async def generate_response(
    user_id: str = Form(...),
    refined_input: str = Form(...),
    intent: str = Form(...),
    latitude: float = Form(...),
    longitude: float = Form(...),
    current_user: str = Depends(get_current_user)
):
    try:
        location = get_location_from_coords(latitude, longitude)

        # 1. Fetch user history
        history = fetch_user_history(user_id)

        # 2. Construct prompt
        prompt = f"""
You are an intelligent travel & food assistant.

User is currently in: {location}
User intent: {intent}
Refined user input: "{refined_input}"

Respond in a helpful and friendly tone. Suggest relevant actions or info.
"""
        response = llama_query(prompt)

        # 3. Optional: update history
        update_user_history(user_id, f"{intent.upper()} AGENT: {response}")

        return {
            "user_id": user_id,
            "response": response,
            "status": "success"
        }
    except Exception as e:
        return {"error": str(e), "status": "failed"}
