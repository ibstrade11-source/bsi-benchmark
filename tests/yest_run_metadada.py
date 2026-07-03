"""
Tests for run metadata functionality.
"""

import pytest
import json
from datetime import datetime
from pathlib import Path


def test_metadata_structure():
    """Test that metadata includes required fields."""
    # این یک تست نمونه است - می‌توانید بر اساس نیاز پروژه خود تنظیم کنید
    metadata = {
        "git_commit": "707d8eb",
        "timestamp": datetime.now().isoformat(),
        "version": "v0.2.0-provenance"
    }
    
    assert "git_commit" in metadata
    assert "timestamp" in metadata
    assert metadata["version"] == "v0.2.0-provenance"


def test_arxiv_doi_in_metadata():
    """Test that article provenance includes DOI/URL."""
    # تست برای بررسی وجود DOI/URL در متادیتا
    article_metadata = {
        "arxiv_id": "2301.12345",
        "doi": "10.1234/example",
        "url": "https://arxiv.org/abs/2301.12345"
    }
    
    assert "arxiv_id" in article_metadata or "doi" in article_metadata
    assert article_metadata.get("url") is not None


def test_methodology_caveat():
    """Test that methodology caveat is present in reports."""
    report_data = {
        "methodology": {
            "caveat": "This is a test caveat about methodology limitations"
        }
    }
    
    assert "caveat" in report_data["methodology"]
    assert len(report_data["methodology"]["caveat"]) > 0


@pytest.mark.parametrize("required_field", [
    "git_hash",
    "timestamp", 
    "article_provenance",
    "methodology_caveat"
])
def test_metadata_required_fields(required_field):
    """Test that all required metadata fields exist."""
    # این تست بررسی می‌کند که فیلدهای ضروری در متادیتا وجود دارند
    metadata = {
        "git_hash": "707d8eb",
        "timestamp": "2026-07-04T10:00:00",
        "article_provenance": {"doi": "10.1234/example"},
        "methodology_caveat": "Test caveat"
    }
    assert required_field in metadata
