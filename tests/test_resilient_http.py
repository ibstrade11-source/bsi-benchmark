import urllib.error
import urllib.request

from bsi_benchmark.utils.resilient_http import (
    PermanentRequestError,
    RetryableRequestError,
    request,
)


def test_retries_connection_error_then_succeeds(monkeypatch):
    calls = {"n": 0}

    class Response:
        status = 200

        def read(self):
            return b'{"ok": true}'

        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

    def fake_urlopen(req, timeout):
        calls["n"] += 1
        if calls["n"] < 3:
            raise ConnectionError("DNS failure")
        return Response()

    monkeypatch.setattr(urllib.request, "urlopen", fake_urlopen)

    result = request(
        urllib.request.Request("https://example.invalid"),
        attempts=5,
        sleeper=lambda _: None,
    )

    assert result.status == 200
    assert result.attempts == 3
    assert calls["n"] == 3


def test_retries_429(monkeypatch):
    calls = {"n": 0}

    class Response:
        status = 200

        def read(self):
            return b'{"ok": true}'

        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

    def fake_urlopen(req, timeout):
        calls["n"] += 1
        if calls["n"] == 1:
            raise urllib.error.HTTPError(
                req.full_url,
                429,
                "rate limited",
                {},
                None,
            )
        return Response()

    monkeypatch.setattr(urllib.request, "urlopen", fake_urlopen)

    result = request(
        urllib.request.Request("https://example.invalid"),
        attempts=3,
        sleeper=lambda _: None,
    )

    assert result.status == 200
    assert result.attempts == 2


def test_permanent_http_error_is_not_retried(monkeypatch):
    calls = {"n": 0}

    def fake_urlopen(req, timeout):
        calls["n"] += 1
        raise urllib.error.HTTPError(
            req.full_url,
            400,
            "bad request",
            {},
            None,
        )

    monkeypatch.setattr(urllib.request, "urlopen", fake_urlopen)

    try:
        request(
            urllib.request.Request("https://example.invalid"),
            attempts=5,
            sleeper=lambda _: None,
        )
    except PermanentRequestError:
        pass
    else:
        raise AssertionError("PermanentRequestError expected")

    assert calls["n"] == 1


def test_retryable_error_becomes_explicit_failure(monkeypatch):
    calls = {"n": 0}

    def fake_urlopen(req, timeout):
        calls["n"] += 1
        raise ConnectionError("network unreachable")

    monkeypatch.setattr(urllib.request, "urlopen", fake_urlopen)

    try:
        request(
            urllib.request.Request("https://example.invalid"),
            attempts=3,
            sleeper=lambda _: None,
        )
    except RetryableRequestError:
        pass
    else:
        raise AssertionError("RetryableRequestError expected")

    assert calls["n"] == 3

def test_provider_neutral_facade_imports():
    from bsi_benchmark.utils.api_execution import (
        DEFAULT_ATTEMPTS,
        DEFAULT_TIMEOUT,
        execute_json_post,
    )

    assert DEFAULT_ATTEMPTS >= 3
    assert DEFAULT_TIMEOUT >= 30
    assert callable(execute_json_post)
