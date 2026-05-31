import os
import logging

_DEFAULT_MODEL = os.environ.get("COREML_MODEL_PATH", "models/argus-local.mlpackage")


def runLocalLLM(prompt: str, model: str = _DEFAULT_MODEL, max_tokens: int = 256) -> dict:
    """
    Run inference via a local CoreML LLM model.
    Stub — replace body with CoreML/MLX bindings when targeting Apple Silicon.
    """
    logging.info(f"[CoreML] runLocalLLM: model={model} prompt_len={len(prompt)}")
    return {
        "status": "stub",
        "model": model,
        "prompt": prompt,
        "text": "",
        "tokens_generated": 0,
        "max_tokens": max_tokens,
    }
