import pytest
from local_llm.coreml import runLocalLLM
from local_llm.whisper_coreml import transcribeAudio


class TestRunLocalLLM:
    def test_returns_dict(self):
        result = runLocalLLM("hello world")
        assert isinstance(result, dict)

    def test_status_is_stub(self):
        result = runLocalLLM("prompt")
        assert result["status"] == "stub"

    def test_prompt_is_echoed(self):
        result = runLocalLLM("test prompt")
        assert result["prompt"] == "test prompt"

    def test_text_key_present(self):
        result = runLocalLLM("prompt")
        assert "text" in result

    def test_tokens_generated_is_int(self):
        result = runLocalLLM("prompt")
        assert isinstance(result["tokens_generated"], int)

    def test_max_tokens_respected(self):
        result = runLocalLLM("prompt", max_tokens=512)
        assert result["max_tokens"] == 512

    def test_model_is_echoed(self):
        result = runLocalLLM("prompt", model="custom.mlpackage")
        assert result["model"] == "custom.mlpackage"


class TestTranscribeAudio:
    def test_returns_dict(self):
        result = transcribeAudio("/path/to/audio.wav")
        assert isinstance(result, dict)

    def test_status_is_stub(self):
        result = transcribeAudio("audio.wav")
        assert result["status"] == "stub"

    def test_audio_path_is_echoed(self):
        result = transcribeAudio("/tmp/clip.m4a")
        assert result["audio_path"] == "/tmp/clip.m4a"

    def test_transcript_key_present(self):
        result = transcribeAudio("audio.wav")
        assert "transcript" in result

    def test_segments_is_list(self):
        result = transcribeAudio("audio.wav")
        assert isinstance(result["segments"], list)

    def test_language_is_echoed(self):
        result = transcribeAudio("audio.wav", language="es")
        assert result["language"] == "es"
