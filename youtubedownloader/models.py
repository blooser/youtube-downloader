from PySide2.QtCore import (
    QSortFilterProxyModel,
    QAbstractItemModel,
    QAbstractListModel,
    QModelIndex,
    Qt,
    Property,
    Signal,
    Slot
)
from PySide2.QtQml import QQmlParserStatus

from bs4 import BeautifulSoup

from .logger import create_logger
from .settings import Settings
from .database.models import History

from sqlalchemy.orm.session import Session

import urllib.request
import urllib.error


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
