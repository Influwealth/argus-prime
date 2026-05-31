import os
import logging

_DEFAULT_MODEL = os.environ.get("WHISPER_COREML_MODEL_PATH", "models/whisper-base.mlpackage")


def transcribeAudio(audio_path: str, language: str = "en", model: str = _DEFAULT_MODEL) -> dict:
    """
    Transcribe audio using a local CoreML Whisper model.
    Stub — replace body with CoreML/WhisperKit bindings when targeting Apple Silicon.
    """
    logging.info(f"[Whisper CoreML] transcribeAudio: audio={audio_path} lang={language}")
    return {
        "status": "stub",
        "audio_path": audio_path,
        "language": language,
        "model": model,
        "transcript": "",
        "segments": [],
    }
