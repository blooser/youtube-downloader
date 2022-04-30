import pytest

from PySide6.QtTest import (
    QSignalSpy
)

from youtubedownloader.download import (
    Pending,
    TaskResult,
    Data,
    Transaction
)

from youtubedownloader.models import (
    PendingModel,
    DownloadModel,
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


    def test_item_assigment_operator_works_correctly(self):
        roles = {
            256: b"title"
        }

        item = Item(roles, title="title")

        assert item[256] == "title"

        item[256] = "another title"

        assert item[256] == "another title"
        
    def test_download_model_puts_multiple_items(self):
        download_model = DownloadModel()

        assert download_model.rowCount() == 0

        # NOTE: Be careful here because of dataRules()...
        tmp_d = dict(destination=None, status=None, info=None, options=None, progress=None)
        items = [Item(download_model.ROLE_NAMES) for _ in range(5)]

        download_model.insertMultiple(items)

        assert download_model.rowCount() == len(items)
        assert download_model.items == items

