import os
import time
import logging
import requests

_BASE_URL = os.environ.get("ARGUS_PRIME_URL", "http://localhost:8080")
_DEFAULT_TIMEOUT = int(os.environ.get("ARGUS_CLIENT_TIMEOUT", "10"))
_MAX_RETRIES = int(os.environ.get("ARGUS_CLIENT_RETRIES", "3"))


def sendToArgusPrime(payload: dict, retries: int = _MAX_RETRIES) -> dict:
    """
    Send an agent request to the Argus Prime API with exponential-backoff retry.
    Returns the parsed JSON response or an error dict on final failure.
    """
    url = f"{_BASE_URL}/agent"
    attempt = 0
    delay = 2

    while attempt <= retries:
        try:
            response = requests.post(url, json=payload, timeout=_DEFAULT_TIMEOUT)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.ConnectionError as e:
            logging.warning(f"[mobile] Connection error on attempt {attempt + 1}: {e}")
        except requests.exceptions.Timeout as e:
            logging.warning(f"[mobile] Timeout on attempt {attempt + 1}: {e}")
        except requests.exceptions.HTTPError as e:
            logging.error(f"[mobile] HTTP error: {e}")
            return {"status": "error", "error": str(e), "attempt": attempt + 1}

        attempt += 1
        if attempt <= retries:
            logging.info(f"[mobile] Retrying in {delay}s (attempt {attempt + 1}/{retries + 1})")
            time.sleep(delay)
            delay *= 2

    return {"status": "error", "error": "Max retries exceeded", "url": url}
