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

from youtubedownloader.logger import (
    create_logger
)

import youtubedownloader.download

from PySide6.QtQml import QQmlParserStatus
from bs4 import BeautifulSoup
from .database.models import History
from sqlalchemy.orm.session import Session

import urllib.request
import urllib.error
import uuid


logger = create_logger("youtubedownloader.models")


class Item(QObject):
    updated = Signal(uuid.UUID)

    def __init__(self, roles, **kwargs):
        super().__init__(None)

        self.item_id = uuid.uuid4()
        logger.info(f"New item with id={self.item_id} created")

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
            self.__dict__[key] = data[key]

        logger.info(f"{self} updated with {data}")

        self.updated.emit(self.item_id)


class RoleNames(list):
    USER_ROLE = 256

    def __init__(self, *args):
        super().__init__(list(args))

    def __getattr__(self, value):
        return self.USER_ROLE + self.index(value)

    def to_dict(self):
        return { self.USER_ROLE + i: self[i].encode() for i in range(len(self)) }

    def get(self, role):
        return self[role - self.USER_ROLE]



class DataModel(QAbstractItemModel):
    ROLE_NAMES = RoleNames()

    itemRemoved = Signal(Item)

    def __init__(self):
        super().__init__(None)

        self.items = []

    def __repr__(self):
        return f"<{self.__class__.__name__} items={self.rowCount()}>"

    def size(self):
        return len(self.items)

    def index(self, row, column, parent=QModelIndex()):
        return self.createIndex(row, column, parent)

    def parent(self, index):
        return QModelIndex()

    def rowCount(self, index=QModelIndex()):
        return self.size()

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

    def dataRules(self, item, role):
        return item

    def data(self, index, role):
        if not index.isValid():
            return None

        try:
            return self.dataRules(self.items[index.row()][role], role)
        except Exception as err:
            return None

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


class PendingModel(DataModel):
    ROLE_NAMES = RoleNames("destination", "status", "info", "options")

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


class DownloadModel(DataModel):
    ROLE_NAMES = RoleNames("destination", "status", "info", "options", "progress")

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



class HistoryModel(QAbstractItemModel):
    COLUMNS: tuple = ("url", "title", "uploader", "thumbnail", "date")
    FIRST_COLUMN: int = 0
    LAST_COLUMN: int = len(COLUMNS)

    sizeChanged = Signal(int, arguments=["size"])

    def __init__(self, session: Session):
        super(HistoryModel, self).__init__(None)

        self.session = session
        self.items = []

        self.populate()

    @Property(int, notify=sizeChanged)
    def size(self) -> int:
        return len(self.items)

    @Slot(str, str, str, str, str)
    def add(self, url: str, title: str, uploader: str, uploader_url: str, thumbnail: str) -> None:
        if self.session.query(History).filter_by(url=url).one_or_none() == None:
            self.session.add(History(url=url, title=title, uploader=uploader, uploader_url=uploader_url, thumbnail=thumbnail))
            self.session.commit()
            self.populate()

    @Slot(str)
    def remove(self, url: str) -> None:
        item = self.session.query(History).filter_by(url=url).one()
        self.session.delete(item) # NOTE: Delete from database
        self.session.commit()

        index = self.items.index(item)
        self.beginRemoveRows(QModelIndex(), index, index)
        self.items.remove(item) # Note: Delete from model's data
        self.endRemoveRows()

        self.sizeChanged.emit(self.rowCount())

    def populate(self) -> None:
        self.beginResetModel()

        self.items = []
        for item in self.session.query(History).order_by(History.date.desc()).all():
            self.items.append(item)

        self.endResetModel()

        self.sizeChanged.emit(self.rowCount())

    def index(self, row: int, column: int, parent: QModelIndex=QModelIndex()) -> QModelIndex:
        return self.createIndex(row, column, parent)

    def roleNames(self, index: QModelIndex=QModelIndex()) -> dict:
        return {
            256: b"url",
            257: b"title",
            258: b"uploader",
            259: b"uploaderUrl",
            260: b"thumbnail",
            261: b"date"
        }

    def rowCount(self, index: QModelIndex=QModelIndex()) -> int:
        return len(self.items)

    def columnCount(self, index: QModelIndex=QModelIndex()) -> int:
        return SupportedSitesModel.LAST_COLUMN

    def data(self, index: QModelIndex, role: int):
        if not index.isValid():
            return

        item = self.items[index.row()]

        if role == 256:
            return item.url

        elif role == 257:
            return item.title

        elif role == 258:
            return item.uploader

        elif role == 259:
            return item.uploader_url

        elif role == 260:
            return item.thumbnail

        elif role == 261:
            return item.date


class SupportedSitesModel(QAbstractItemModel):
    SUPPORTED_SITES_URL = "https://ytdl-org.github.io/youtube-dl/supportedsites.html"

    COLUMNS: str = ("name")
    FIRST_COLUMN: int = 0
    LAST_COLUMN: int = len(COLUMNS)

    sizeChanged = Signal(int)

    def __init__(self):
        super(SupportedSitesModel, self).__init__(None)
        self.logger = create_logger(__name__)
        self.sites = []

        self.collect_sites()

    @Property(int, notify=sizeChanged)
    def size(self) -> int:
        return len(self.sites)

    def index(self, row: int, column: int, parent: QModelIndex=QModelIndex()) -> QModelIndex:
        return self.createIndex(row, column, parent)

    def collect_sites(self) -> None:
        try:
            with urllib.request.urlopen(SupportedSitesModel.SUPPORTED_SITES_URL) as response:
                data = response.read().decode("utf-8")
                soup = BeautifulSoup(data, "html.parser")

                for tag in soup.find_all("li"):
                    self.sites.append(tag.b.string)

            self.sizeChanged.emit(len(self.sites))

            self.logger.info("Collected {sites} sites".format(sites=len(self.sites)))

        except urllib.error.URLError as err:
            self.logger.warning(str(err))

    def roleNames(self, index: QModelIndex=QModelIndex()) -> dict:
        return {
            256: b"name"
        }

    def rowCount(self, index: QModelIndex=QModelIndex()) -> int:
        return len(self.sites)

    def columnCount(self, index: QModelIndex=QModelIndex()) -> int:
        return SupportedSitesModel.LAST_COLUMN

    def data(self, index: QModelIndex, role: int):
        if not index.isValid():
            return

        if role == 256:
            return self.sites[index.row()]


class WebTabsModel(QAbstractListModel):
    COLUMNS: str = ("url", "title")
    FIRST_COLUMN: int = 0
    LAST_COLUMN: int = len(COLUMNS)

    def __init__(self):
        super(WebTabsModel, self).__init__(None)
        self.tabs = []

    def rowCount(self, index: QModelIndex=QModelIndex()) -> int:
        return len(self.tabs)

    def columnCount(self, index: QModelIndex=QModelIndex()) -> int:
        return WebTabsModel.LAST_COLUMN

    def parent(index: QModelIndex=QModelIndex()) -> QModelIndex:
        return QModelIndex()

    def roleNames(self, index: QModelIndex=QModelIndex()) -> dict:
        return {
            256: b"url",
            257: b"title"
        }

    def index(self, row: int, column: int, parent: QModelIndex=QModelIndex()) -> QModelIndex:
        return self.createIndex(row, column, parent)

    def data(self, index: QModelIndex, role: int):
        if not index.isValid():
            return

        tab = self.tabs[index.row()]

        if role == 256:
            return tab.url

        elif role == 257:
            return tab.title

    def set_tabs(self, new_tabs: list) -> None:
        if (not self.rowCount()):
            self.beginResetModel()
            self.tabs = new_tabs
            self.endResetModel()

        else:
            self.beginRemoveRows(QModelIndex(), 0, len(self.tabs) - 1)
            self.tabs.clear()
            self.endRemoveRows()

            self.beginInsertRows(QModelIndex(), 0, len(new_tabs) - 1)
            self.tabs = new_tabs
            self.endInsertRows()






# NOTE: Proxy

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

    def get_role(self, role_name: str) -> int:
        role_names = self.sourceModel().roleNames()
        for role in self.sourceModel().roleNames():
            if role_names[role] == role_name:
                return role

        return -1

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
