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

            articles.append(
                Article(
                    title=title.strip(),
                    abstract=summary.strip(),
                )
            )

        return articles

from .registry import registry

registry.register("arxiv", ArxivParser())
