from fastapi import APIRouter, UploadFile, File, Form, Depends
from .utils import translate_audio, translate_text
from auth.deps import get_current_user

router = APIRouter(prefix="/agent", tags=["Input Agent"])

@router.post("/voice")
async def handle_voice_input(file: UploadFile = File(...), current_user: str = Depends(get_current_user)):
    try:
        contents = await file.read()

        with open("./agents/input_agent/temp_audio.wav", "wb") as f:
            f.write(contents)

        english_text = translate_audio("./agents/input_agent/temp_audio.wav")
        return {
            "user_id": current_user["id"],
            "text": english_text,
            "status": "success"
        }
    except Exception as e:
        return {"error": str(e), "status": "failed"}

@router.post("/text")
async def handle_text_input(text: str = Form(...), current_user: str = Depends(get_current_user)):
    try:
        english_text = translate_text(text)
        return {
            "user_id": current_user["id"],
            "text": english_text,
            "status": "success"
        }
    except Exception as e:
        return {"error": str(e), "status": "failed"}
