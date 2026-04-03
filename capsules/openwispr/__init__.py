import logging
from typing import Any

LOGGER = logging.getLogger("argus.capsules.openwispr")


def stt(audio_source: str, context: dict[str, Any]) -> dict[str, Any]:
    LOGGER.info("OpenWISPR stt invoked for audio_source=%s context=%s", audio_source, context)
    return {"status": "ok", "action": "stt", "transcript": f"Stub transcript for {audio_source}"}


def tts(text: str, context: dict[str, Any]) -> dict[str, Any]:
    LOGGER.info("OpenWISPR tts invoked for text=%s context=%s", text, context)
    return {"status": "ok", "action": "tts", "audio_path": "memory://openwispr/output.wav", "text": text}


def handle_voice_command(text: str, context: dict[str, Any]) -> dict[str, Any]:
    LOGGER.info("OpenWISPR handle_voice_command invoked for text=%s context=%s", text, context)
    return {"status": "ok", "action": "handle_voice_command", "command": text, "intent": "stubbed"}
