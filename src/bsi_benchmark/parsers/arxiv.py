import xml.etree.ElementTree as ET

from .base import Parser
from bsi_benchmark.models.article import Article


class ArxivParser(Parser):

    def parse(self, raw):

        root = ET.fromstring(raw)

        ns = {
            "a": "http://www.w3.org/2005/Atom"
        }

        articles = []

        for entry in root.findall("a:entry", ns):

            title = entry.findtext("a:title", default="", namespaces=ns)

            summary = entry.findtext(
                "a:summary",
                default="",
                namespaces=ns
            )

            # arXiv's Atom <id> is the canonical abstract-page URL for this
            # exact entry (e.g. "http://arxiv.org/abs/2106.01234v2") --
            # this is the provenance record: without it there is no way to
            # verify which paper/version a score was computed against.
            entry_url = entry.findtext("a:id", default=None, namespaces=ns)
            if entry_url:
                entry_url = entry_url.strip() or None

            # Some arXiv entries carry a DOI (arxiv:doi element, e.g. once
            # a paper is later published) -- capture it when present.
            arxiv_ns = {"arxiv": "http://arxiv.org/schemas/atom"}
            doi = entry.findtext("arxiv:doi", default=None, namespaces=arxiv_ns)
            if doi:
                doi = doi.strip() or None

            articles.append(
                Article(
                    title=title.strip(),
                    abstract=summary.strip(),
                    doi=doi,
                    url=entry_url,
                )
            )

        return articles

from .registry import registry

registry.register("arxiv", ArxivParser())
