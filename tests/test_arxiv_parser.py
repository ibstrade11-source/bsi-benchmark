"""
Tests for ArxivParser provenance extraction (url from <id>, doi from
<arxiv:doi> when present). Before this fix, Article.doi/url were always
None for arXiv results, making it impossible to verify which exact paper
a score was computed against.
"""
from bsi_benchmark.parsers.arxiv import ArxivParser

SAMPLE_FEED = """<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom"
      xmlns:arxiv="http://arxiv.org/schemas/atom">
  <entry>
    <id>http://arxiv.org/abs/2106.01234v2</id>
    <title>A Sample Paper Title</title>
    <summary>A sample abstract about large language models.</summary>
    <arxiv:doi>10.1000/sample.doi</arxiv:doi>
  </entry>
  <entry>
    <id>http://arxiv.org/abs/2107.05678v1</id>
    <title>A Second Paper Without DOI</title>
    <summary>Another sample abstract.</summary>
  </entry>
</feed>
"""


def test_arxiv_parser_extracts_url_for_every_entry():
    articles = ArxivParser().parse(SAMPLE_FEED)
    assert len(articles) == 2
    assert articles[0].url == "http://arxiv.org/abs/2106.01234v2"
    assert articles[1].url == "http://arxiv.org/abs/2107.05678v1"


def test_arxiv_parser_extracts_doi_when_present():
    articles = ArxivParser().parse(SAMPLE_FEED)
    assert articles[0].doi == "10.1000/sample.doi"


def test_arxiv_parser_doi_is_none_when_absent():
    articles = ArxivParser().parse(SAMPLE_FEED)
    assert articles[1].doi is None


def test_arxiv_parser_still_extracts_title_and_abstract():
    articles = ArxivParser().parse(SAMPLE_FEED)
    assert articles[0].title == "A Sample Paper Title"
    assert "large language models" in articles[0].abstract
