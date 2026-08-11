import httpx
import speech_recognition as sr
from typing import List, Dict, Any
from datetime import datetime
import io

class AudioCollector:
    async def collect(self, source_config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Collect articles by performing speech-to-text on audio"""
        url = source_config.get('url')
        if not url:
            raise ValueError("Audio source config missing 'url'")

        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(url)
            response.raise_for_status()
            audio_bytes = response.content

        recognizer = sr.Recognizer()
        audio_file = sr.AudioFile(io.BytesIO(audio_bytes))

        with audio_file as source:
            audio_data = recognizer.record(source)

        try:
            text = recognizer.recognize_google(audio_data, language=source_config.get('language', 'en-US'))
        except sr.UnknownValueError:
            text = ""
        except sr.RequestError as e:
            raise RuntimeError(f"Speech recognition error: {e}")

        article = {
            'url': url,
            'title': source_config.get('title', 'Audio Transcript'),
            'content': text,
            'summary': text[:500],
            'author': source_config.get('author', None),
            'published_at': source_config.get('published_at', datetime.utcnow())
        }

        return [article]
