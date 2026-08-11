import speech_recognition as sr
from fastapi import HTTPException
from backend.src.core.logging import get_logger

logger = get_logger("stt_service")

class SpeechToTextService:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def recognize_audio(self, audio_file_path: str) -> str:
        """Reconoce el texto en un archivo de audio.

        Args:
            audio_file_path (str): Ruta al archivo de audio.

        Returns:
            str: Texto reconocido.

        Raises:
            HTTPException: Si el reconocimiento falla.
        """
        try:
            with sr.AudioFile(audio_file_path) as source:
                audio = self.recognizer.record(source)
            # Usar Google Speech Recognition como motor STT
            text = self.recognizer.recognize_google(audio, language="es-ES")
            logger.info("Audio reconocido correctamente", audio_file=audio_file_path, text=text)
            return text
        except sr.UnknownValueError:
            logger.error("No se pudo entender el audio", audio_file=audio_file_path)
            raise HTTPException(status_code=400, detail="No se pudo entender el audio")
        except sr.RequestError as e:
            logger.error(f"Error en el servicio de reconocimiento de voz: {e}", audio_file=audio_file_path)
            raise HTTPException(status_code=503, detail="Servicio de reconocimiento de voz no disponible")
