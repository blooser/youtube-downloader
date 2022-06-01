import pytest

from youtubedownloader.models import (
    Item
)


from youtubedownloader.serializer import (
    Serializer,
    ItemSerializer,
    ItemJson
)

class ItemGood:
    def json(self):
        return {}

class ItemBad:
    def json(self):
        raise Exception("Bad item")


class TestSerializer:

    def test_serializer_creates_valid_instance(self):
        assert type(Serializer(Item) == ItemSerializer)

    def test_serializer_returns_none_if_invalid_class_type(self):
        assert type(Serializer(int) == None)
        assert type(Serializer(str) == None)
        assert type(Serializer(bool) == None)


    def test_item_json_filters_items_by_exception(self):
        items = [ItemGood(), ItemBad(), ItemBad(), ItemGood()]
        items = list(ItemJson(items))

        assert len(items) == 2
