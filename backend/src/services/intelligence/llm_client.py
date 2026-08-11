import os
import requests

class LLMClient:
    def __init__(self):
        self.api_url = os.getenv('LLM_API_URL', 'http://localhost:8000/llm/generate')
        self.api_key = os.getenv('LLM_API_KEY', '')

    def generate_summary(self, prompt: str) -> str:
        headers = {'Authorization': f'Bearer {self.api_key}'} if self.api_key else {}
        response = requests.post(self.api_url, json={'prompt': prompt}, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get('summary', '')
