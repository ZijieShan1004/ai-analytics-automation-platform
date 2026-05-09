import httpx

from app.core.config import get_settings

settings = get_settings()


class OllamaClient:
    def __init__(self):
        self.base_url = settings.ollama_base_url
        self.model = settings.ollama_model
        self.timeout = settings.ollama_timeout_seconds

    # Generate text using the local Ollama model.
    def generate(self, prompt: str) -> str:
        url = f"{self.base_url}/api/generate"
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
        }

        try:
            response = httpx.post(url, json=payload, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()
            return data.get("response", "").strip()
        except Exception:
            return "The local LLM summary service is unavailable. The analytics pipeline completed, but the natural-language summary could not be generated."