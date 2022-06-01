import json

from youtubedownloader.logger import create_logger

logger = create_logger(__name__)



class ItemJson:
    def __init__(self, items):
        self.items = items

    def __iter__(self):
        for item in self.items:
            try:
                yield item.json()
            except Exception as err:
                logger.warning(f"Failed to convert {item} to json : {err}")

                continue

class ItemInfoPicker:
    def __new__(cls, content, status):
        from youtubedownloader.download import Data, Error

        if status == "error":
            return Error(**content)

        return Data(**content)


class ItemSerializer:
    def __init__(self):
        ...

    def to_json(self, items, path):
        items = list(ItemJson(items))

        with open(path, "w") as f:
            json.dump(items, f)

        logger.info(f"Saved {len(items)} items to {path}")

    def from_json(self, path):
        with open(path, "r") as f:
            items = json.load(f)

        for item in items:
            from youtubedownloader.download import Data, Error, Options
            from youtubedownloader.models import Item

            item["info"] = ItemInfoPicker(item["info"], item["status"])
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


