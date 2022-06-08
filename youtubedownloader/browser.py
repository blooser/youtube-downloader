from PySide6.QtCore import (
    QObject,
    QFileSystemWatcher,
    Qt,
    Signal,
    Slot,
    Property
)

from .logger import create_logger
from .models import WebTabsModel
from . import paths
from bs4 import BeautifulSoup

import os, os.path, json, lz4.block, subprocess, re
import urllib.request
import urllib.error

from youtubedownloader.logger import (
    create_logger
)


logger = create_logger(__name__)

YOUTUBE_PATTERN = re.compile("http(?:s?):\/\/(?:www\.)?youtu(?:be\.com\/watch\?v=|\.be\/)([\w\-\_]*)(&(amp;)?‌​[\w\?‌​=]*)?")


def collect(url, tag):
    items = []

    try:
        with urllib.request.urlopen(url) as response:
            data = response.read().decode("utf-8")
            soup = BeautifulSoup(data, "html.parser")

            items = soup.find_all(tag)

        logger.info(f"Collected {len(items)} items from {url}")

    except (urllib.error.URLError, ValueError) as err:
        logger.warning(err)

    return items


def is_youtube(url: str) -> re.Match:
    return YOUTUBE_PATTERN.match(url)


class BrowserTab(object):
    def __init__(self, url: str, title: str):
        self.url = url
        self.title = title

    def __eq__(self, other):
        return self.url == other.url


class Firefox(QObject):
    NAME: str = "Firefox"
    TABS_LOCATION_PATTERN: str = "~/.mozilla/firefox*/*.*/sessionstore-backups/recovery.jsonlz4"
    MOZILLA_MAGIC_NUMBER: int = 8 # NOTE: https://gist.github.com/mnordhoff/25e42a0d29e5c12785d0

    tabs_changed = Signal()

    def __init__(self):
        super(Firefox, self).__init__(None)

        self.logger = create_logger(__name__)
        self.tabs_model = WebTabsModel()
        self.file_expect = paths.FileExpect()

        self.detect()

        self.file_expect.file_exists.connect(self.get_tabs)

    def detect(self) -> None:
        self.tabs_location = paths.find_file(Firefox.TABS_LOCATION_PATTERN)

        if self.tabs_location:
            self.logger.info("Firefox detected={tabs_location}".format(tabs_location=(bool(self.tabs_location != ""))))

            self.tabs_file_watcher = QFileSystemWatcher()
            self.get_tabs(self.tabs_location)
            self.tabs_file_watcher.fileChanged.connect(self.get_tabs, Qt.QueuedConnection)

            self.detected = True
        else:
            self.detected = False

    @Slot(str)
    def get_tabs(self, path: str) -> None:
        tabs = []

        if not os.path.isfile(path):
            self.file_expect.observe(path)
            return

        if path not in (self.tabs_file_watcher.files()):
            self.tabs_file_watcher.addPath(self.tabs_location)

        with open(self.tabs_location, "rb") as tabs_file:
            mozilla_magic = tabs_file.read(Firefox.MOZILLA_MAGIC_NUMBER)
            j_data = json.loads(lz4.block.decompress(tabs_file.read()).decode("utf-8"))

        for window in j_data.get("windows"):
            for tab in window.get("tabs"):
                index = int(tab.get("index")) - 1

                if (is_youtube(tab.get("entries")[index].get("url"))):
                    tabs.append(BrowserTab(
                            tab.get("entries")[index].get("url"),
                            tab.get("entries")[index].get("title"))
                        )

        if (self.tabs_model.tabs != tabs):
            self.tabs_model.set_tabs(tabs)

    @Property(str)
    def name(self) -> str:
        return Firefox.NAME

    @Property(QObject)
    def tabs(self) -> WebTabsModel:
        return self.tabs_model


# TODO: Add Google Chrome and Opera... not sure it will be possible to do this same like Firefox

class Browsers(QObject):
    browsers_changed = Signal(list)

    def __init__(self):
        super(Browsers, self).__init__(None)

        self._browsers = []
        self.logger = create_logger(__name__)

        self.populate()

    @Slot()
    def populate(self) -> None:
        for browser in [Firefox()]:
            if browser.detected:
                self.browsers.append(browser)

        if len(self._browsers) == 0:
            self.logger.info("No any browser found")
        else:
            self.browsers_changed.emit(self.browsers)

    @Property("QVariantList", notify=browsers_changed)
    def browsers(self) -> list:
        return self._browsers

