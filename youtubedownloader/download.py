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
    PendingModel,
    Item
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
        "uploader_url",
        "thumbnail",
        "duration",
        "upload_date",
        "view_count",
        "like_count"
    ]

    def __init__(self, **kwargs):
        for name in kwargs:
            self.__dict__[name] = kwargs[name]

        logger.info(f"Data populated, number of items: {len(self.__dict__)}")

    def keys(self):
        return self.KEYS

    def __getitem__(self, item):
        return self.__dict__[item]

    def __add__(self, other):
        for name in other:
            self.__dict__[name] = other[name]

        return self

    def __eq__(self, other):
        return self.id == other.id

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

        self.item = self.model.item()

        # NOTE: DirectConnection needed because of QThread has its own event loop
        self.task.resultReady.connect(self.taskResultReady, Qt.DirectConnection)

    @Slot(TaskResult)
    def taskResultReady(self, task_result):
        if task_result.is_error():
            # TODO: Implement error info logic
            self.item.update(dict(info={}, status="error"))
            return

        value = task_result.value
        self.item.update(dict(info=value, status="ready"))

    def start(self):
        self.model.insert(self.item)

        self.task.start()

    def wait(self):
        self.task.wait()


class PendingManager(QObject):
    def __init__(self):
        super().__init__(None)

        self.pending_model = PendingModel()
        self.transactions = []

    @Slot(str)
    def insert(self, url):
        task = Pending(url)

        transaction = Transaction(task, self.pending_model)
        transaction.start()

        self.transactions.append(transaction)

    @Property(QObject, constant=True)
    def model(self):
        return self.pending_model



class Options(QObject):
    def __init__(self, output="", format="mp4"):
        super().__init__(None)

        self.format = Format.fromstr(format)
        self.output = output

    def to_opts(self):
        return dict(output_path = f"{self.output}/%(title)s.%(ext)s", **self.format.to_opts())

class Format:
    name = None
    format = None
    postprocessors = None

    def to_opts(self):
        return {
            "format": self.format,
            "postprocessors": self.postprocessors
        }


    @staticmethod
    def fromstr(name):
        return {
            "mp4":  MP4,
            "webm": WEBM,
            "mkv":  MKV,
            "m4a":  M4A,
            "flac": FLAC,
            "mp3":  MP3,
            "wav":  WAV,
        }[name]()


class MP4(Format):
    name = "mp4",
    format = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4"


class WEBM(Format):
    name = "webm",
    format = "bestvideo[ext=webm]+bestaudio[ext=webm]/webm"


class MKV(Format):
    name = "webm",
    format = "bestvideo[ext=webm]+bestaudio[ext=m4a]/mkv"


class M4A(Format):
    name = "m4a"
    format = "bestaudio[ext=m4a]/m4a"


class FLAC(Format):
    name = "flac"
    format = "bestaudio/best"
    postprocessors = [{
        "key": 'FFmpegExtractAudio',
        "preferredcodec": 'flac',
     }]


class MP3(Format):
    name = "mp3"
    format = "bestaudio/best"
    postprocessors = [{
        "key": 'FFmpegExtractAudio',
        "preferredcodec": 'mp3',
        "preferredquality": "320",
     }]


class WAV(Format):
    name = "wav"
    format = "bestaudio/best"
    postprocessors = [{
        "key": 'FFmpegExtractAudio',
        "preferredcodec": 'wav',
    }]
