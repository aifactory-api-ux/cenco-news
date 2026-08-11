from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from fastapi.responses import FileResponse, JSONResponse
from uuid import uuid4
import os
from backend.src.services.voice.stt_service import SpeechToTextService
from backend.src.services.voice.tts_service import TextToSpeechService
from backend.src.services.voice.query_processor import VoiceQueryProcessor
from backend.src.core.logging import get_logger

router = APIRouter(prefix="/voice", tags=["Voice"])

stt_service = SpeechToTextService()
tts_service = TextToSpeechService()
query_processor = VoiceQueryProcessor()

logger = get_logger("voice_router")

@router.post("/query")
async def voice_query(audio: UploadFile = File(...)):
    # Guardar archivo temporal
    temp_filename = f"/tmp/{uuid4()}.wav"
    try:
        content = await audio.read()
        with open(temp_filename, "wb") as f:
            f.write(content)

        # Reconocer texto de audio
        text = stt_service.recognize_audio(temp_filename)

        # Procesar consulta
        response_text = await query_processor.process_query(text)
        return JSONResponse(content={"response": response_text})
    finally:
        if os.path.exists(temp_filename):
            os.remove(temp_filename)


@router.post("/speak")
async def voice_speak(text: str = Form(...), lang: str = Form("es")):
    output_path = f"/tmp/{uuid4()}.mp3"
    try:
        audio_path = tts_service.synthesize_text(text, lang, output_path)
        return FileResponse(audio_path, media_type="audio/mpeg", filename="speech.mp3")
    except HTTPException as e:
        raise e
    finally:
        # Clean up is handled by client or needs other strategy if ephemeral storage
        pass
