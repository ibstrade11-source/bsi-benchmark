"""
Deterministic retrieval validation for benchmark article selection.

The provider may return semantically related but incorrect records.
This module distinguishes title-like article queries from broad
topical queries and validates title-like retrievals before analysis.
"""

import re
from dataclasses import dataclass


_STOPWORDS = {
    "a", "an", "and", "as", "at", "by", "for", "from", "in", "into",
    "of", "on", "or", "the", "to", "with", "without", "through",
    "toward", "towards", "over", "under", "using", "via",
}


def normalize(text: str) -> str:
    text = (text or "").lower()
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return " ".join(text.split())


def tokens(text: str) -> set[str]:
    return {
        token
        for token in normalize(text).split()
        if token
    }


def substantive_tokens(text: str) -> set[str]:
    return tokens(text) - _STOPWORDS


def title_similarity(query: str, title: str) -> float:
    q = substantive_tokens(query)
    t = substantive_tokens(title)

    if not q or not t:
        return 0.0

    intersection = len(q & t)
    union = len(q | t)
    jaccard = intersection / union if union else 0.0

    # Recall of the requested substantive terms is especially important
    # when the provider adds/removes short function words.
    recall = intersection / len(q)

    # Weighted toward query-term recall, while retaining Jaccard
    # discrimination against merely related titles.
    return round((0.65 * recall) + (0.35 * jaccard), 4)


def looks_like_title_query(query: str) -> bool:
    """
    Conservative classifier.

    Short/broad queries remain topical queries.  Longer queries containing
    strong title-like punctuation are treated as requests for a specific
    article.  A long structured title without punctuation is also covered
    when it has >= 9 substantive tokens.
    """
    raw = (query or "").strip()
    if not raw:
        return False

    q_tokens = normalize(raw).split()
    substantive = substantive_tokens(raw)

    if len(substantive) < 6:
        return False

    # Strong signals of a bibliographic/article-title query.
    if re.search(r"[:;?!]", raw):
        return True

    if " - " in raw or "—" in raw or "–" in raw:
        return True

    # Very long exact-title-like strings.
    if len(q_tokens) >= 12 and len(substantive) >= 8:
        return True

    return False


@dataclass
class RetrievalDecision:
    accepted: bool
    status: str
    reason: str
    match_score: float
    query_type: str
    requested_query: str
    returned_title: str
    candidate_rank: int


def validate_candidates(query: str, articles: list) -> tuple[list, list[dict], dict]:
    """
    Return:
      valid articles,
      rejected candidate audit records,
      summary metadata.

    Broad topical queries preserve the historical behavior: all usable
    provider results are accepted.

    Title-like queries require a high title match and select the best
    matching candidate.
    """
    title_query = looks_like_title_query(query)

    if not title_query:
        return (
            articles,
            [],
            {
                "retrieval_status": "accepted",
                "retrieval_validation": "not_required",
                "query_type": "topic",
                "requested_query": query,
                "candidate_count": len(articles),
            },
        )

    scored = []
    for rank, article in enumerate(articles, 1):
        score = title_similarity(query, article.title)
        scored.append((score, rank, article))

    scored.sort(key=lambda item: (-item[0], item[1]))

    # Deliberately strict for article-title retrieval.
    threshold = 0.72

    best = scored[0] if scored else None
    if best is not None and best[0] >= threshold:
        score, rank, article = best

        rejected = []
        for candidate_score, candidate_rank, candidate in scored:
            if candidate is article:
                continue
            rejected.append(
                {
                    "title": candidate.title,
                    "doi": candidate.doi,
                    "url": candidate.url,
                    "rank": candidate_rank,
                    "match_score": candidate_score,
                    "status": "rejected_lower_match",
                }
            )

        return (
            [article],
            rejected,
            {
                "retrieval_status": "accepted",
                "retrieval_validation": "title_match",
                "query_type": "title",
                "requested_query": query,
                "selected_title": article.title,
                "selected_rank": rank,
                "match_score": score,
                "threshold": threshold,
                "candidate_count": len(articles),
            },
        )

    rejected = []
    for score, rank, article in scored:
        rejected.append(
            {
                "title": article.title,
                "doi": article.doi,
                "url": article.url,
                "rank": rank,
                "match_score": score,
                "status": "invalid_retrieval",
                "reason": "title_query_mismatch",
            }
        )

    return (
        [],
        rejected,
        {
            "retrieval_status": "invalid",
            "retrieval_validation": "title_mismatch",
            "query_type": "title",
            "requested_query": query,
            "match_score": best[0] if best else 0.0,
            "threshold": threshold,
            "candidate_count": len(articles),
            "reason": "title_query_mismatch",
        },
    )
