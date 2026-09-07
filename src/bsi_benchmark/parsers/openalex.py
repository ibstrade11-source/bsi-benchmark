import json

from .base import Parser
from bsi_benchmark.models.article import Article


def _reconstruct_abstract(inverted_index):
    """
    OpenAlex does not return abstracts as plain text -- for copyright
    reasons it returns `abstract_inverted_index`, a {word: [positions]}
    map, e.g. {"The": [0], "cat": [1], "sat": [2]}. Reassemble it into
    normal text by placing each word at each of its recorded positions.
    """
    if not inverted_index:
        return None

    positions = {}
    for word, idxs in inverted_index.items():
        for i in idxs:
            positions[i] = word

    if not positions:
        return None

    ordered = [positions[i] for i in sorted(positions)]
    text = " ".join(ordered).strip()
    return text or None


class OpenAlexParser(Parser):

    def parse(self, raw):

        data = json.loads(raw)

        # OpenAlex search responses use {"results": [...]},
        # while /works/{id} returns one Work object directly.
        # Normalize both response shapes to a list.
        if "results" in data:
            items = data["results"]
        elif data.get("id") and data.get("title"):
            items = [data]
        else:
            raise ValueError("Unrecognized OpenAlex response shape")

        articles = []

        for item in items:

            title = item.get("title") or ""
            abstract = _reconstruct_abstract(item.get("abstract_inverted_index"))

            quality = {
                "has_title": bool(title),
                "has_abstract": bool(abstract),
                "source": "openalex",
                "enriched": False,
            }

            articles.append(
                Article(
                    title=title,
                    abstract=abstract,
                    doi=item.get("doi"),
                    url=item.get("id"),
                    input_quality=quality,
                )
            )

        return articles

from .registry import registry

registry.register("openalex", OpenAlexParser())
