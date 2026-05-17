import requests
from rich.console import Console
from dataclasses import dataclass, field
from typing import Any

@dataclass
class Agent:
    model: str = "qwen3.5-0.8b"
    base_url: str = "http://127.0.0.1:1234/v1"
    api_key: str = field(default="", repr=False)
    messages: list[dict[str, Any]] = field(default_factory=list)
    
    def __post_init__(self) -> None:
        self.base_url = self.base_url.rstrip("/")
        
    def chat(self, user_message: str) -> str:
        self.messages.append({"role": "user", "content": user_message})
        
        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        
        r = requests.post(
            url,
            headers=headers,
            json={"model": self.model, "messages": self.messages},
            timeout=600,
        )
        r.raise_for_status()
        data = r.json()
        choices = data.get("choices")
        
        if not choices:
            raise RuntimeError("Model response missing choices")
        
        message = choices[0].get("message")
        if message is None:
            raise RuntimeError("Model response missing message")
        
        response = message.get("content") or ""
        self.messages.append({"role": "assistant", "content": response})
        return response
    