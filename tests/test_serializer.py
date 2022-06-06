import pytest

from youtubedownloader.models import (
    Item,
    RoleNames
)


from youtubedownloader.serializer import (
    Serializer,
    ItemSerializer,
)

from youtubedownloader.download import (
    Pending,
    Options
)


class TestSerializer:

    def test_serializer_creates_valid_instance(self):
        assert type(Serializer(Item) == ItemSerializer)

    def test_serializer_returns_none_if_invalid_class_type(self):
        assert type(Serializer(int) == None)
        assert type(Serializer(str) == None)
        assert type(Serializer(bool) == None)

    def test_serializer_converts_items_to_json(self):
        pending = Pending("https://www.youtube.com/watch?v=tLsJQ5srVQA")
        pending.start()
        pending.wait()

        item = Item (
            roles = RoleNames("destination", "status", "info", "options"),
            destination = "home",
            status = "finished",
            info = pending.result.value,
            options = Options(output="documents", format="mp3")
        )

        serializer = Serializer(Item)

        item_json = serializer.item_to_json(item)

        assert type(item_json) == dict
        assert len(item_json.keys()) == 5
        assert item_json["destination"] == "home"
        assert item_json["status"] == "finished"
        assert item_json["info"] == dict(pending.result.value)
        assert item_json["options"] == dict(output="documents", format="mp3")

        item1 = serializer.item_from_json(item_json)
        
        assert type(item1) == Item
        assert item1.destination == item.destination
        assert item1.status == item.status
        assert item1.info == item.info
        assert item1.options == item.options
     
