from types import SimpleNamespace

from bsi_benchmark.network.client import HttpClient
from bsi_benchmark.network.response import Response


class FakeSession:
    def __init__(self, responses=None, exceptions=None):
        self.headers = {}
        self.responses = list(responses or [])
        self.exceptions = list(exceptions or [])
        self.calls = []

    def get(self, url, timeout):
        self.calls.append(("GET", url, timeout))

        if self.exceptions:
            exc = self.exceptions.pop(0)
            raise exc

        return self.responses.pop(0)

    def post(self, url, json, headers, timeout):
        self.calls.append(("POST", url, json, headers, timeout))

        if self.exceptions:
            exc = self.exceptions.pop(0)
            raise exc

        return self.responses.pop(0)


def response(status_code, url="https://example.test", text="body"):
    return SimpleNamespace(
        status_code=status_code,
        url=url,
        text=text,
    )


def test_get_returns_normalized_response(monkeypatch):
    client = HttpClient()
    fake = FakeSession(
        responses=[response(200, text="hello")]
    )
    client.session = fake

    result = client.get("https://example.test/data")

    assert isinstance(result, Response)
    assert result.status_code == 200
    assert result.url == "https://example.test"
    assert result.body == "hello"
    assert len(fake.calls) == 1


def test_get_retries_503_then_succeeds(monkeypatch):
    client = HttpClient()
    fake = FakeSession(
        responses=[
            response(503, text="temporary"),
            response(200, text="success"),
        ]
    )
    client.session = fake

    monkeypatch.setattr(
        "bsi_benchmark.network.retry.time.sleep",
        lambda _: None,
    )

    result = client.get("https://example.test/data")

    assert result.status_code == 200
    assert result.body == "success"
    assert len(fake.calls) == 2


def test_get_retries_429_then_succeeds(monkeypatch):
    client = HttpClient()
    fake = FakeSession(
        responses=[
            response(429, text="rate limited"),
            response(200, text="success"),
        ]
    )
    client.session = fake

    monkeypatch.setattr(
        "bsi_benchmark.network.retry.time.sleep",
        lambda _: None,
    )

    result = client.get("https://example.test/data")

    assert result.status_code == 200
    assert result.body == "success"
    assert len(fake.calls) == 2


def test_get_does_not_retry_401():
    client = HttpClient()
    fake = FakeSession(
        responses=[response(401, text="unauthorized")]
    )
    client.session = fake

    result = client.get("https://example.test/data")

    assert result.status_code == 401
    assert result.body == "unauthorized"
    assert len(fake.calls) == 1


def test_get_does_not_retry_404():
    client = HttpClient()
    fake = FakeSession(
        responses=[response(404, text="not found")]
    )
    client.session = fake

    result = client.get("https://example.test/data")

    assert result.status_code == 404
    assert result.body == "not found"
    assert len(fake.calls) == 1


def test_get_retries_network_exception_then_succeeds(monkeypatch):
    client = HttpClient()
    fake = FakeSession(
        responses=[response(200, text="recovered")],
        exceptions=[ConnectionError("connection reset")],
    )
    client.session = fake

    monkeypatch.setattr(
        "bsi_benchmark.network.retry.time.sleep",
        lambda _: None,
    )

    result = client.get("https://example.test/data")

    assert result.status_code == 200
    assert result.body == "recovered"
    assert len(fake.calls) == 2


def test_get_exhausts_5xx_retries(monkeypatch):
    client = HttpClient()
    fake = FakeSession(
        responses=[
            response(503),
            response(503),
            response(503),
        ]
    )
    client.session = fake

    monkeypatch.setattr(
        "bsi_benchmark.network.retry.time.sleep",
        lambda _: None,
    )

    result = client.get("https://example.test/data")

    assert result.status_code == 503
    assert len(fake.calls) == 3


def test_post_returns_normalized_response(monkeypatch):
    client = HttpClient()
    fake = FakeSession(
        responses=[response(201, text="created")]
    )
    client.session = fake

    result = client.post(
        "https://example.test/data",
        json_body={"name": "test"},
        headers={"X-Test": "1"},
        timeout=42,
    )

    assert result.status_code == 201
    assert result.body == "created"
    assert fake.calls == [
        (
            "POST",
            "https://example.test/data",
            {"name": "test"},
            {"X-Test": "1"},
            42,
        )
    ]


def test_post_retries_500_then_succeeds(monkeypatch):
    client = HttpClient()
    fake = FakeSession(
        responses=[
            response(500),
            response(200, text="ok"),
        ]
    )
    client.session = fake

    monkeypatch.setattr(
        "bsi_benchmark.network.retry.time.sleep",
        lambda _: None,
    )

    result = client.post(
        "https://example.test/data",
        json_body={"query": "test"},
    )

    assert result.status_code == 200
    assert result.body == "ok"
    assert len(fake.calls) == 2


def test_should_retry_policy():
    assert HttpClient._should_retry(Response(429, "", ""))
    assert HttpClient._should_retry(Response(500, "", ""))
    assert HttpClient._should_retry(Response(502, "", ""))
    assert HttpClient._should_retry(Response(503, "", ""))
    assert HttpClient._should_retry(Response(504, "", ""))

    assert not HttpClient._should_retry(Response(200, "", ""))
    assert not HttpClient._should_retry(Response(400, "", ""))
    assert not HttpClient._should_retry(Response(401, "", ""))
    assert not HttpClient._should_retry(Response(404, "", ""))
