import os
from functools import lru_cache

from langchain_openai import AzureChatOpenAI

from codegen import config


@lru_cache(maxsize=1)
def _client() -> AzureChatOpenAI:
    return AzureChatOpenAI(
        azure_deployment=config.DEPLOYMENT_NAME,
        azure_endpoint=config.ENDPOINT,
        api_version=config.API_VERSION,
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        temperature=config.TEMPERATURE,
    )


def ask_llm(prompt: str) -> str:
    """Send a single user prompt and return the raw text of the reply.

    May raise openai.BadRequestError (e.g. Azure content filtering).
    """
    return _client().invoke([{"role": "user", "content": prompt}]).content


def strip_code_fences(text: str) -> str:
    """Remove a surrounding ```python ... ``` (or ``` ... ```) block."""
    code = text.strip()
    if code.startswith("```python"):
        code = code[len("```python"):].strip()
    elif code.startswith("```"):
        code = code[len("```"):].strip()
    if code.endswith("```"):
        code = code[:-len("```")].strip()
    return code
