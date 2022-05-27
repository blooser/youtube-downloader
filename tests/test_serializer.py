import pytest

from youtubedownloader.models import (
    Item
)


from youtubedownloader.serializer import (
    Serializer,
    ItemSerializer
)

class TestSerializer:

    def test_serializer_creates_valid_instance(self):
        assert type(Serializer(Item) == ItemSerializer)

    def test_serializer_returns_none_if_invalid_class_type(self):
        assert type(Serializer(int) == None)
        assert type(Serializer(str) == None)
        assert type(Serializer(bool) == None)

