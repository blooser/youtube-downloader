import json

from youtubedownloader.logger import create_logger

logger = create_logger(__name__)


class ItemAttribute:
    attributes = (
        "roles",
        "destination",
        "status",
        "info",
        "options",
        "progress"
    )

    def __init__(self, mode="write"):
        self.mode = mode

    def __call__(self, name, value):
        return getattr(self, name)(value)

    def roles(self, x):
        return x

    def destination(self, x):
        return x

    def status(self, x):
        return x

    def info(self, x):
        if self.mode == "write":
            return dict(x)

        from youtubedownloader.download import Data, Error

        if "error" in x:
            return Error(**x)

        return Data(**x)

    def options(self, x):
        if self.mode == "write":
            return x.to_dict()

        from youtubedownloader.download import Options

        return Options(**x)

    def progress(self, x):
        if self.mode == "write":
            return dict(x)

        from youtubedownloader.download import ProgressData

        return ProgressData(**x)


class ItemSerializer:

    def __init__(self):
        ...

    def to_json(self, items, path):
        items = list(map(self.item_to_json, items))

        with open(path, "w") as f:
            json.dump(items, f)

        logger.info(f"Saved {len(items)} items to {path}")

    def from_json(self, path):
        with open(path, "r") as f:
            items = json.load(f)

        items = list(map(self.item_from_json, items))

        logger.info(f"Loaded {len(items)} from {path}")

        return items

    def item_to_json(self, item):
        d = dict()

        item_attribute = ItemAttribute(mode="write")

        for attribute in item_attribute.attributes:
            try:
                d[attribute] = item_attribute(attribute, item.__getattribute__(attribute))
            except (AttributeError, KeyError) as err:
                continue

        return d

    def item_from_json(self, d):
        item_attribute = ItemAttribute(mode="read")

        for attribute in item_attribute.attributes:
            try:
                d[attribute] = item_attribute(attribute, d[attribute])
            except (AttributeError, KeyError) as err:
                continue

        from youtubedownloader.models import Item

        return Item(**d)


class Serializer:
    def __new__(cls, class_to_serialize):
        try:
            return cls.serializers()[class_to_serialize]()
        except KeyError:
            return None

    def serializers():
        from youtubedownloader.models import Item

        return {
            Item: ItemSerializer
        }


