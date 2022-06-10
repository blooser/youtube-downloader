from PySide6.QtCore import (
    QSortFilterProxyModel,
    QAbstractItemModel,
    QAbstractListModel,
    QModelIndex,
    Qt,
    QObject,
    Property,
    Signal,
    Slot
)

import youtubedownloader
import copy

from youtubedownloader.logger import (
    create_logger
)

from youtubedownloader.settings import Paths

from youtubedownloader.serializer import (
    Serializer
)

from PySide6.QtQml import QQmlParserStatus

from .database.models import History
from sqlalchemy.orm.session import Session

import uuid
import os
import pickle
import atexit


logger = create_logger("youtubedownloader.models")


class Item(QObject):
    updated = Signal(uuid.UUID)

    def __init__(self, roles, **kwargs):
        super().__init__(None)

        self.item_id = uuid.uuid4()
        logger.debug(f"New item with id={self.item_id} created")

        self.roles = roles

        for kwarg in kwargs:
            self.__dict__[kwarg] = kwargs[kwarg]

    def __getitem__(self, role):
        return self.__getattribute__(self.roles.get(role))

    def __setitem__(self, role, value):
        self.__dict__[self.roles.get(role)] = value

    def __eq__(self, item_id):
        return self.item_id == item_id

    def __repr__(self):
        return f"<Item {self.item_id}>"

    def update(self, data):
        for key in data:
            if data[key]:
                self.__dict__[key] = data[key]

        logger.info(f"{self} updated with {data}")

        self.updated.emit(self.item_id)


class Duplicate(QObject):
    changed = Signal()

    def __init__(self):
        super().__init__()

        self._url = str("")
        self._exists = False

    def scan(self, url, items):
        for item in items:
            self._exists = (item.info.url == url and url != "")

            print(item.info.url, url, self._exists)

            if self._exists:
                self._url = url

                break

        if not self._exists:
            self._url = ""

        self.changed.emit()

    @Property(str, notify = changed)
    def url(self):
        return self._url

    @Property(bool, notify = changed)
    def exists(self):
        return self._exists


class RoleNotFoundError(Exception):
    """Role was not found"""


class RoleNames(list):
    USER_ROLE = 256

    def __init__(self, *args):
        super().__init__(list(args))

    def __getattr__(self, value):
        return self.USER_ROLE + self.index(value)

    def to_dict(self):
        return { self.USER_ROLE + i: self[i].encode() for i in range(len(self)) }

    def get(self, role):
        try:
            return self[role - self.USER_ROLE]
        except IndexError:
            raise RoleNotFoundError()


class DataModel(QAbstractItemModel):
    ROLE_NAMES = RoleNames()

    itemRemoved = Signal(Item)
    itemPaused = Signal(Item)
    itemResumed = Signal(Item)

    def __init__(self):
        super().__init__(None)

        self.items = []

        self._duplicate = Duplicate()

    def __repr__(self):
        return f"<{self.__class__.__name__} items={self.rowCount()}>"

    def size(self):
        return len(self.items)

    def index(self, row, column, parent=QModelIndex()):
        return self.createIndex(row, column, parent)

    def parent(self, index):
        return QModelIndex()

    def rowCount(self, index=QModelIndex()):
        return len(self.items)

    def columnCount(self, index=QModelIndex()):
        return len(self.ROLE_NAMES)

    def roleNames(self, index=QModelIndex()):
        return self.ROLE_NAMES.to_dict()

    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsEditable

    def insert(self, *items):
        for item in items:
            item.roles = self.ROLE_NAMES
            item.updated.connect(self.update)

        self.beginInsertRows(QModelIndex(), self.size(), self.size() + len(items) - 1)
        self.items.extend(items)
        self.endInsertRows()

        logger.info(f"Inserted {len(items)} items")

    def reset(self):
        for item in self.items:
            item.updated.disconnect(self.update)

        self.beginResetModel()
        # NOTE: Don't clear() because another model will take these items
        self.items = []
        self.endResetModel()

    @Slot("QVariant")
    def remove(self, index):
        item = self.items[index]
        item.updated.disconnect(self.update)

        self.beginRemoveRows(QModelIndex(), index, index)
        del self.items[index]
        self.endRemoveRows()

        self.itemRemoved.emit(item)

    @Slot("QVariant")
    def pause(self, index):
        item = self.items[index]

        self.itemPaused.emit(item)

    @Slot("QVariant")
    def resume(self, index):
        item = self.items[index]

        self.itemResumed.emit(item)

    def dataRules(self, item, role):
        return item

    def data(self, index, role):
        if not index.isValid():
            return None

        try:
            return self.dataRules(self.items[index.row()][role], role)
        except Exception as err:
            return None

    def exists(self, item):
        return item in self.items

    @Slot(str)
    def scan(self, url):
        self._duplicate.scan(url, self.items)

    def setDataRules(self, item, value, role):
        return item

    def setData(self, index, value, role):
        if not index.isValid():
            return False

        item = self.items[index.row()]
        item[role] = self.setDataRules(item, value, role)

        topLeft = self.index(index.row(), 0)

        self.dataChanged.emit(
            topLeft,
            topLeft
        )

        logger.info(f"Item at index={index.row()} changed to {item[role]}")

        return True

    @Slot(uuid.UUID)
    def update(self, item_uuid):
        try:
            row = self.items.index(item_uuid)
        except ValueError:
            logger.warning(f"Failed to find Item ({item_id})")
            return

        topLeft = self.index(row, 0)

        self.dataChanged.emit(
            topLeft,
            topLeft
        )

        logger.info(f"Item at index={row} row updated")

    @Property(QObject, constant = True)
    def duplicate(self):
        return self._duplicate


class FreezeDataModel(DataModel):
    DATA_PATH = os.path.join(Paths.models, "models.json")

    def __init__(self):
        super().__init__()

        atexit.register(self.save)

        if os.path.isfile(self.DATA_PATH):
            self.load()

    def save(self):
        Serializer(Item).to_json(self.items, self.DATA_PATH)

    def load(self):
        items = Serializer(Item).from_json(self.DATA_PATH)
        self.insert(*items)


class PendingModel(FreezeDataModel):
    ROLE_NAMES = RoleNames("destination", "status", "info", "options")
    DATA_PATH = os.path.join(Paths.models, "pendingmodel.json")

    def __init__(self):
        super().__init__()

    def dataRules(self, item, role):
        return {
            256: lambda x: x,
            257: lambda x: x,
            258: lambda x: dict(x),
            # TODO: Make it solid! :)
            259: lambda x: x.to_dict()
        }[role](item)

    def setDataRules(self, item, value, role):
        return {
            256: lambda x: x,
            257: lambda x: x,
            258: lambda x: x,
            # FIXME: Deal with circular imports here
            259: lambda x: youtubedownloader.download.Options(**value.toVariant())
        }[role](item)

    def item(self, destination=None,
                   status="waiting",
                   info={},
                   options={},
                   progress = {}):
        return Item(
            self.ROLE_NAMES,
            destination = destination,
            status = status,
            info = info,
            options = options,
            progress = progress
        )


class DownloadModel(FreezeDataModel):
    ROLE_NAMES = RoleNames("destination", "status", "info", "options", "progress")
    DATA_PATH = os.path.join(Paths.models, "downloadmodel.json")

    def __init__(self):
        super().__init__()

    def dataRules(self, item, role):
        return {
            256: lambda x: x,
            257: lambda x: x,
            258: lambda x: dict(x),
            # TODO: Make it solid! :)
            259: lambda x: x.to_dict(),
            260: lambda x: dict(x)
        }[role](item)


class HistoryModel(DataModel):
    ROLE_NAMES = RoleNames("url", "title", "uploader", "uploader_url", "thumbnail", "date")

    rowsChanged = Signal()

    def __init__(self, session):
        super().__init__()

        self.session = session

        self.populate()

        self.rowsInserted.connect(self.rowsChanged)
        self.rowsRemoved.connect(self.rowsChanged)

    def insert(self, item):
        if self.session.query(History).filter_by(url=item.info.url).one_or_none() != None:
            return

        history_item = self.item_to_history(item)

        self.session.add(history_item)
        self.session.commit()

        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self.items.append(history_item)
        self.endInsertRows()

    def populate(self):
        self.items = self.session.query(History).all()

        logger.info(f"History model populated with {len(self.items)} items")

    @Slot(str)
    def remove(self, url):
        history_item = self.session.query(History).filter_by(url=url).one()

        self.session.delete(history_item)
        self.session.commit()

        index = self.items.index(history_item)

        self.beginRemoveRows(QModelIndex(), index, index)
        del self.items[index]
        self.endRemoveRows()

    def data(self, index, role):
        if not index.isValid():
            return None
        try:
            return self.items[index.row()].__getattribute__(self.ROLE_NAMES.get(role))
        except Exception as err:
            return None

    @Property(int, notify = rowsChanged)
    def size(self):
        return self.rowCount()

    def item_to_history(self, item):
        return History(
            url = item.info.url,
            title = item.info.title,
            uploader = item.info.uploader,
            uploader_url = item.info.uploader_url,
            thumbnail = item.info.thumbnail,
        )


class SupportedSitesModel(DataModel):
    SUPPORTED_SITES_URL = "https://ytdl-org.github.io/youtube-dl/supportedsites.html"

    ROLE_NAMES = RoleNames("name")

    rowsChanged = Signal()

    def __init__(self):
        super().__init__()

        self.populate()

        self.rowsInserted.connect(self.rowsChanged)
        self.rowsRemoved.connect(self.rowsChanged)

    @Property(int, notify = rowsChanged)
    def size(self):
        return self.rowCount()

    def populate(self):
        from youtubedownloader.browser import collect

        self.items = list(map(lambda tag: Item(roles=self.ROLE_NAMES, name=str(tag.b.string)), collect(self.SUPPORTED_SITES_URL, "li")))


class WebTabsModel(DataModel):
    ROLE_NAMES = RoleNames("url", "title")

    def __init__(self):
        super().__init__()

    def reset(self, tabs):
        self.beginResetModel()
        self.items = list(map(lambda tab: Item(self.ROLE_NAMES, url=tab.url, title=tab.title), tabs))
        self.endResetModel()


# NOTE: Proxy
# TODO: Modernize this!

class StringFilterModel(QSortFilterProxyModel, QQmlParserStatus):
    stringChanged = Signal(str, arguments=["string"])
    filterRoleNamesChanged = Signal("QVariantList", arguments=["filterRoleNames"])

    def __init__(self):
        super(StringFilterModel, self).__init__(None)

        self.setDynamicSortFilter(True)
        self.setFilterCaseSensitivity(Qt.CaseInsensitive)

        self._string = str()
        self._filter_role_names = []

    def classBegin(self) -> None:
        pass

    def componentComplete(self) -> None:
        pass

    def get_role(self, role):
        role_names = self.sourceModel().roleNames()

        for key in role_names:
            print(role_names[key], role)
            if role == role_names[key]:
                return key

    def filterAcceptsRow(self, source_row: int, source_parent: QModelIndex=QModelIndex()) -> bool:
        index = self.sourceModel().index(source_row, 0, source_parent)

        for role_name in self._filter_role_names:
            if self._string.lower() in self.sourceModel().data(index, self.get_role(role_name.encode())).lower():
                return True

        return False

    def read_filter_role_names(self) -> list:
        return self._filter_role_names

    def set_filter_role_names(self, new_filter_role_names: list) -> None:
        if len(new_filter_role_names) == 0:
            return

        self._filter_role_names = new_filter_role_names
        self.filterRoleNamesChanged.emit(self._filter_role_names)

    def read_string(self) -> str:
        return self.string

    def set_string(self, new_string: str) -> None:
        if self._string == new_string:
            return

        self._string = new_string
        self.stringChanged.emit(self._string)

        self.invalidateFilter()

    filterRoleNames = Property("QVariantList", read_filter_role_names, set_filter_role_names, notify=filterRoleNamesChanged)
    string = Property(str, read_string, set_string, notify=stringChanged)
