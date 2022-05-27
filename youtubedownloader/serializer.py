import json

from youtubedownloader.logger import create_logger

logger = create_logger(__name__)


class ItemSerializer:
    def __init__(self):
        ...

    def to_json(self, items, path):
        items = [item.json() for item in items]

        with open(path, "w") as f:
            json.dump(items, f)

        logger.info(f"Saved {len(items)} items to {path}")

    def from_json(self, path):
        with open(path, "r") as f:
            items = json.load(f)

        for item in items:
            from youtubedownloader.download import Data, Options
            from youtubedownloader.models import Item

            item["info"] = Data(**item["info"])
            item["options"] = Options(**item["options"])

        items = list(map(lambda x: Item(**x), items))

        logger.info(f"Loaded {len(items)} from {path}")

        return items



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


