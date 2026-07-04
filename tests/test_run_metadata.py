"""
Tests for bsi_benchmark.run_metadata.RunMetadata.
"""
import re

from bsi_benchmark.run_metadata import RunMetadata, METHODOLOGY_NOTE


def test_capture_returns_tool_version():
    meta = RunMetadata.capture()
    assert meta.tool_version == "0.1.0"


def test_capture_returns_iso8601_utc_timestamp():
    meta = RunMetadata.capture()
    assert re.match(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$", meta.run_timestamp_utc)


def test_capture_includes_methodology_note():
    meta = RunMetadata.capture()
    assert meta.methodology_note == METHODOLOGY_NOTE
    assert "not a validated measurement" in meta.methodology_note


def test_git_commit_is_none_or_40_char_hex_when_not_a_repo(tmp_path):
    # Running in a directory that is not a git repo: git_commit must be
    # None, never a silently-wrong empty string or stale value.
    meta = RunMetadata.capture(repo_dir=str(tmp_path))
    assert meta.git_commit is None
    assert meta.git_dirty is None


def test_git_commit_is_real_hash_inside_this_repo():
    import os
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    meta = RunMetadata.capture(repo_dir=here)
    if meta.git_commit is not None:
        assert re.match(r"^[0-9a-f]{40}$", meta.git_commit)
