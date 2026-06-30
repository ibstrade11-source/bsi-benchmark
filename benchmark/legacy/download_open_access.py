#!/usr/bin/env python3

import json
import pathlib
import random
import time
import requests

ROOT = pathlib.Path.home() / "bsi-benchmark" / "benchmark"
DATASETS = ROOT / "datasets"

FIELDS = {
    "medicine": "medicine",
    "computer_science": "computer science",
    "economics": "economics",
    "psychology": "psychology",
    "physics": "physics",
    "biology": "biology",
    "engineering": "engineering",
    "education": "education",
    "sociology": "sociology",
    "environment": "environment"
}

HEADERS = {
    "User-Agent": "BSI-Benchmark/1.0"
}

API = "https://api.crossref.org/works"

for folder, query in FIELDS.items():

    out = DATASETS / folder
    out.mkdir(parents=True, exist_ok=True)

    params = {
        "query": query,
        "rows": 25,
        "filter": "has-full-text:true"
    }

    r = requests.get(API, params=params, headers=HEADERS, timeout=60)

    if r.status_code != 200:
        print(folder, "FAILED")
        continue

    items = r.json()["message"]["items"]

    random.shuffle(items)

    saved = 0

    for paper in items:

        if saved >= 10:
            break

        title = paper.get("title", ["untitled"])[0]

        doi = paper.get("DOI", "")

        links = paper.get("link", [])

        pdf = None

        for x in links:
            if "pdf" in x.get("content-type", "").lower():
                pdf = x["URL"]
                break

        if pdf is None:
            continue

        fn = out / f"{saved+1:02d}.json"

        json.dump(
            {
                "title": title,
                "doi": doi,
                "pdf": pdf
            },
            open(fn, "w"),
            indent=2
        )

        print(folder, saved + 1, title[:70])

        saved += 1

        time.sleep(1)

print("\nDONE")
