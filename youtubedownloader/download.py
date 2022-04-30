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
    DownloadModel,
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



class DownloadingStop(Exception):
    """The downloading process was stopped"""

class DownloadingStopEvent:
    def __call__(self):
        raise DownloadingStop


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

    def keys(self):
        return self.KEYS

    def __len__(self):
        return len(self.__dict__.keys())

    def __getitem__(self, item):
        return self.__dict__[item]

    def __add__(self, other):
        for name in other:
            self.__dict__[name] = other[name]

        return self

    def __eq__(self, other):
        return self.id == other.id

    def __repr__(self):
        return f"<Data {len(self)} attributes>"

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
    progress = Signal(Data)

    def __init__(self, url):
        super().__init__(None)

        self.url = url
        self.result = None

        self.events = []

    def id(self):
        return QThread.currentThreadId()

    def set_result(self, value):
        self.result = TaskResult(value)
        self.resultReady.emit(self.result)

        logger.info(f"Result for {self.url} ready: {self.result}")

    def run(self):
        return NotImplemented

    def stop(self):
        self.events.append(DownloadingStopEvent())

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
    def __init__(self, task, model, item):
        super().__init__(None)

        self.task = task
        self.model = model
        self.item = item

        # NOTE: DirectConnection needed because of QThread has its own event loop
        self.task.resultReady.connect(self.taskResultReady, Qt.DirectConnection)
        self.task.progress.connect(self.progress, Qt.DirectConnection)
        self.model.itemRemoved.connect(self.stopIfItemRemoved)

    @Slot(TaskResult)
    def taskResultReady(self, task_result):
        if task_result.is_error():
            # TODO: Implement error info logic
            self.item.update(dict(info={}, status="error"))
            return

        value = task_result.value
        self.item.update(dict(info=value, status="ready"))

    @Slot(Data)
    def progress(self, progress):
        self.item.update(dict(progress=progress, status="downloading"))

    @Slot(Item)
    def stopIfItemRemoved(self, item):
        if self.item == item and self.task.isRunning():
            self.stop()

    def start(self):
        self.model.insert(self.item)

        self.task.start()

        logger.info(f"Transaction for {self.item} started")

    def stop(self):
        self.task.stop()

        logger.info(f"Transaction for {self.item} stopped")

    def wait(self):
        self.task.wait()


class ProgressData(Data):
    KEYS = [
        "downloaded_bytes",
        "total_bytes",
        "filename",
        "speed",
        "eta",
        "elapsed",

        "_eta_str",
        "_percent_str",
        "_speed_str",
        "_total_bytes_str"
    ]


class Downloading(Task):
    def __init__(self, url, options):
        super().__init__(url)

        self.options = options

        self.options.progress_hooks = [self.progress_track]

    def progress_track(self, data):
        for event in self.events:
            event()

        self.data = ProgressData(**data)

        self.progress.emit(self.data)

    def run(self):
        logger.info(f"Downloading started for {self.url} with options={self.options}")

        try:
            with youtube_dl.YoutubeDL(self.options.to_opts()) as ydl:
                ydl.download([self.url])

        except DownloadingStop as err:
            logger.info(err)

        except youtube_dl.utils.DownloadError as err:
            self.set_result(err)



class Transactions:
    def __init__(self):
        self.transactions = []

    def start(self, task, model, item):
        transaction = Transaction(task, model, item)
        transaction.start()

        self.transactions.append(transaction)

    def remove(self):
        pass


class DownloadManager(QObject):
    def __init__(self):
        super().__init__(None)

        self.pending_model = PendingModel()
        self.download_model = DownloadModel()

        self.transactions = []

    @Slot(str, "QVariantMap")
    def insert(self, url, options):
        task = Pending(url)

        item = self.pending_model.item(options=Options(**options))
        transaction = Transaction(task, self.pending_model, item)
        transaction.start()

        self.transactions.append(transaction)

    @Slot()
    def download(self):
        # NOTE: Steal pending's items
        items = self.pending_model.items
        self.pending_model.reset()

        for item in items:
            # TODO: Implement special Roles object for that kind of operation :)
            task = Downloading(item[self.pending_model.ROLE_NAMES.info].url,
                               item[self.pending_model.ROLE_NAMES.options])

            transaction = Transaction(task, self.download_model, item)
            transaction.start()

            self.transactions.append(transaction)

    @Property(QObject, constant=True)
    def pendingModel(self):
        return self.pending_model

    @Property(QObject, constant=True)
    def downloadModel(self):
        return self.download_model


class Options(QObject):
    def __init__(self, output = "", format = "mp4", progress_hooks = []):
        super().__init__(None)

        self.format = Format.fromstr(format)
        self.output = output
        self.progress_hooks = progress_hooks

    def to_opts(self):
        return {
            "output_path": f"{self.output}/%(title)s.%(ext)s",
            "progress_hooks": self.progress_hooks,
            **self.format.to_opts()
        }

    def to_dict(self):
        return {
            "output": self.output,
            "format": self.format.name,
            "progress_hooks": self.progress_hooks
        }

    def __repr__(self):
        return f"<Options format={self.format} output={self.output}>"


class Format:
    name = None
    format = None
    postprocessors = []

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

    def __repr__(self):
        return f"<{self.name.upper()}>"


class MP4(Format):
    name = "mp4"
    format = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4"


class WEBM(Format):
    name = "webm"
    format = "bestvideo[ext=webm]+bestaudio[ext=webm]/webm"


class MKV(Format):
    name = "webm"
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

