from fastapi import APIRouter, UploadFile, File, Form, Depends, Request
import requests
from auth.deps import get_current_user
import httpx


router = APIRouter(prefix="/agent", tags=["Multi-Agent Flow"])

BASE_URL = "http://127.0.0.1:8000"  # Adjust if deployed elsewhere

@router.post("/process")
async def full_agent_flow(request: Request, file: UploadFile = File(None), text: str = Form(None), current_user: str = Depends(get_current_user)):
    try:
        token = request.headers.get("authorization")
        headers = {"Authorization": token}

        async with httpx.AsyncClient() as client:
            # -------- Step 1: Input Agent --------
            if file:
                input_resp = await client.post(
                    f"{BASE_URL}/agent/voice",
                    files=file,
                    headers=headers
                )

            elif text:
                input_resp = await client.post(
                    f"{BASE_URL}/agent/text",
                    data={"text": text},
                    headers=headers
                )
            else:
                return {"status": "failed", "error": "No input provided."}

        input_data = input_resp.json()
        english_text = input_data["text"]
        user_id = input_data["user_id"]

        # # -------- Step 2: Intent Agent --------
        async with httpx.AsyncClient() as client:
            intent_resp = await client.post(
                f"{BASE_URL}/agent/intent",
                data={"text": english_text, "user_id": user_id},
                headers=headers  # Add real JWT if auth enforced
            )

        intent_data = intent_resp.json()
        intent = intent_data["intent"]
        refined_input = intent_data["refined_input"]

        # # # -------- Step 3: Response Agent --------
        # # response_resp = requests.post(
        # #     f"{BASE_URL}/agent/response",
        # #     data={
        # #         "text": refined_input,
        # #         "intent": intent,
        # #         "user_id": user_id,
        # #         "lat": "24.8607",  # Optional, pass if coming from frontend
        # #         "lon": "67.0011"
        # #     }
        # # )
        # # final_output = response_resp.json()

        # # -------- Step 4: Call Service Agent --------
        async with httpx.AsyncClient() as client:
            if intent == "dishcovery":
                service_resp = await client.post(f"{BASE_URL}/agent/restaurant-agent", json={"prompt": refined_input}, headers=headers)
            elif intent == "skyflow":
                service_resp = await client.post(f"{BASE_URL}/agent/airline-agent", json={"prompt": refined_input}, headers=headers)
            elif intent == "hotel":
                service_resp = await client.post(f"{BASE_URL}/agent/hotel-agent", json={"prompt": refined_input}, headers=headers)
            else:
                return {"status": "failed", "error": "Unknown intent."}

        service_data = service_resp.json()

        return {
            "status": "success",
            "user_id": user_id,
            "intent": intent,
            "refined_input": refined_input,
            "agent_response": service_data
        }

    except Exception as e:
        return {"status": "failed", "error": str(e)}
