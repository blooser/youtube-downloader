import pytest

from youtubedownloader.browser import (
    collect
)


def test_collect_collects_items_from_url():
    items = collect("https://ytdl-org.github.io/youtube-dl/supportedsites.html" ,"li")

    assert len(items) > 1000 # NOTE: yd-downloader supports more then 1000 urls


def test_collect_collects_empty_if_invalid_input_data():
    items = collect("test", "body")

    assert len(items) == 0
