# فقط فایل فعلی را اصلاح کن:
# بعد از response = self.client.get(url)

for _ in range(3):
    response = self.client.get(url)
    if response.ok:
        break
    import time
    time.sleep(2)

if not response.ok:
    raise ProviderUnavailable(
        f"Crossref HTTP {response.status_code}: {response.body}"
    )
