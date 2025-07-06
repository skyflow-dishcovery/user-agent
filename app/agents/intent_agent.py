from fastapi import APIRouter, Depends, HTTPException, Form
from pydantic import BaseModel
from auth.deps import get_current_user
from agents.input_agent.utils import llama_query
from utils.history import fetch_user_history
from utils.db_store import update_user_history

router = APIRouter(prefix="/agent", tags=["Intent Agent"])

class IntentRequest(BaseModel):
    text: str
    user_id: str

@router.post("/intent")
async def classify_intent(text: str = Form(...), user_id: str = Form(...), current_user: str = Depends(get_current_user)):
    try:
        history = fetch_user_history(user_id)

        # Step 1: Classify intent
        prompt = f"""
You are an AI that helps route travel and food-related requests.

User message: "{text}"

User history: "{history}"

Based on this, is the user asking about:
1. Food ordering (Dishcovery)
2. Travel booking (SkyFlow)

Respond with only "dishcovery" or "skyflow".
"""
        intent = llama_query(prompt).strip().lower()

        # Step 2: Regenerate refined input
        regen_prompt = f"""
Rewrite the user's message: "{text}" into a clearer version suitable for an AI assistant, 
based on this history: {history}. Respond with only rewritten message.
"""
        refined_input = llama_query(regen_prompt).strip()

        update_user_history(user_id, refined_input)

        return {
            "user_id": user_id,
            "intent": intent,
            "refined_input": refined_input,
            "status": "success"
        }
    except Exception as e:
        return {"error": str(e), "status": "failed"}
