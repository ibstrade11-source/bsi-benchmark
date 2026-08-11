import json
import urllib.request

import pytest

from bsi_benchmark.utils import judge_execution


def test_judge_execution_uses_shared_request_layer(monkeypatch):
    calls = []

    def fake_request(req, *, timeout, attempts):
        calls.append((req, timeout, attempts))
        return type(
            "Response",
            (),
            {"body": json.dumps({"choices": [{"message": {"content": "OK"}}]}).encode()},
        )()

    monkeypatch.setattr(judge_execution, "request", fake_request)

    result = judge_execution.execute_judge_request(
        "https://example.test/v1/chat/completions",
        {"model": "test", "messages": []},
        api_key="dummy",
        timeout=30,
        attempts=5,
    )

    assert result["choices"][0]["message"]["content"] == "OK"
    assert len(calls) == 1
    assert calls[0][1] == 30
    assert calls[0][2] == 5


def test_judge_execution_rejects_invalid_json(monkeypatch):
    def fake_request(req, *, timeout, attempts):
        return type("Response", (), {"body": b"not-json"})()

    monkeypatch.setattr(judge_execution, "request", fake_request)

    with pytest.raises(ValueError, match="invalid JSON"):
        judge_execution.execute_judge_request(
            "https://example.test/v1/chat/completions",
            {"model": "test", "messages": []},
            api_key="dummy",
        )
