import os
import shutil
import uuid
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status
from backend.app.auth.dependencies import get_current_user
from backend.app.models.user import User
from ai.speech.transcriber import SpeechTranscriber

router = APIRouter()
transcriber = SpeechTranscriber()

AUDIO_UPLOAD_DIR = "data/audio"
os.makedirs(AUDIO_UPLOAD_DIR, exist_ok=True)

@router.post("/transcribe", status_code=status.HTTP_200_OK)
async def transcribe_audio_endpoint(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    """
    Accepts an audio file upload (wav, mp3, m4a, etc.), saves it temporarily, 
    and returns the transcribed text.
    """
    allowed_extensions = [".wav", ".mp3", ".m4a", ".ogg", ".webm", ".flac"]
    _, ext = os.path.splitext(file.filename)
    if ext.lower() not in allowed_extensions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported audio format. Allowed formats: {', '.join(allowed_extensions)}"
        )

    # Save audio file
    file_id = str(uuid.uuid4())
    file_path = os.path.join(AUDIO_UPLOAD_DIR, f"{file_id}{ext.lower()}")
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save audio file: {e}")

    # Transcribe audio
    transcript = transcriber.transcribe_audio(file_path)

    # Optional: cleanup audio file to save space after transcription
    if os.path.exists(file_path):
        os.remove(file_path)

    if "[Transcription failed.]" in transcript:
        raise HTTPException(status_code=500, detail="Audio transcription failed.")

    return {
        "text": transcript
    }
