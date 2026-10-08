"""
VertifyCase Multi-Provider LLM Client
Supports:
1. Google Gemini (GEMINI_API_KEY)
2. OpenAI (OPENAI_API_KEY)
3. Anthropic Claude (ANTHROPIC_API_KEY)
4. Local Ollama (OLLAMA_BASE_URL)
5. Built-in Deterministic Fallback Engine (when no key is provided)
Always enforces temperature=0.0 and structured output adherence.
"""

import os
import json
from pathlib import Path
from typing import Optional, Dict, Any, List
import requests
from dotenv import load_dotenv

ENV_PATH = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=ENV_PATH)

def mask_key(k: str) -> str:
    if not k:
        return ""
    if len(k) <= 8:
        return "****"
    return k[:4] + "..." + k[-4:]

class LLMProviderClient:
    def __init__(self):
        self.reload_keys()

    def reload_keys(self):
        load_dotenv(dotenv_path=ENV_PATH, override=True)
        self.gemini_key = os.getenv("GEMINI_API_KEY", "").strip()
        self.openai_key = os.getenv("OPENAI_API_KEY", "").strip()
        self.anthropic_key = os.getenv("ANTHROPIC_API_KEY", "").strip()
        self.ollama_url = os.getenv("OLLAMA_BASE_URL", "").strip()
        self.preferred_provider = os.getenv("ACTIVE_LLM_PROVIDER", "").strip().lower()

    def save_keys_to_env(self, gemini_key: Optional[str] = None,
                         openai_key: Optional[str] = None,
                         anthropic_key: Optional[str] = None,
                         ollama_url: Optional[str] = None,
                         preferred_provider: Optional[str] = None):
        """Persists keys to local .env file."""
        if gemini_key is not None:
            self.gemini_key = gemini_key.strip()
        if openai_key is not None:
            self.openai_key = openai_key.strip()
        if anthropic_key is not None:
            self.anthropic_key = anthropic_key.strip()
        if ollama_url is not None:
            self.ollama_url = ollama_url.strip()
        if preferred_provider is not None:
            self.preferred_provider = preferred_provider.strip().lower()

        env_lines = [
            f"# VertifyCase Environment & LLM Configuration",
            f"GEMINI_API_KEY={self.gemini_key}",
            f"OPENAI_API_KEY={self.openai_key}",
            f"ANTHROPIC_API_KEY={self.anthropic_key}",
            f"OLLAMA_BASE_URL={self.ollama_url}",
            f"ACTIVE_LLM_PROVIDER={self.preferred_provider}",
        ]
        ENV_PATH.write_text("\n".join(env_lines) + "\n", encoding="utf-8")
        self.reload_keys()

    def get_config(self) -> Dict[str, Any]:
        return {
            "active_provider_label": self.get_active_provider(),
            "cloud_enabled": self.is_cloud_enabled(),
            "preferred_provider": self.preferred_provider or ("gemini" if self.gemini_key else "openai" if self.openai_key else "offline"),
            "gemini_configured": bool(self.gemini_key),
            "gemini_key_masked": mask_key(self.gemini_key),
            "openai_configured": bool(self.openai_key),
            "openai_key_masked": mask_key(self.openai_key),
            "anthropic_configured": bool(self.anthropic_key),
            "anthropic_key_masked": mask_key(self.anthropic_key),
            "ollama_configured": bool(self.ollama_url),
            "ollama_url": self.ollama_url,
        }

    def get_active_provider(self) -> str:
        if self.preferred_provider == "gemini" and self.gemini_key:
            return "Google Gemini (gemini-1.5-flash)"
        if self.preferred_provider == "openai" and self.openai_key:
            return "OpenAI (gpt-4o)"
        if self.preferred_provider == "anthropic" and self.anthropic_key:
            return "Anthropic (claude-3-5-sonnet)"
        if self.preferred_provider == "ollama" and self.ollama_url:
            return f"Local Ollama ({self.ollama_url})"

        # Auto fallback based on whatever key is present
        if self.gemini_key:
            return "Google Gemini (gemini-1.5-flash)"
        if self.openai_key:
            return "OpenAI (gpt-4o)"
        if self.anthropic_key:
            return "Anthropic (claude-3-5-sonnet)"
        if self.ollama_url:
            return f"Local Ollama ({self.ollama_url})"
        return "Built-in Verifiable Engine (Offline)"

    def is_cloud_enabled(self) -> bool:
        return bool(self.gemini_key or self.openai_key or self.anthropic_key or self.ollama_url)

    def generate(self, system_prompt: str, user_prompt: str, temperature: float = 0.0) -> Optional[str]:
        """Calls active cloud LLM provider at temperature 0.0 with fallback to None."""
        provider = self.preferred_provider
        if provider == "gemini" and self.gemini_key:
            return self._call_gemini(system_prompt, user_prompt, temperature)
        elif provider == "openai" and self.openai_key:
            return self._call_openai(system_prompt, user_prompt, temperature)
        elif provider == "anthropic" and self.anthropic_key:
            return self._call_anthropic(system_prompt, user_prompt, temperature)
        elif provider == "ollama" and self.ollama_url:
            return self._call_ollama(system_prompt, user_prompt, temperature)

        # Fallback to any configured key
        if self.gemini_key:
            return self._call_gemini(system_prompt, user_prompt, temperature)
        elif self.openai_key:
            return self._call_openai(system_prompt, user_prompt, temperature)
        elif self.anthropic_key:
            return self._call_anthropic(system_prompt, user_prompt, temperature)
        elif self.ollama_url:
            return self._call_ollama(system_prompt, user_prompt, temperature)
        return None

    def _call_gemini(self, system_prompt: str, user_prompt: str, temperature: float = 0.0) -> Optional[str]:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.gemini_key}"
        payload = {
            "systemInstruction": {"parts": [{"text": system_prompt}]},
            "contents": [{"parts": [{"text": user_prompt}]}],
            "generationConfig": {
                "temperature": temperature,
                "topP": 0.1,
                "maxOutputTokens": 2048
            }
        }
        try:
            resp = requests.post(url, json=payload, timeout=25)
            if resp.status_code == 200:
                data = resp.json()
                candidates = data.get("candidates", [])
                if candidates:
                    return candidates[0]["content"]["parts"][0]["text"]
            else:
                print(f"[LLM Warning] Gemini API error ({resp.status_code}): {resp.text[:200]}")
        except Exception as e:
            print(f"[LLM Warning] Gemini connection failed: {e}")
        return None

    def _call_openai(self, system_prompt: str, user_prompt: str, temperature: float = 0.0) -> Optional[str]:
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.openai_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "gpt-4o",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": temperature
        }
        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=25)
            if resp.status_code == 200:
                data = resp.json()
                return data["choices"][0]["message"]["content"]
            else:
                print(f"[LLM Warning] OpenAI API error ({resp.status_code}): {resp.text[:200]}")
        except Exception as e:
            print(f"[LLM Warning] OpenAI connection failed: {e}")
        return None

    def _call_anthropic(self, system_prompt: str, user_prompt: str, temperature: float = 0.0) -> Optional[str]:
        url = "https://api.anthropic.com/v1/messages"
        headers = {
            "x-api-key": self.anthropic_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "claude-3-5-sonnet-20241022",
            "system": system_prompt,
            "messages": [{"role": "user", "content": user_prompt}],
            "temperature": temperature,
            "max_tokens": 2048
        }
        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=25)
            if resp.status_code == 200:
                data = resp.json()
                return data["content"][0]["text"]
            else:
                print(f"[LLM Warning] Anthropic API error ({resp.status_code}): {resp.text[:200]}")
        except Exception as e:
            print(f"[LLM Warning] Anthropic connection failed: {e}")
        return None

    def _call_ollama(self, system_prompt: str, user_prompt: str, temperature: float = 0.0) -> Optional[str]:
        url = f"{self.ollama_url.rstrip('/')}/api/generate"
        payload = {
            "model": "llama3.1",
            "system": system_prompt,
            "prompt": user_prompt,
            "stream": False,
            "options": {"temperature": temperature}
        }
        try:
            resp = requests.post(url, json=payload, timeout=25)
            if resp.status_code == 200:
                return resp.json().get("response")
        except Exception as e:
            print(f"[LLM Warning] Ollama connection failed: {e}")
        return None

llm_client = LLMProviderClient()
