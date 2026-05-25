from src.core import config
from src.core.completion_params import build_completion_kwargs


def test_build_completion_kwargs_respects_allowlist(monkeypatch):
    monkeypatch.setattr(config, "AZURE_OPENAI_SUPPORTED_PARAMS", "temperature,max_tokens")
    monkeypatch.setattr(config, "AZURE_OPENAI_TEMPERATURE", 0.4)
    monkeypatch.setattr(config, "AZURE_OPENAI_MAX_TOKENS", 150)
    monkeypatch.setattr(config, "AZURE_OPENAI_TOP_P", 0.9)

    kwargs = build_completion_kwargs()

    assert kwargs == {"temperature": 0.4, "max_tokens": 150}


def test_build_completion_kwargs_omits_unsupported_overrides(monkeypatch):
    monkeypatch.setattr(config, "AZURE_OPENAI_SUPPORTED_PARAMS", "temperature,max_tokens")
    monkeypatch.setattr(config, "AZURE_OPENAI_TEMPERATURE", 0.6)
    monkeypatch.setattr(config, "AZURE_OPENAI_MAX_TOKENS", 100)

    kwargs = build_completion_kwargs(max_tokens=250, top_p=0.7)

    assert kwargs == {"temperature": 0.6, "max_tokens": 250}


def test_build_completion_kwargs_drops_empty_values(monkeypatch):
    monkeypatch.setattr(config, "AZURE_OPENAI_SUPPORTED_PARAMS", "temperature,frequency_penalty")
    monkeypatch.setattr(config, "AZURE_OPENAI_TEMPERATURE", 0.7)
    monkeypatch.setattr(config, "AZURE_OPENAI_FREQUENCY_PENALTY", "")

    kwargs = build_completion_kwargs()

    assert kwargs == {"temperature": 0.7}
