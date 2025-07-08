# Copyright (c) 2025 ByteDance Ltd. and/or its affiliates
# SPDX-License-Identifier: MIT

"""Pollinations API client wrapper with tool integration."""

import json
import os
import random
import time
from typing import override

import openai
from openai.types.chat import (
    ChatCompletionAssistantMessageParam,
    ChatCompletionFunctionMessageParam,
    ChatCompletionMessageParam,
    ChatCompletionMessageToolCallParam,
    ChatCompletionSystemMessageParam,
    ChatCompletionToolParam,
    ChatCompletionUserMessageParam,
)
from openai.types.chat.chat_completion_message_tool_call_param import Function
from openai.types.chat.chat_completion_tool_message_param import (
    ChatCompletionToolMessageParam,
)
from openai.types.shared_params.function_definition import FunctionDefinition

from ..tools.base import Tool, ToolCall, ToolResult
from ..utils.config import ModelParameters
from .base_client import BaseLLMClient
from .llm_basics import LLMMessage, LLMResponse, LLMUsage


class PollinationsClient(BaseLLMClient):
    """Pollinations client wrapper with tool schema generation."""

    def __init__(self, model_parameters: ModelParameters):
        super().__init__(model_parameters)

        # Pollinations API doesn't require an API key for basic usage
        # But we can support optional API key for authenticated requests
        if self.api_key == "":
            self.api_key: str = os.getenv("POLLINATIONS_API_KEY", "")

        # Set the base URL to Pollinations OpenAI-compatible API
        if self.base_url is None or self.base_url == "":
            self.base_url = "https://text.pollinations.ai/openai/v1"

        self.client: openai.OpenAI = openai.OpenAI(
            api_key=self.api_key or "dummy-key",  # Pollinations doesn't require auth
            base_url=self.base_url,
        )
        self.message_history: list[ChatCompletionMessageParam] = []

    @override
    def set_chat_history(self, messages: list[LLMMessage]) -> None:
        """Set the chat history."""
        self.message_history = self.parse_messages(messages)

    @override
    def chat(
        self,
        messages: list[LLMMessage],
        model_parameters: ModelParameters,
        tools: list[Tool] | None = None,
        reuse_history: bool = True,
    ) -> LLMResponse:
        """Send chat messages to Pollinations with optional tool support."""
        openai_messages: list[ChatCompletionMessageParam] = self.parse_messages(messages)

        tool_schemas = None
        if tools:
            tool_schemas = [
                ChatCompletionToolParam(
                    function=FunctionDefinition(
                        name=tool.name,
                        description=tool.description,
                        parameters=tool.get_input_schema(),
                    ),
                    type="function",
                )
                for tool in tools
            ]

        api_call_input: list[ChatCompletionMessageParam] = []
        if reuse_history:
            api_call_input.extend(self.message_history)
        api_call_input.extend(openai_messages)

        response = None
        error_message = ""
        for i in range(model_parameters.max_retries):
            try:
                response = self.client.chat.completions.create(
                    messages=api_call_input,
                    model=model_parameters.model,
                    tools=tool_schemas if tool_schemas else openai.NOT_GIVEN,
                    temperature=model_parameters.temperature,
                    top_p=model_parameters.top_p,
                    max_tokens=model_parameters.max_tokens,
                )
                break
            except Exception as e:
                error_message += f"Error {i + 1}: {str(e)}\n"
                # Randomly sleep for 3-30 seconds
                time.sleep(random.randint(3, 30))
                continue

        if response is None:
            raise ValueError(
                f"Failed to get response from Pollinations after max retries: {error_message}"
            )

        # Update message history
        self.message_history = api_call_input
        if response.choices and response.choices[0].message:
            self.message_history.append(response.choices[0].message)

        content = ""
        tool_calls: list[ToolCall] = []
        
        if response.choices and response.choices[0].message:
            message = response.choices[0].message
            content = message.content or ""
            
            if message.tool_calls:
                for tool_call in message.tool_calls:
                    tool_calls.append(
                        ToolCall(
                            call_id=tool_call.id,
                            name=tool_call.function.name,
                            arguments=json.loads(tool_call.function.arguments)
                            if tool_call.function.arguments
                            else {},
                            id=tool_call.id,
                        )
                    )

        usage = None
        if response.usage:
            usage = LLMUsage(
                input_tokens=response.usage.prompt_tokens,
                output_tokens=response.usage.completion_tokens,
                cache_read_input_tokens=0,  # Pollinations doesn't provide cache info
                reasoning_tokens=0,  # Pollinations doesn't provide reasoning tokens
            )

        llm_response = LLMResponse(
            content=content,
            usage=usage,
            model=response.model or model_parameters.model,
            finish_reason=response.choices[0].finish_reason if response.choices else "stop",
            tool_calls=tool_calls if len(tool_calls) > 0 else None,
        )

        # Record trajectory if recorder is available
        if self.trajectory_recorder:
            self.trajectory_recorder.record_llm_interaction(
                messages=messages,
                response=llm_response,
                provider="pollinations",
                model=model_parameters.model,
                tools=tools,
            )

        return llm_response

    @override
    def supports_tool_calling(self, model_parameters: ModelParameters) -> bool:
        """Check if the current model supports tool calling."""
        # Based on Pollinations API model list, these models support tools
        tool_capable_models = [
            "openai",           # OpenAI GPT-4o Mini
            "openai-fast",      # OpenAI GPT-4.1 Nano
            "openai-large",     # OpenAI GPT-4.1
            "openai-roblox",    # OpenAI GPT-4.1 Mini (Roblox)
            "openai-audio",     # OpenAI GPT-4o Mini Audio Preview
            "grok",             # xAI Grok-3 Mini
            "llama-roblox",     # Llama 3.1 8B FP8
            "mistral",          # Mistral Small 3.1 24B
            "mistral-roblox",   # Mistral Small 3.1 24B (Cloudflare)
            "qwen-coder",       # Qwen 2.5 Coder 32B
            "searchgpt",        # OpenAI GPT-4o Mini Search Preview
            "bidara",           # BIDARA (NASA)
            "midijourney",      # MIDIjourney
            "mirexa",           # Mirexa AI Companion
            "rtist",            # Rtist
            "sur",              # Sur AI Assistant
            "unity",            # Unity Unrestricted Agent
            "evil",             # Evil (uncensored)
            "hypnosis-tracy",   # Hypnosis Tracy
        ]
        return model_parameters.model in tool_capable_models

    def parse_messages(self, messages: list[LLMMessage]) -> list[ChatCompletionMessageParam]:
        """Parse the messages to OpenAI format."""
        openai_messages: list[ChatCompletionMessageParam] = []
        for msg in messages:
            if msg.tool_result:
                openai_messages.append(self.parse_tool_call_result(msg.tool_result))
            elif msg.tool_call:
                openai_messages.append(self.parse_tool_call(msg.tool_call))
            else:
                if not msg.content:
                    raise ValueError("Message content is required")
                if msg.role == "system":
                    openai_messages.append(
                        ChatCompletionSystemMessageParam(
                            role="system", content=msg.content
                        )
                    )
                elif msg.role == "user":
                    openai_messages.append(
                        ChatCompletionUserMessageParam(role="user", content=msg.content)
                    )
                elif msg.role == "assistant":
                    openai_messages.append(
                        ChatCompletionAssistantMessageParam(
                            role="assistant", content=msg.content
                        )
                    )
                else:
                    raise ValueError(f"Invalid message role: {msg.role}")
        return openai_messages

    def parse_tool_call(self, tool_call: ToolCall) -> ChatCompletionAssistantMessageParam:
        """Parse the tool call from the LLM response."""
        return ChatCompletionAssistantMessageParam(
            role="assistant",
            tool_calls=[
                ChatCompletionMessageToolCallParam(
                    id=tool_call.call_id,
                    function=Function(
                        name=tool_call.name,
                        arguments=json.dumps(tool_call.arguments),
                    ),
                    type="function",
                )
            ],
        )

    def parse_tool_call_result(
        self, tool_call_result: ToolResult
    ) -> ChatCompletionToolMessageParam:
        """Parse the tool call result from the LLM response to OpenAI format."""
        result_content: str = ""
        if tool_call_result.result is not None:
            result_content += str(tool_call_result.result)
        if tool_call_result.error:
            result_content += f"\nError: {tool_call_result.error}"
        result_content = result_content.strip()

        return ChatCompletionToolMessageParam(
            role="tool",
            tool_call_id=tool_call_result.call_id,
            content=result_content,
        )
