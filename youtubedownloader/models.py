# This Python file uses the following encoding: utf-8
from PySide2.QtCore import QSortFilterProxyModel, QAbstractItemModel, QModelIndex, Qt, Property, Signal, Slot
from PySide2.QtQml import QQmlParserStatus

from bs4 import BeautifulSoup

from .logger import create_logger
from .settings import Settings
from .database.models import History

import urllib.request
import urllib.error


class HistoryModel(QAbstractItemModel):
    COLUMNS = ("url", "title", "uploader", "thumbnail", "date")
    FIRST_COLUMN = 0
    LAST_COLUMN = len(COLUMNS)

    sizeChanged = Signal(int, arguments=["size"])

    def __init__(self, session):
        super(HistoryModel, self).__init__(None)

        self.session = session
        self.items = []

        self.populate()

    @Slot(str, str, str, str, str)
    def add(self, url, title, uploader, uploader_url, thumbnail):
        if self.session.query(History).filter_by(url=url).one_or_none() == None:
            self.session.add(History(url=url, title=title, uploader=uploader, uploader_url=uploader_url, thumbnail=thumbnail))
            self.session.commit()
            self.populate()

    @Slot(str)
    def remove(self, url):
        item = self.session.query(History).filter_by(url=url).one()
        self.session.delete(item) # NOTE: Delete from database
        self.session.commit()

        index = self.items.index(item)
        self.beginRemoveRows(QModelIndex(), index, index)
        self.items.remove(item) # Note: Delete from model's data
        self.endRemoveRows()

        self.sizeChanged.emit(self.rowCount())

    @Property(int, notify=sizeChanged)
    def size(self):
        return len(self.items)

    def populate(self):
        self.beginResetModel()

        self.items = []
        for item in self.session.query(History).order_by(History.date.desc()).all():
            self.items.append(item)

        self.endResetModel()

        self.sizeChanged.emit(self.rowCount())

    def index(self, row, column, parent):
        return self.createIndex(row, column, parent)

    def roleNames(self, index=QModelIndex()):
        return {
            256: b"url",
            257: b"title",
            258: b"uploader",
            259: b"uploaderUrl",
            260: b"thumbnail",
            261: b"date"
        }

    def rowCount(self, index=QModelIndex()):
        return len(self.items)

    def columnCount(self, index=QModelIndex()):
        return SupportedSitesModel.LAST_COLUMN

    def data(self, index, role):
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

    COLUMNS = ("name")
    FIRST_COLUMN = 0
    LAST_COLUMN = len(COLUMNS)

    sizeChanged = Signal(int)

    def __init__(self):
        super(SupportedSitesModel, self).__init__(None)
        self.logger = create_logger(__name__)
        self.sites = []

        self.collect_sites()

    @Property(int, notify=sizeChanged)
    def size(self):
        return len(self.sites)

    def index(self, row, column, parent):
        return self.createIndex(row, column, parent)

    def collect_sites(self):
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

    def roleNames(self, index=QModelIndex()):
        return {
            256: b"name"
        }

    def rowCount(self, index=QModelIndex()):
        return len(self.sites)

    def columnCount(self, index=QModelIndex()):
        return SupportedSitesModel.LAST_COLUMN

    def data(self, index, role):
        if not index.isValid():
            return

        if role == 256:
            return self.sites[index.row()]

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

    def classBegin(self):
        pass

    def componentComplete(self):
        pass

    def get_role(self, role_name):
        role_names = self.sourceModel().roleNames()
        for role in self.sourceModel().roleNames():
            if role_names[role] == role_name:
                return role

        return None

    def filterAcceptsRow(self, source_row, source_parent):
        index = self.sourceModel().index(source_row, 0, source_parent)

        for role_name in self._filter_role_names:
            if self._string.lower() in self.sourceModel().data(index, self.get_role(role_name.encode())).lower():
                return True

        return False

    def read_filter_role_names(self):
        return self._filter_role_names

    def set_filter_role_names(self, new_filter_role_names: list):
        if len(new_filter_role_names) == 0:
            return

        self._filter_role_names = new_filter_role_names
        self.filterRoleNamesChanged.emit(self._filter_role_names)

    def read_string(self):
        return self.string

    def set_string(self, new_string):
        if self._string == new_string:
            return

        self._string = new_string
        self.stringChanged.emit(self._string)

        self.invalidateFilter()

    filterRoleNames = Property("QVariantList", read_filter_role_names, set_filter_role_names, notify=filterRoleNamesChanged)
    string = Property(str, read_string, set_string, notify=stringChanged)
