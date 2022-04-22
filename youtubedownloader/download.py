from PySide6.QtCore import (
    QObject,
    QAbstractListModel,
    QFileInfo,
    QFile,
    QIODevice,
    QFileSystemWatcher,
    QModelIndex,
    QDateTime,
    QDate,
    QTime,
    QThread,
    QTimer,
    Qt,
    QSettings,
    QStandardPaths,
    Slot,
    Signal,
    Property

)
from PySide6.QtQml import (
    QQmlApplicationEngine,
    QQmlContext
)
from PySide6.QtNetwork import (
    QNetworkAccessManager,
    QNetworkReply,
    QNetworkRequest
)

import os.path
import pathlib
import pickle
import youtube_dl
import atexit
import urllib.request



class Data():
    KEYS = [
        "id",
        "url",
        "title",
        "categories",
        "uploader",
        "thumbnail",
        "duration",
        "upload_date",
        "view_coint",
    ]

    def __init__(self, **kwargs):
        for name in kwargs:
            self.__dict__[name] = kwargs[name]

    def keys(self):
        return self.KEYS

    def __getitem__(self, item):
        return self.__dict__[item]

    def __add__(self, other):
        for name in other:
            self.__dict__[name] = other[name]

        return self

    @classmethod
    def frominfo(cls, info):
        return cls(**info)


class Task(QThread):
    def __init__(self, url):
        super().__init__(None)

        self.url = url

    def run(self):
        return NotImplemented


class Pending(Task):
    def __init__(self, url):
        super().__init__(url)

    def run(self):
        try:
            with youtube_dl.YoutubeDL() as ydl:
                self.data = Data.frominfo(ydl.extract_info(self.url, download=False)) + dict(url=self.url)


        except Exception as err:
            print(err)












