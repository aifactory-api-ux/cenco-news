from gtts import gTTS
from fastapi import HTTPException
import os
from backend.src.core.logging import get_logger

logger = get_logger("tts_service")

class TextToSpeechService:

    def __init__(self):
        pass

    def synthesize_text(self, text: str, lang: str = "es", output_path: str = "output.mp3") -> str:
        """Convierte texto en un archivo de audio MP3.

        Args:
            text (str): Texto a sintetizar.
            lang (str, optional): Código de idioma. Defaults a "es".
            output_path (str, optional): Ruta donde guardar el archivo MP3. Defaults a "output.mp3".

        Returns:
            str: Ruta del archivo de audio generado.

        Raises:
            HTTPException: Si la síntesis falla.
        """
        try:
            tts = gTTS(text=text, lang=lang)
            tts.save(output_path)
            logger.info("Texto sintetizado a audio", text=text, output_path=output_path)
            return output_path
        except Exception as e:
            logger.error(f"Error en el servicio de texto a voz: {e}", text=text)
            raise HTTPException(status_code=503, detail="Servicio de texto a voz no disponible")
