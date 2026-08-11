import re
from langdetect import detect


def normalize_content(content: str) -> str:
    # Remove HTML tags
    text = re.sub(r'<[^>]*>', '', content)
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def detect_language(text: str) -> str:
    try:
        lang = detect(text)
        return lang
    except Exception:
        return 'unknown'
