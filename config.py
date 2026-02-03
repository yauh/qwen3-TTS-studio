"""Configuration module for loading environment variables."""

import os
from pathlib import Path
from typing import Any


def _load_env_file():
    """Load .env file into os.environ if it exists."""
    env_path = Path(__file__).parent / ".env"
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    os.environ.setdefault(key.strip(), value.strip())


_load_env_file()


def get_llm_provider() -> str:
    """
    Get the configured LLM provider.

    Returns:
        str: The provider name ('openai' or 'portkey'). Defaults to 'openai'.
    """
    return os.getenv("LLM_PROVIDER", "openai").lower()


def get_llm_model() -> str:
    """
    Get the configured LLM model name.

    Returns:
        str: The model name. Defaults to 'gpt-5.2'.
    """
    return os.getenv("LLM_MODEL", "gpt-5.2")


def get_openai_api_key() -> str:
    """
    Load and return the OpenAI API key from environment.

    Returns:
        str: The OpenAI API key

    Raises:
        ValueError: If OPENAI_API_KEY is not set in environment
    """
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY not found in environment. "
            "Please ensure .env file exists with OPENAI_API_KEY set."
        )

    return api_key


def get_portkey_api_key() -> str:
    """
    Load and return the Portkey API key from environment.

    Returns:
        str: The Portkey API key

    Raises:
        ValueError: If PORTKEY_API_KEY is not set in environment when using Portkey
    """
    api_key = os.getenv("PORTKEY_API_KEY")

    if not api_key:
        raise ValueError(
            "PORTKEY_API_KEY not found in environment. "
            "Please ensure .env file exists with PORTKEY_API_KEY set."
        )

    return api_key


def get_portkey_virtual_key() -> str | None:
    """
    Load and return the Portkey virtual key from environment.

    Returns:
        str | None: The Portkey virtual key for OpenAI, or None if not set
    """
    return os.getenv("PORTKEY_VIRTUAL_KEY")


def get_portkey_base_url() -> str:
    """
    Get the Portkey base URL.

    Returns:
        str: The Portkey API base URL. Defaults to 'https://api.portkey.ai/v1'.
    """
    return os.getenv("PORTKEY_BASE_URL", "https://api.portkey.ai/v1")


def get_llm_client_config() -> dict[str, Any]:
    """
    Get the LLM client configuration based on the configured provider.

    Returns:
        dict: Configuration dictionary for OpenAI client initialization.
              For OpenAI: {"api_key": "..."}
              For Portkey: {"api_key": "...", "base_url": "...", "default_headers": {...}}

    Raises:
        ValueError: If required configuration is missing for the selected provider
    """
    provider = get_llm_provider()

    if provider == "portkey":
        portkey_api_key = get_portkey_api_key()
        portkey_virtual_key = get_portkey_virtual_key()
        portkey_base_url = get_portkey_base_url()

        headers: dict[str, str] = {
            "x-portkey-api-key": portkey_api_key,
        }

        # If virtual key is provided, use it (recommended)
        if portkey_virtual_key:
            headers["x-portkey-virtual-key"] = portkey_virtual_key
        else:
            # Otherwise, try to use OpenAI API key directly with Portkey
            # This only works for OpenAI models, not for Gemini/Claude/etc.
            openai_api_key = os.getenv("OPENAI_API_KEY")
            if not openai_api_key:
                raise ValueError(
                    "When using Portkey without a virtual key, OPENAI_API_KEY is required.\n"
                    "To use other models (Gemini, Claude, etc.), you must set PORTKEY_VIRTUAL_KEY.\n\n"
                    "Option 1 - Use virtual key (recommended for any model):\n"
                    "  PORTKEY_VIRTUAL_KEY=your-virtual-key\n\n"
                    "Option 2 - Use OpenAI directly (OpenAI models only):\n"
                    "  OPENAI_API_KEY=sk-proj-your-key"
                )
            headers["Authorization"] = f"Bearer {openai_api_key}"
            headers["x-portkey-provider"] = "openai"

        return {
            "api_key": portkey_api_key,
            "base_url": portkey_base_url,
            "default_headers": headers
        }
    elif provider == "openai":
        return {
            "api_key": get_openai_api_key()
        }
    else:
        raise ValueError(
            f"Unknown LLM provider: {provider}. "
            "Please set LLM_PROVIDER to either 'openai' or 'portkey'."
        )
