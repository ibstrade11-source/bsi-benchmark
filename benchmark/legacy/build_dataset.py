#!/usr/bin/env python3

import json
import random
import re
import time
from pathlib import Path

import requests

ROOT = Path.home() / "bsi-benchmark" / "benchmark"

DATA = ROOT / "datasets"

HEADERS = {
    "User-Agent": "BSI-Benchmark/1.0"
}

FIELDS = {

    "medicine":
        "https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=OPEN_ACCESS:y AND HAS_PDF:y AND SRC:PMC&format=json&pageSize=100",

    "computer_science":
        "http://export.arxiv.org/api/query?search_query=cat:cs.AI&start=0&max_results=100",

    "physics":
        "http://export.arxiv.org/api/query?search_query=cat:physics&start=0&max_results=100",

    "biology":
        "https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=OPEN_ACCESS:y AND biology&format=json&pageSize=100",

    "engineering":
        "http://export.arxiv.org/api/query?search_query=cat:cs.RO&start=0&max_results=100",

    "economics":
        "https://api.crossref.org/works?query=economics&rows=100",

    "psychology":
        "https://api.crossref.org/works?query=psychology&rows=100",

    "education":
        "https://api.crossref.org/works?query=education&rows=100",

    "sociology":
        "https://api.crossref.org/works?query=sociology&rows=100",

    "environment":
        "https://api.crossref.org/works?query=environment&rows=100"

}

BLACKLIST = [

"book review",
"review of",
"editorial",
"welcome",
"preface",
"commentary",
"correction",
"corrigendum",
"letter",
"news",
"foreword"

]

def bad(title):

    t = title.lower()

    return any(x in t for x in BLACKLIST)


def save(folder,title,pdf,doi):

    out = DATA/folder

    out.mkdir(parents=True,exist_ok=True)

    n=len(list(out.glob("*.json")))+1

    with open(out/f"{n:03}.json","w") as f:

        json.dump({

            "title":title,

            "doi":doi,

            "pdf":pdf

        },f,indent=2)

for field,url in FIELDS.items():

    print("\n==========",field,"==========")

    if "crossref" in url:

        r=requests.get(url,headers=HEADERS,timeout=60)

        items=r.json()["message"]["items"]

        random.shuffle(items)

        count=0

        for p in items:

            if count==20:

                break

            title=" ".join(p.get("title",[]))

            if bad(title):

                continue

            links=p.get("link",[])

            pdf=None

            for x in links:

                if "pdf" in x.get("content-type","").lower():

                    pdf=x["URL"]

                    break

            if pdf is None:

                continue

            save(field,title,pdf,p.get("DOI",""))

            print("✓",title[:90])

            count+=1

            time.sleep(0.5)

    elif "europepmc" in url:

        r=requests.get(url,headers=HEADERS,timeout=60)

        items=r.json()["resultList"]["result"]

        random.shuffle(items)

        count=0

        for p in items:

            if count==20:

                break

            title=p.get("title","")

            if bad(title):

                continue

            pdf=f"https://pmc.ncbi.nlm.nih.gov/articles/{p['pmcid']}/pdf"

            save(field,title,pdf,p.get("doi",""))

            print("✓",title[:90])

            count+=1

            time.sleep(.5)

    else:

        print("arXiv source registered (parser added in next step).")

print("\nDATASET BUILD COMPLETE")
