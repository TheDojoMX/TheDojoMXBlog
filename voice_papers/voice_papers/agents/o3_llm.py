"""Custom LLM wrapper for o3 model compatibility."""

from typing import Any, Dict, List, Optional
from crewai.llm import LLM
from openai import OpenAI
import os


class O3LLM(LLM):
    """Custom LLM wrapper for o3 model that filters unsupported parameters."""

    def __init__(self, api_key: str, model: str = "o3-mini"):
        self.client = OpenAI(api_key=api_key)
        self.model = model
        # Initialize parent class without parameters that o3 doesn't support
        super().__init__(model=model, api_key=api_key)

    def call(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Call the o3 model with filtered parameters."""
        # Filter out unsupported parameters for o3
        supported_params = {"model": self.model, "messages": messages}

        # Only add supported parameters that o3 accepts
        if "max_tokens" in kwargs and kwargs["max_tokens"] is not None:
            supported_params["max_tokens"] = kwargs["max_tokens"]

        # o3 doesn't support: temperature, stop, top_p, frequency_penalty, presence_penalty
        # Remove these if they exist in kwargs
        unsupported_params = [
            "temperature",
            "stop",
            "top_p",
            "frequency_penalty",
            "presence_penalty",
        ]

        try:
            response = self.client.chat.completions.create(**supported_params)
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"O3 LLM call failed: {e}")

    def __call__(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Make the object callable."""
        return self.call(messages, **kwargs)
