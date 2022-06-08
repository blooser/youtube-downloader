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

class Browser(QObject):
    NAME = "Unknown"
    PATH = "Unknown"

    tabsChanged = Signal()

    def __init__(self):
        super().__init__(None)

        self.model = WebTabsModel()

        self.file_expect = paths.FileExpect()
        self.file_expect.file_exists.connect(self.collect_tabs)

        self.file_watcher = QFileSystemWatcher()
        self.file_watcher.fileChanged.connect(self.collect_tabs, Qt.QueuedConnection)

        self.detect()

        if self.localization:
            self.collect_tabs(self.localization)

    def detect(self):
        self.localization = paths.find_file(self.PATH)

        if self.localization:
            logger.info(f"{self.NAME} detected")

    def set_tabs(self, tabs):
        self.model.reset(tabs)

    @Slot(str)
    def collect_tabs(self, path):
        return NotImplemented

    @Property(str)
    def name(self):
        return self.NAME

    @Property(QObject)
    def tabs(self):
        return self.model


class Firefox(Browser):
    NAME = "Firefox"
    PATH = "~/.mozilla/firefox*/*.*/sessionstore-backups/recovery.jsonlz4"

    MOZILLA_MAGIC_NUMBER: int = 8 # NOTE: https://gist.github.com/mnordhoff/25e42a0d29e5c12785d0

    def __init__(self):
        super().__init__()

    @Slot(str)
    def collect_tabs(self, path: str) -> None:
        tabs = []

        if not os.path.isfile(path):
            self.file_expect.observe(path)
            return

        if path not in (self.file_watcher.files()):
            self.file_watcher.addPath(self.localization)

        with open(self.localization, "rb") as tabs_file:
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

        self.set_tabs(tabs)


# TODO: Add Google Chrome and Opera... not sure it will be possible to do this same like Firefox

class Browsers(QObject):
    browsers_changed = Signal(list)

    def __init__(self):
        super(Browsers, self).__init__(None)

        self._browsers = []

        self.populate()

    @Slot()
    def populate(self) -> None:
        for browser in [Firefox()]:
            if browser.localization:
                self._browsers.append(browser)

        if len(self._browsers) == 0:
            logger.warning("No any browser found")
        else:
            self.browsers_changed.emit(self.browsers)

    @Property("QVariantList", notify=browsers_changed)
    def browsers(self) -> list:
        return self._browsers

