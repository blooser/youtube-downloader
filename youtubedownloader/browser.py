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
    detectedChanged = Signal(bool)

    def __init__(self):
        super().__init__(None)

        self.model = WebTabsModel()

        self.file_expect = paths.FileExpect()
        self.file_expect.file_exists.connect(self.fileExists)

        self.file_watcher = QFileSystemWatcher()
        self.file_watcher.fileChanged.connect(self.browser_tabs_changed, Qt.QueuedConnection)

        self._detected = False
        self.detect()

    def detect(self):
        if localization := self.find():
            logger.info(f"{self.NAME} detected")

            self.browser_tabs_changed(localization)

            self._detected = True
            self.detectedChanged.emit(self._detected)

            return

        self.file_expect.expect(self.PATH)

    def find(self):
        return paths.find_file(self.PATH)

    def set_tabs(self, tabs):
        self.model.reset(tabs)

    def collect_tabs(self, path):
        return NotImplemented

    def wait_for(self, path):
        while not os.path.isfile(path):
            continue

    @Slot(str)
    def fileExists(self, path):
        self._detected = True
        self.detectedChanged.emit(self._detected)

        self.browser_tabs_changed(path)

    @Slot(str)
    def browser_tabs_changed(self, path):
        # NOTE: This slot is a little bit faster than the filesystem operation
        self.wait_for(path)

        self.file_watcher.addPath(path)

        self.collect_tabs(path)

    @Property(str, constant = True)
    def name(self):
        return self.NAME

    @Property(QObject, constant = True)
    def tabs(self):
        return self.model

    @Property(bool, notify = detectedChanged)
    def detected(self):
        return self._detected


class Firefox(Browser):
    NAME = "Firefox"
    PATH = "~/.mozilla/firefox*/*.*/sessionstore-backups/recovery.jsonlz4"

    MOZILLA_MAGIC_NUMBER: int = 8 # NOTE: https://gist.github.com/mnordhoff/25e42a0d29e5c12785d0

    def __init__(self):
        super().__init__()

    def collect_tabs(self, path):
        tabs = []

        with open(path, "rb") as tabs_file:
            mozilla_magic = tabs_file.read(Firefox.MOZILLA_MAGIC_NUMBER)
            j_data = json.loads(lz4.block.decompress(tabs_file.read()).decode("utf-8"))

        for window in j_data.get("windows"):
            for tab in window.get("tabs"):
                index = int(tab.get("index")) - 1

                if (Browsers.is_youtube(tab.get("entries")[index].get("url"))):
                    tabs.append(BrowserTab(
                            tab.get("entries")[index].get("url"),
                            tab.get("entries")[index].get("title"))
                        )

        self.set_tabs(tabs)


# TODO: Add Google Chrome and Opera... not sure it will be possible to do this same like Firefox

class Browsers(QObject):
    PATTERN = re.compile("http(?:s?):\/\/(?:www\.)?youtu(?:be\.com\/watch\?v=|\.be\/)([\w\-\_]*)(&(amp;)?‌​[\w\?‌​=]*)?")

    @staticmethod
    def is_youtube(url):
        return Browsers.PATTERN.match(url)

    browsersChanged = Signal(list)

    def __init__(self):
        super(Browsers, self).__init__(None)

        self._browsers = []

        self.populate()

    @Slot(bool)
    def browserChanged(self, detected):
        self.browsersChanged.emit(self._browsers)

    @Slot()
    def populate(self) -> None:
        for browser in [Firefox()]:
            browser.detectedChanged.connect(self.browserChanged)
            self._browsers.append(browser)

        self.browsersChanged.emit(self.browsers)

    @Property("QVariantList", notify=browsersChanged)
    def browsers(self):
        return list(filter(lambda x: x._detected, self._browsers))

