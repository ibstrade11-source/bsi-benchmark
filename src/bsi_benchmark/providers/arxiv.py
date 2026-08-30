"""
arXiv provider.
"""

import io
import re
from urllib.parse import quote

from bsi_benchmark.network import HttpClient
from bsi_benchmark.errors import ProviderUnavailable

from .base import Provider
from .registry import registry


class ArxivFullTextError(ProviderUnavailable):
    """Raised when a PDF for an arXiv article can't be fetched or parsed
    into usable text. Callers decide whether to fall back to abstract-only
    -- this is never silently swallowed inside the provider."""
    pass


def _extract_arxiv_id(url_or_id: str) -> str:
    """
    Normalize an arXiv abstract-page URL or a bare id into the id string
    used in the PDF URL. Handles both id schemes arXiv has used:
      - new-style (2007-present): '2106.01234v2'
      - old-style (pre-2007): 'physics/0508180v2', 'quant-ph/9908047'
        -- these carry a subject-class prefix that MUST be preserved,
        since https://arxiv.org/pdf/0508180v2 (without 'physics/') 404s;
        the correct PDF url is https://arxiv.org/pdf/physics/0508180v2.
    Falls back to the last path segment for anything that doesn't match
    either pattern.
    """
    if not url_or_id:
        return url_or_id
    new_style = re.search(r"(\d{4}\.\d{4,5}(v\d+)?)", url_or_id)
    if new_style:
        return new_style.group(1)
    old_style = re.search(r"([a-zA-Z\-]+/\d{7}(v\d+)?)", url_or_id)
    if old_style:
        return old_style.group(1)
    return url_or_id.rstrip("/").split("/")[-1]


class ArxivProvider(Provider):

    name = "arxiv"

    BASE_URL = "https://export.arxiv.org/api/query"
    PDF_URL = "https://arxiv.org/pdf/{arxiv_id}"

    def __init__(self):
        self.client = HttpClient()

    def fetch_fulltext(self, article) -> str:
        """
        Download the PDF for `article` (derived from its arXiv
        abstract-page URL) and extract plain text from it.

        Raises ArxivFullTextError on any failure (no URL to derive an id
        from, network/HTTP failure, missing pypdf, unparseable PDF, or a
        PDF that yields no extractable text -- e.g. a scanned/image-only
        paper). Never returns an empty string; callers can catch this
        exception and fall back to abstract-only rather than have a
        silent empty full_text field.
        """
        if not article.url:
            raise ArxivFullTextError(
                "article has no arXiv URL to derive a PDF link from"
            )

        arxiv_id = _extract_arxiv_id(article.url)
        pdf_url = self.PDF_URL.format(arxiv_id=arxiv_id)

        try:
            pdf_bytes = self.client.get_bytes(pdf_url)
        except Exception as e:
            # A versioned id whose PDF 404s often means that specific
            # version was withdrawn by the authors (arXiv still lists it
            # as the "latest version" but serves no PDF for it) -- v1
            # commonly still has a real PDF in that case. Retry once
            # against v1 before giving up; only for v2+ so we don\'t loop.
            fallback_id = None
            m = re.match(r"^(.*?)v(\d+)$", arxiv_id)
            if m and int(m.group(2)) > 1:
                fallback_id = f"{m.group(1)}v1"

            if not fallback_id:
                raise ArxivFullTextError(
                    f"failed to download PDF from {pdf_url}: {e}"
                ) from e

            fallback_url = self.PDF_URL.format(arxiv_id=fallback_id)
            try:
                pdf_bytes = self.client.get_bytes(fallback_url)
                pdf_url = fallback_url
            except Exception as e2:
                raise ArxivFullTextError(
                    f"failed to download PDF from {pdf_url} ({e}) and "
                    f"from fallback {fallback_url} ({e2}) -- the article "
                    "may have been withdrawn with no PDF available at "
                    "any version"
                ) from e2

        try:
            from pypdf import PdfReader
        except ImportError as e:
            raise ArxivFullTextError(
                "pypdf is required for full-text extraction -- install "
                "it with: pip install pypdf"
            ) from e

        try:
            reader = PdfReader(io.BytesIO(pdf_bytes))
            pages_text = [(page.extract_text() or "") for page in reader.pages]
        except Exception as e:
            raise ArxivFullTextError(
                f"failed to parse PDF from {pdf_url}: {e}"
            ) from e

        full_text = "\n\n".join(t.strip() for t in pages_text if t.strip())

        if not full_text.strip():
            raise ArxivFullTextError(
                f"PDF at {pdf_url} produced no extractable text "
                "(likely a scanned/image-only PDF)"
            )

        return full_text

    def search(self, query: str, rows: int = 5):
        # Retry-on-5xx/429 is handled centrally inside HttpClient.get().
        q = (query or "").strip()
        if q.lower().startswith("id:"):
            paper_id = q.split(":", 1)[1].strip()
            url = (
                f"{self.BASE_URL}"
                f"?id_list={quote(paper_id)}"
                f"&start=0"
                f"&max_results={rows}"
            )
        else:
            url = (
                f"{self.BASE_URL}"
                f"?search_query=all:{quote(q)}"
                f"&start=0"
                f"&max_results={rows}"
            )

        response = self.client.get(url)

        if not response.ok:
            raise ProviderUnavailable(
                f"arXiv HTTP {response.status_code}: {response.body}"
            )

        return response.body


registry.register(ArxivProvider)
