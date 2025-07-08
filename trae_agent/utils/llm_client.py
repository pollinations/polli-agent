# Copyright (c) 2025 ByteDance Ltd. and/or its affiliates
# SPDX-License-Identifier: MIT

"""LLM Client wrapper for OpenAI, Anthropic, Azure, and OpenRouter APIs."""

from enum import Enum

from ..tools.base import Tool
from .base_client import BaseLLMClient
from .config import ModelParameters
from .llm_basics import LLMMessage, LLMResponse
from .trajectory_recorder import TrajectoryRecorder


class LLMProvider(Enum):
    """Supported LLM providers."""

    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    AZURE = "azure"
    OLLAMA = "ollama"
    OPENROUTER = "openrouter"
    DOUBAO = "doubao"
    GOOGLE = "google"
    POLLINATIONS = "pollinations"
    # Individual Pollinations model providers
    POLLINATIONS_OPENAI = "pollinations-openai"
    POLLINATIONS_DEEPSEEK = "pollinations-deepseek"
    POLLINATIONS_DEEPSEEK_REASONING = "pollinations-deepseek-reasoning"
    POLLINATIONS_QWEN_CODER = "pollinations-qwen-coder"
    POLLINATIONS_MISTRAL = "pollinations-mistral"
    POLLINATIONS_OPENAI_LARGE = "pollinations-openai-large"
    POLLINATIONS_GROK = "pollinations-grok"
    POLLINATIONS_LLAMA_SCOUT = "pollinations-llama-scout"
    POLLINATIONS_OPENAI_FAST = "pollinations-openai-fast"
    POLLINATIONS_PHI = "pollinations-phi"


class LLMClient:
    """Main LLM client that supports multiple providers."""

    def __init__(self, provider: str | LLMProvider, model_parameters: ModelParameters):
        if isinstance(provider, str):
            provider = LLMProvider(provider)

        self.provider: LLMProvider = provider

        if provider == LLMProvider.OPENAI:
            from .openai_client import OpenAIClient

            self.client: BaseLLMClient = OpenAIClient(model_parameters)
        elif provider == LLMProvider.ANTHROPIC:
            from .anthropic_client import AnthropicClient

            self.client = AnthropicClient(model_parameters)
        elif provider == LLMProvider.AZURE:
            from .azure_client import AzureClient

            self.client = AzureClient(model_parameters)
        elif provider == LLMProvider.OPENROUTER:
            from .openrouter_client import OpenRouterClient

            self.client = OpenRouterClient(model_parameters)
        elif provider == LLMProvider.DOUBAO:
            from .doubao_client import DoubaoClient

            self.client = DoubaoClient(model_parameters)
        elif provider == LLMProvider.OLLAMA:
            from .ollama_client import OllamaClient

            self.client = OllamaClient(model_parameters)
        elif provider == LLMProvider.GOOGLE:
            from .google_client import GoogleClient

            self.client = GoogleClient(model_parameters)
        elif provider in [
            LLMProvider.POLLINATIONS,
            LLMProvider.POLLINATIONS_OPENAI,
            LLMProvider.POLLINATIONS_DEEPSEEK,
            LLMProvider.POLLINATIONS_DEEPSEEK_REASONING,
            LLMProvider.POLLINATIONS_QWEN_CODER,
            LLMProvider.POLLINATIONS_MISTRAL,
            LLMProvider.POLLINATIONS_OPENAI_LARGE,
            LLMProvider.POLLINATIONS_GROK,
            LLMProvider.POLLINATIONS_LLAMA_SCOUT,
            LLMProvider.POLLINATIONS_OPENAI_FAST,
            LLMProvider.POLLINATIONS_PHI,
        ]:
            from .pollinations_client import PollinationsClient

            self.client = PollinationsClient(model_parameters)
        else:
            raise ValueError(f"Unsupported provider: {provider}")

    def set_trajectory_recorder(self, recorder: TrajectoryRecorder | None) -> None:
        """Set the trajectory recorder for the underlying client."""
        self.client.set_trajectory_recorder(recorder)

    def set_chat_history(self, messages: list[LLMMessage]) -> None:
        """Set the chat history."""
        self.client.set_chat_history(messages)

    def chat(
        self,
        messages: list[LLMMessage],
        model_parameters: ModelParameters,
        tools: list[Tool] | None = None,
        reuse_history: bool = True,
    ) -> LLMResponse:
        """Send chat messages to the LLM."""
        return self.client.chat(messages, model_parameters, tools, reuse_history)

    def supports_tool_calling(self, model_parameters: ModelParameters) -> bool:
        """Check if the current client supports tool calling."""
        return hasattr(
            self.client, "supports_tool_calling"
        ) and self.client.supports_tool_calling(model_parameters)
