import requests


class BSIApiClient:
    def __init__(self, base_url="http://127.0.0.1:8000"):
        self.base_url = base_url.rstrip("/")

    def score(self, text, detail=False):
        r = requests.post(
            f"{self.base_url}/bsi/score",
            json={
                "text": text,
                "detail": detail,
            },
            timeout=120,
        )
        r.raise_for_status()
        return r.json()

    def analyze(self, text):
        r = requests.post(
            f"{self.base_url}/bsi/analyze",
            json={
                "text": text,
            },
            timeout=120,
        )
        r.raise_for_status()
        return r.json()

    def analyze_llm(self, text):
        r = requests.post(
            f"{self.base_url}/bsi/analyze_llm",
            json={
                "text": text,
            },
            timeout=300,
        )
        r.raise_for_status()
        return r.json()

    def compare(self, text_a, text_b):
        r = requests.post(
            f"{self.base_url}/bsi/compare",
            json={
                "text_a": text_a,
                "text_b": text_b,
            },
            timeout=120,
        )
        r.raise_for_status()
        return r.json()
