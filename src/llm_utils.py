# src/llm_utils.py — robust OpenAI helper (handles different SDK shapes)
import os
import json
import logging
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

load_dotenv()

# Try to import openai and the newer OpenAI client wrapper if available
try:
    import openai
    from openai import OpenAI as OpenAIClient  # may exist in newer SDKs
except Exception:
    openai = None
    OpenAIClient = None

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
OPENAI_TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))
OPENAI_MAX_TOKENS = int(os.getenv("OPENAI_MAX_TOKENS", "800"))

logger = logging.getLogger("llm_utils")
logger.setLevel(logging.INFO)
if not logger.handlers:
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    logger.addHandler(ch)

# Build new client if possible
_client = None
if OpenAIClient is not None:
    try:
        _client = OpenAIClient(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else OpenAIClient()
    except Exception:
        _client = None

# Determine retry exception types (prefer openai-specific types if present)
_retry_exceptions = (Exception,)
if openai is not None:
    try:
        _retry_exceptions = (openai.error.RateLimitError, openai.error.ServiceUnavailableError, openai.error.APIError)
    except Exception:
        _retry_exceptions = (Exception,)


@retry(stop=stop_after_attempt(3),
       wait=wait_exponential(multiplier=1, min=1, max=8),
       retry=retry_if_exception_type(_retry_exceptions))
def call_openai_chat(prompt: str, system_prompt: str = None, model: str = None, temperature: float = None, max_tokens: int = None) -> dict:
    """
    Robust wrapper: tries new Responses API then falls back to legacy ChatCompletion.
    Returns: {"text": str, "usage": dict}
    """
    model = model or OPENAI_MODEL
    temperature = OPENAI_TEMPERATURE if temperature is None else temperature
    max_tokens = OPENAI_MAX_TOKENS if max_tokens is None else max_tokens

    # Try new Responses API (defensive about kwarg names)
    if _client is not None:
        logger.info("Attempting Responses API via new OpenAI client. model=%s", model)
        try:
            # Try call with max_output_tokens (modern name)
            try:
                resp = _client.responses.create(
                    model=model,
                    instructions=(system_prompt or ""),
                    input=prompt,
                    max_output_tokens=max_tokens,
                    temperature=temperature,
                )
            except TypeError as e:
                # If that param isn't accepted, try without max_output_tokens
                logger.info("Responses.create rejected max_output_tokens, retrying without it (%s)", e)
                try:
                    resp = _client.responses.create(
                        model=model,
                        instructions=(system_prompt or ""),
                        input=prompt,
                        temperature=temperature,
                    )
                except TypeError:
                    # Some SDKs accept messages-like input shape
                    messages = []
                    if system_prompt:
                        messages.append({"role": "system", "content": system_prompt})
                    messages.append({"role": "user", "content": prompt})
                    resp = _client.responses.create(model=model, input=messages, temperature=temperature)

            # Extract text safely
            text = None
            text = getattr(resp, "output_text", None)
            if not text:
                output = getattr(resp, "output", None) or (resp.get("output") if isinstance(resp, dict) else None)
                if output and isinstance(output, (list, tuple)) and len(output) > 0:
                    first = output[0]
                    content = first.get("content") if isinstance(first, dict) else None
                    if isinstance(content, list) and len(content) > 0:
                        c0 = content[0]
                        if isinstance(c0, dict):
                            text = c0.get("text") or c0.get("markdown") or c0.get("html") or str(c0)
                        else:
                            text = str(c0)
            if not text:
                text = str(resp)
            usage = getattr(resp, "usage", {}) or {}
            return {"text": text.strip() if isinstance(text, str) else str(text), "usage": usage}
        except Exception:
            logger.exception("Responses API attempt failed; will rethrow for retry or fallback.")
            raise

    # Fallback: legacy openai.ChatCompletion
    if openai is not None:
        logger.info("Attempting legacy ChatCompletion API fallback.")
        if not getattr(openai, "api_key", None) and not OPENAI_API_KEY:
            raise RuntimeError("OPENAI_API_KEY not set. Add it to .env or environment to use LLM mode.")
        if OPENAI_API_KEY and not getattr(openai, "api_key", None):
            openai.api_key = OPENAI_API_KEY

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        try:
            resp = openai.ChatCompletion.create(model=model, messages=messages, max_tokens=max_tokens, temperature=temperature)
            text = ""
            try:
                text = resp.choices[0].message.content.strip()
            except Exception:
                try:
                    text = resp.choices[0].text.strip()
                except Exception:
                    text = str(resp)
            usage = resp.get("usage", {}) if isinstance(resp, dict) else {}
            return {"text": text, "usage": usage}
        except Exception:
            logger.exception("Legacy ChatCompletion call failed")
            raise

    raise RuntimeError("openai library is not installed or configured properly. Install/upgrade openai and set OPENAI_API_KEY in .env to use LLM mode.")
