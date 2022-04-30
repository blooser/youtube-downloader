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
    Item,
    RoleNames
)


class TestItem:
    def test_item_populates_with_all_variables(self):
        roles = RoleNames("url", "title", "status")

        item = Item(roles, url="test", title="nice", status="ready")

        assert item.url == "test"
        assert item.title == "nice"
        assert item.status == "ready"

        assert item[256] == "test"
        assert item[257] == "nice"
        assert item[258] == "ready"


    def test_item_updates_itself(self):
        roles = RoleNames("url", "title", "status") 
        
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
        roles = RoleNames("url", "title", "status")        

        item = Item(roles, url="test", title="nice", status="ready")

        good_id = item.item_id
        bad_id = "badid"

        assert item == good_id
        assert item != bad_id


    def test_item_assigment_operator_works_correctly(self):
        roles = RoleNames("title")

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

        download_model.insert(*items)

        assert download_model.rowCount() == len(items)
        assert download_model.items == items

    @pytest.mark.parametrize(
        "roles, numbers", [
            (
                ["destination", "status", "info", "options"],
                [256, 257, 258, 259]
            ),
            (
                ["destination", "status", "info", "options", "progress"],
                [256, 257, 258, 259, 260]    
            )
        ]
    )
    def test_rolenames_can_uses_getattr_operator(self, roles, numbers):
        role_names = RoleNames(*roles)

        for role, number in zip(roles, numbers):
            assert role_names.__getattr__(role) == number


    @pytest.mark.parametrize(
        "roles, expected_dict", [
            (
                ["destination", "status", "info", "options"],
                {
                    256: b"destination",
                    257: b"status",
                    258: b"info",
                    259: b"options"
                }
            ),
            (
                ["destination", "status", "info", "options", "progress"],
                {
                    256: b"destination",
                    257: b"status",
                    258: b"info",
                    259: b"options",
                    260: b"progress"
                }
            ),
        ]
    )
    def test_rolenames_can_be_casted_to_dict(self, roles, expected_dict):
        role_names = RoleNames(*roles) 

        assert role_names.to_dict() == expected_dict

    def test_rolenames_returns_value_with_get_method(self):
        role_names = RoleNames("destination", "title")

        assert role_names.get(256) == "destination"
        assert role_names.get(257) == "title"
