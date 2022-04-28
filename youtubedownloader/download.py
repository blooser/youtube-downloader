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

from youtubedownloader.models import (
    PendingModel
)

from youtubedownloader.logger import (
    create_logger
)

import os.path
import pathlib
import pickle
import youtube_dl
import atexit
import urllib.request


logger = create_logger("youtubedownloader.download")


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

        logger.info(f"Data populated, number of variables: {len(self.__dict__)}")

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


class TaskResult(QObject):
    def __init__(self, value):
        super().__init__(None)

        self.value = value

    def is_valid(self):
        return isinstance(self.value, Data)

    def is_error(self):
        return isinstance(self.value, Exception)

    def __str__(self):
        if self.is_error():
            return "task failed"

        if self.is_valid():
            return "task successful"

        return "unknown"


class Task(QThread):
    resultReady = Signal(QObject)

    def __init__(self, url):
        super().__init__(None)

        self.url = url
        self.result = None

    def id(self):
        return QThread.currentThreadId()

    def set_result(self, value):
        self.result = TaskResult(value)
        self.resultReady.emit(self.result)

        logger.info(f"Result for {self.url} ready: {self.result}")

    def run(self):
        return NotImplemented

    def __eq__(self, other):
       return self.id() == other.id()


class Pending(Task):
    def __init__(self, url):
        super().__init__(url)

    def run(self):
        logger.info(f"Pending started for {self.url}")

        try:
            with youtube_dl.YoutubeDL() as ydl:
                self.set_result(Data.frominfo(ydl.extract_info(self.url, download=False)) + dict(url=self.url))

        except Exception as err:
            self.set_result(err)


class Transaction(QObject):
    def __init__(self, task, model):
        super().__init__(None)

        self.task = task
        self.model = model

        # NOTE: `DirectConnection` beacuse of multithreaded
        self.task.resultReady.connect(self.insertTaskResult, Qt.DirectConnection)

    @Slot(QObject)
    def insertTaskResult(self, task_result):
        self.model.insert(task_result.value)

        logger.info(f"Inserted new task result to the model")

    def start(self):
        self.task.start()

    def wait(self):
        self.task.wait()


class PendingManager(QObject):
    def __init__(self):
        super().__init__(None)

        self.model = PendingModel()

    @Property(str)
    def insert(self, url):
        task = Pending(url)

        transaction = Transaction(task, self.model)
        transaction.start()








