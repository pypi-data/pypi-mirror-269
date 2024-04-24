# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Union, Iterable, Optional
from typing_extensions import Literal, Required, TypedDict

__all__ = [
    "CompletionCreateParams",
    "Message",
    "ToolChoice",
    "ToolChoiceToolChoice",
    "ToolChoiceToolChoiceFunction",
    "Tool",
    "ToolFunction",
    "ToolFunctionParameters",
    "ToolFunctionParametersProperties",
]


class CompletionCreateParams(TypedDict, total=False):
    messages: Required[Iterable[Message]]

    model: Required[Literal["cygnet-v0.2"]]

    frequency_penalty: Optional[float]

    max_tokens: Optional[int]

    n: Optional[int]

    stream: Optional[bool]

    temperature: Optional[float]

    tool_choice: ToolChoice

    tools: Optional[Iterable[Tool]]

    top_p: Optional[float]


class Message(TypedDict, total=False):
    content: Required[str]

    role: Required[Literal["system", "user", "assistant", "data"]]


class ToolChoiceToolChoiceFunction(TypedDict, total=False):
    name: Required[str]


class ToolChoiceToolChoice(TypedDict, total=False):
    function: Required[ToolChoiceToolChoiceFunction]

    type: Required[str]


ToolChoice = Union[Literal["none", "auto"], ToolChoiceToolChoice]


class ToolFunctionParametersProperties(TypedDict, total=False):
    description: Required[str]

    type: Required[str]


class ToolFunctionParameters(TypedDict, total=False):
    properties: Required[Dict[str, ToolFunctionParametersProperties]]

    required: Required[List[str]]

    type: Required[str]


class ToolFunction(TypedDict, total=False):
    description: Required[str]

    name: Required[str]

    parameters: Required[ToolFunctionParameters]


class Tool(TypedDict, total=False):
    function: Required[ToolFunction]

    type: Required[str]
