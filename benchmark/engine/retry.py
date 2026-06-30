import time
import requests

def get(url, **kwargs):
    retries = kwargs.pop("retries", 3)
    backoff = kwargs.pop("backoff", 2)

    last = None

    for i in range(retries):
        try:
            return requests.get(url, **kwargs)
        except Exception as e:
            last = e
            time.sleep(backoff ** i)

    raise last
