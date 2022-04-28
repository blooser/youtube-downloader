import pytest

from PySide6.QtTest import (
    QSignalSpy
)

from youtubedownloader.download import (
    Pending,
    PendingManager,
    TaskResult,
    Data,
    Transaction
)

from youtubedownloader.models import (
    PendingModel,
    Item
)


class TestItem:
    def test_item_populates_with_all_variables(self):
        roles = {
            256: b"url",
            257: b"title",
            258: b"status"
        }

        item = Item(roles, url="test", title="nice", status="ready")

        assert item.url == "test"
        assert item.title == "nice"
        assert item.status == "ready"

        assert item[256] == "test"
        assert item[257] == "nice"
        assert item[258] == "ready"


    def test_item_updates_itself(self):
        roles = {
            256: b"url",
            257: b"title",
            258: b"status"
        }

        item = Item(roles, url="test", title="nice", status="ready")

        assert item.url == "test"
        assert item.title == "nice"
        assert item.status == "ready"

        item.update(dict(status="finished"))

        assert item.url == "test"
        assert item.title == "nice"
        assert item.status == "finished"

        item.update(dict(url="newurl"))

        assert item.url == "newurl"


    def test_item_compares_with_id(self):
        roles = {
            256: b"url",
            257: b"title",
            258: b"status"
        }

        item = Item(roles, url="test", title="nice", status="ready")

        good_id = item.item_id
        bad_id = "badid"

        assert item == good_id
        assert item != bad_id


