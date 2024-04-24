"""
Predefined types derived from traces.
"""

from dataclasses import dataclass

from pydantic import BaseModel


@dataclass(frozen=True)
class QueryReceived(BaseModel):
    """Query received by the system - something a user would say."""

    query: str


@dataclass(frozen=True)
class ContextRetrieved(BaseModel):
    """Retrieved data from ingestion pipeline - relevant pieces of text
    extracted from documents."""

    context: list[str]


@dataclass(frozen=True)
class PromptResolved(BaseModel):
    """Final prompt input with all template variables included - the exact text
    that gets sent to the LLM."""

    fully_resolved_prompt: str


@dataclass(frozen=True)
class LLMOutputReceived(BaseModel):
    """Text response from the LLM."""

    llm_output: str
