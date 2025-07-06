from pydantic import BaseModel
from typing import Optional

class TextInput(BaseModel):
    user_id: str
    text: str

class VoiceInput(BaseModel):
    user_id: str