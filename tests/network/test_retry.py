import pytest

from bsi_benchmark.network.retry import retry


class FakeResponse:
    def __init__(self, status_code):
        self.status_code = status_code


def test_retry_success_without_retry():
    calls = []

    def operation():
        calls.append(1)
        return "ok"

    result = retry(operation, attempts=3, delay=0)

    assert result == "ok"
    assert len(calls) == 1


def test_retry_on_exception_then_success():
    calls = []

    def operation():
        calls.append(1)
        if len(calls) < 3:
            raise ConnectionError("temporary failure")
        return "ok"

    result = retry(operation, attempts=3, delay=0)

    assert result == "ok"
    assert len(calls) == 3


def test_retry_on_retryable_response_then_success():
    calls = []

    def operation():
        calls.append(1)
        if len(calls) < 3:
            return FakeResponse(503)
        return FakeResponse(200)

    result = retry(
        operation,
        attempts=3,
        delay=0,
        should_retry=lambda response: response.status_code
        in {429, 500, 502, 503, 504},
    )

    assert result.status_code == 200
    assert len(calls) == 3


def test_retry_on_429_response_then_success():
    calls = []

    def operation():
        calls.append(1)
        if len(calls) == 1:
            return FakeResponse(429)
        return FakeResponse(200)

    result = retry(
        operation,
        attempts=3,
        delay=0,
        should_retry=lambda response: response.status_code == 429,
    )

    assert result.status_code == 200
    assert len(calls) == 2


def test_retry_does_not_retry_non_retryable_response():
    calls = []

    def operation():
        calls.append(1)
        return FakeResponse(401)

    result = retry(
        operation,
        attempts=3,
        delay=0,
        should_retry=lambda response: response.status_code
        in {429, 500, 502, 503, 504},
    )

    assert result.status_code == 401
    assert len(calls) == 1


def test_retry_raises_last_exception_after_exhaustion():
    calls = []

    def operation():
        calls.append(1)
        raise TimeoutError("timeout")

    with pytest.raises(TimeoutError, match="timeout"):
        retry(operation, attempts=3, delay=0)

    assert len(calls) == 3


def test_retry_returns_last_retryable_result_after_exhaustion():
    calls = []

    def operation():
        calls.append(1)
        return FakeResponse(503)

    result = retry(
        operation,
        attempts=3,
        delay=0,
        should_retry=lambda response: response.status_code >= 500,
    )

    assert result.status_code == 503
    assert len(calls) == 3
