import pytest
import os
import os.path
import atexit

from PySide6.QtTest import (
    QSignalSpy
)

from PySide6.QtCore import (
    QModelIndex
)

from youtubedownloader.download import (
    Pending,
    TaskResult,
    Data,
    Transaction,
    Options
)

from youtubedownloader.models import (
    FreezeDataModel,
    PendingModel,
    DownloadModel,
    Item,
    RoleNames,

    HistoryModel,
    
    RoleNotFoundError,
)

from youtubedownloader.settings import (
    Paths
)

from youtubedownloader.database import (
    Database
)

from youtubedownloader.models import (
    History
)


class FreezeDataModelFixture(FreezeDataModel):
    DATA_PATH = os.path.join(Paths.models, "testmodel.json")

    def __init__(self):
        super().__init__()

    def clean(self):
        atexit.unregister(self.save)

        if os.path.isfile(self.DATA_PATH):
            os.remove(self.DATA_PATH)

class PendingModelFixture(PendingModel):
    def __init__(self):
        super().__init__()

    def load(self):
        ...

    def save(self):
        ...


class DownloadModelFixture(DownloadModel):
    def __init__(self):
        super().__init__()

    def load(self):
        ...

    def save(self):
        ...





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

    
    def test_item_deals_with_empty_values(self):
        roles = RoleNames("url", "title")
        info = {"title": "test", "number": 25}

        item = Item(roles, url="path", info=info)
        
        assert item.url == "path"
        assert item.info == info

        item.update({
            "ur": "",
            "info": {}
        })

        assert item.url == "path"
        assert item.info == info


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
        download_model = DownloadModelFixture()

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

    def test_rolenames_raises_role_not_found_exception(self):
        role_names = RoleNames("destination", "title")

        with pytest.raises(RoleNotFoundError):
            role_names.get(258)


def test_freeze_model_serialize_data():
    pending = Pending("https://www.youtube.com/watch?v=tLsJQ5srVQA")
    pending.start()
    pending.wait()

    item = Item (
        roles = RoleNames("title", "url"),
        destination = "home",
        status = "finished",
        info = pending.result.value,
        options = Options(output="documents", format="mp3"),
        progress = {}
    )

    model = FreezeDataModelFixture()
    model.items = [item]

    model.save()
    assert os.path.isfile(model.DATA_PATH)
    
    model2 = FreezeDataModelFixture() # NOTE: This invokes load() when creating instance 
    assert len(model2.items) > 0

    item2 = model2.items[0]

#    assert item.roles == item2.roles
    assert item.destination == item2.destination
    assert item.status == item2.status
    assert item.info == item2.info
    assert item.options == item2.options

    model.clean()
    model2.clean()

    assert not os.path.isfile(model.DATA_PATH)


def test_data_model_can_scan():
    model = DownloadModelFixture()

    item = Item (
        roles = RoleNames("title", "url"),
        destination = "home",
        status = "finished",
        info = None,
        options = Options(output="documents", format="mp3"),
        progress = {}
    )

    model.items = [item]
    pattern = dict(destination="home", status="finished")

    assert model.scan(pattern)

    pattern = dict(destination="home", status="paused")

    assert not model.scan(pattern)


def test_model_exists_functions_works_correctly():
    model = DownloadModelFixture()
    
    roles = RoleNames("info")

    pending = Pending("https://www.youtube.com/watch?v=tLsJQ5srVQA")
    pending.start()
    pending.wait()

    item1 = Item(roles, info=pending.result.value)
    item2 = Item(roles, info=pending.result.value)
    item3 = Item(roles, info=pending.result.value)

    model.items = [item1, item2]

    assert model.exists(item1)
    assert model.exists(item2)
    assert not model.exists(item3)


def test_history_models_inserts_items():
    db = Database(":memory:")
    history_model = HistoryModel(db.session)

    roles = RoleNames("info")

    pending = Pending("https://www.youtube.com/watch?v=tLsJQ5srVQA")
    pending.start()
    pending.wait()

    item1 = Item(roles, info=pending.result.value)
    item2 = Item(roles, info=pending.result.value)
    item3 = Item(roles, info=pending.result.value)


    history_model.insert(item1)
    history_model.insert(item1)

    history_model.insert(item2)
    history_model.insert(item2)

    history_model.insert(item3)
    history_model.insert(item3)

    assert history_model.rowCount() == 1 
    assert type(history_model.items[0]) == History
    #assert history_model.data(history_model.index(0, 0), 256) == pending.url


def test_history_models_is_able_to_remove_item():
    db = Database(":memory:")
    history_model = HistoryModel(db.session)

    roles = RoleNames("info")

    pending = Pending("https://www.youtube.com/watch?v=tLsJQ5srVQA")
    pending.start()
    pending.wait()

    item1 = Item(roles, info=pending.result.value)

    history_model.insert(item1)

    assert history_model.rowCount() == 1 
    
    history_model.remove(pending.url)
   
    assert history_model.rowCount() == 0
