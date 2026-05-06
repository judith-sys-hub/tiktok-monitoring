"""Tests for monitor.py — written before fixes (TDD)."""
import json
import urllib.error
from unittest.mock import patch, MagicMock

import pytest

from monitor import score, post_to_teams


# ---------------------------------------------------------------------------
# score() — must not raise KeyError when a weight key is missing from config
# ---------------------------------------------------------------------------

def test_score_does_not_crash_when_weight_key_missing():
    """Missing weight key should default to 0, not raise KeyError."""
    video = {"stats": {"playCount": 1000, "diggCount": 500, "shareCount": 100}}
    incomplete_weights = {"views": 0.5}  # missing 'likes' and 'shares'
    result = score(video, incomplete_weights)
    assert result == 500.0  # 1000 * 0.5 + 0 + 0


def test_score_returns_zero_for_missing_stats():
    """Missing stats fields should default to 0, not crash."""
    video = {}  # no 'stats' key at all
    weights = {"views": 0.5, "likes": 0.3, "shares": 0.2}
    result = score(video, weights)
    assert result == 0.0


# ---------------------------------------------------------------------------
# post_to_teams() — must retry on transient HTTP errors
# ---------------------------------------------------------------------------

def _make_output(n_videos=3):
    videos = [
        {
            "rank": i + 1,
            "title": f"Video {i+1}",
            "views": "1K",
            "region": "Steiermark",
            "account": f"user{i}",
        }
        for i in range(n_videos)
    ]
    return {"videos": videos}


def test_post_to_teams_retries_on_http_error():
    """A single transient failure should not drop the notification — must retry."""
    call_count = 0

    def flaky_urlopen(req, timeout):
        nonlocal call_count
        call_count += 1
        if call_count < 3:
            raise urllib.error.URLError("temporary failure")
        return MagicMock()  # success on 3rd attempt

    with patch("monitor.urllib.request.urlopen", side_effect=flaky_urlopen):
        post_to_teams("https://example.webhook", _make_output())

    assert call_count == 3, f"Expected 3 attempts, got {call_count}"


def test_post_to_teams_raises_after_max_retries():
    """After exhausting all retries, the error should propagate."""
    with patch("monitor.urllib.request.urlopen", side_effect=urllib.error.URLError("down")):
        with pytest.raises(urllib.error.URLError):
            post_to_teams("https://example.webhook", _make_output())
