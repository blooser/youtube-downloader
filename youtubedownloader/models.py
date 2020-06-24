# This Python file uses the following encoding: utf-8
from PySide2.QtCore import QSortFilterProxyModel, QAbstractItemModel, QModelIndex, Qt, Property, Signal, Slot
from PySide2.QtQml import QQmlParserStatus

from bs4 import BeautifulSoup

from .logger import create_logger

import urllib.request


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
        with urllib.request.urlopen(SupportedSitesModel.SUPPORTED_SITES_URL) as response:
            data = response.read().decode("utf-8")
            soup = BeautifulSoup(data, "html.parser")

            for tag in soup.find_all("li"):
                self.sites.append(tag.b.string)

        self.sizeChanged.emit(len(self.sites))

        self.logger.info("Collected {sites} sites".format(sites=len(self.sites)))

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


class StringFilterModel(QSortFilterProxyModel, QQmlParserStatus):
    stringChanged = Signal(str, arguments=["string"])
    filterRoleNameChanged = Signal(str, arguments=["filterRoleName"])

    def __init__(self):
        super(StringFilterModel, self).__init__(None)

        self.setDynamicSortFilter(True)
        self.setFilterCaseSensitivity(Qt.CaseInsensitive)

        self._string = str()
        self._filter_role_name = str()

        self.logger = create_logger(__name__)

        self.sourceModelChanged.connect(lambda: self.set_filter_role_if_need())

    def classBegin(self):
        pass

    def componentComplete(self):
        pass

    def set_filter_role_if_need(self):
        if self.sourceModel() == None:
            return;

        role_names = self.sourceModel().roleNames()
        for role in role_names:
            if role_names[role].decode() == self._filter_role_name:
                self.setFilterRole(role)

    def read_filter_role_name(self):
        return self._filter_role_name

    def set_filter_role_name(self, new_filter_role_name):
        if self._filter_role_name == new_filter_role_name or not new_filter_role_name:
            return

        self._filter_role_name = new_filter_role_name
        self.filterRoleNameChanged.emit(self._filter_role_name)

        self.set_filter_role_if_need()

    def read_string(self):
        return self.string

    def set_string(self, new_string):
        if self._string == new_string:
            return

        self._string = new_string
        self.stringChanged.emit(self._string)

        self.setFilterWildcard("*{string}*".format(string=self._string))

    filterRoleName = Property(str, read_filter_role_name, set_filter_role_name, notify=filterRoleNameChanged)
    string = Property(str, read_string, set_string, notify=stringChanged)
