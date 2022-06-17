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
    HistoryModel,
    Item
)

from youtubedownloader.database import (
    Database
)

from youtubedownloader.logger import (
    create_logger
)

from youtubedownloader.settings import (
    Paths
)

from youtubedownloader.task import (
    Task,

    TaskFinished,
    TaskError,
    TaskPause,
    TaskPaused,
    TaskStop,
    TaskStopped,
    TaskResult
)

import os.path
import pathlib
import pickle
import youtube_dl
import atexit
import urllib.request


logger = create_logger("youtubedownloader.download")



class Mappable:
    KEYS = []

    def __init__(self, **kwargs):
        for kwarg in kwargs:
            self.__dict__[kwarg] = kwargs[kwarg]

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


class Data(Mappable):
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
        "like_count",
        "is_live"
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __eq__(self, other):
        return self.id == other.id

    def __repr__(self):
        return f"<Data attributes={len(self)}>"

    @classmethod
    def frominfo(cls, info):
        return cls(**info)


class Error(Mappable):
    KEYS = [
        "error",
        "url"
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class DownloadingLivestreamNotSupportedError(Exception):
    """Downloading a livestream is not supported"""

    def __init__(self):
        super().__init__(self.__doc__)


class Pending(Task):
    progress = Signal(Data)
    convert = Signal()

    def __init__(self, url):
        super().__init__(url)

    def run(self):
        logger.info(f"Pending started for {self.url}")

        try:
            with youtube_dl.YoutubeDL() as ydl:
                data = Data.frominfo(ydl.extract_info(self.url, download=False)) + dict(url=self.url)

                if data.is_live:
                    raise DownloadingLivestreamNotSupportedError()

                self.set_result(TaskFinished(data))

        except Exception as err:
            self.set_result(TaskError(dict(url=self.url, error=str(err))))


class Transaction(QObject):
    finished = Signal(QObject)

    def __init__(self, task, model, item):
        super().__init__(None)

        self.task = task
        self.model = model
        self.item = item

        # NOTE: DirectConnection needed because of QThread has its own event loop
        self.task.progress.connect(self.progress, Qt.DirectConnection)
        self.task.convert.connect(self.convert, Qt.DirectConnection)
        self.task.finished.connect(self.transactionFinished, Qt.DirectConnection)

        self.model.itemRemoved.connect(self.stopIfItemRemoved)
        self.model.itemPaused.connect(self.pauseIfItem)
        self.model.itemResumed.connect(self.resumeIfItem)

    def __eq__(self, other):
        return self.item == other.item

    def __repr__(self):
        return f"<Transaction {self.item} {self.model}>"

    @Slot(TaskResult)
    def taskResultReady(self, task_result):
        self.item.update(task_result.to_dict())

    @Slot(Data)
    def progress(self, progress):
        self.item.update(dict(progress=progress, status="downloading"))

    @Slot()
    def convert(self):
        self.item.update(dict(status="converting"))

    @Slot(Item)
    def stopIfItemRemoved(self, item):
        if self.item == item and self.task.isRunning():
            self.stop()

    @Slot(Item)
    def pauseIfItem(self, item):
        if self.item == item and self.task.isRunning():
            self.pause()

    @Slot(Item)
    def resumeIfItem(self, item):
        if self.item == item and not self.task.isRunning():
            self.resume()

    @Slot()
    def transactionFinished(self):
        self.item.update(self.task.result.to_dict())

        self.finished.emit(self)

    def start(self):
        if not self.model.exists(self.item):
            self.model.insert(self.item)

        self.task.start()

        self.item.update(dict(status="waiting"))

        logger.info(f"Transaction for {self.item} started")

    def stop(self):
        if self.task.isRunning():
            self.task.stop()

    def pause(self):
        if self.task.isRunning():
            self.task.pause()

    def resume(self):
        if not self.task.isRunning():
            self.task.start()

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
        "status",

        "_eta_str",
        "_percent_str",
        "_speed_str",
        "_total_bytes_str"
    ]


class Downloading(Task):
    progress = Signal(Data)
    convert = Signal()

    def __init__(self, url, options):
        super().__init__(url)

        self.options = options

        self.options.progress_hooks = [self.progress_track]

    def progress_track(self, data):
        for event in self.events:
            event()

        self.data = ProgressData(**data)

        self.progress.emit(self.data)

        if self.data.status == "finished" and self.options.format.need_convert():
            self.convert.emit()

    def run(self):
        logger.info(f"Downloading started for {self.url} with options={self.options}")

        try:
            with youtube_dl.YoutubeDL(self.options.to_opts()) as ydl:
                ydl.download([self.url])

            self.set_result(TaskFinished())

        except TaskStop as err:
            self.set_result(TaskStopped())

        except TaskPause as err:
            self.set_result(TaskPaused())

        except youtube_dl.utils.DownloadError as err:
            self.set_result(TaskError(dict(url=self.url, error=str(err))))

    def stop(self):
        # TODO: Implement better stop/pause when deleting item from model
        self.pause()


class Transactions(QObject):
    def __init__(self):
        super().__init__(None)

        self.transactions = []

        atexit.register(self.clear)

    def start(self, task, model, item):
        transaction = Transaction(task, model, item)
        transaction.finished.connect(self.handleTransactionFinished)

        transaction.start()

        self.transactions.append(transaction)

    def itemExists(self, item):
        class transaction_comparer:
            def __init__(self, item):
                self.item = item

        return transaction_comparer(item) in self.transactions

    @Slot(QObject)
    def handleTransactionFinished(self, transaction):
        if transaction.task.result.status == "finished":
            self.remove(transaction)
            return

    def remove(self, transaction):
        try:
            del self.transactions[self.transactions.index(transaction)]
        except ValueError:
            logger.warning(f"Failed to find {transaction}")

            return

        logger.info(f"Removed {transaction}")

    def clear(self):
        logger.info(f"Clearing {len(self.transactions)} transactions")

        for transaction in self.transactions:
            transaction.stop()

        for transaction in self.transactions:
            transaction.wait()


class DownloadManager(QObject):
    itemAboutToBeDownload = Signal(Item)

    def __init__(self):
        super().__init__(None)

        self.pending_model = PendingModel()
        self.download_model = DownloadModel()

        self.transactions = Transactions()

        self.download_model.itemResumed.connect(self.listenForResumeDownload)

    @Slot(str, "QVariantMap")
    def insert(self, url, options):
        task = Pending(url)

        item = self.pending_model.item(options=Options(**options))

        self.transactions.start(task, self.pending_model, item)

    @Slot()
    def download(self):
        # NOTE: Steal pending's items
        items = self.pending_model.items
        self.pending_model.reset()

        for item in items:
            if item.status == "error":
                logger.warning(f"Skipping {item} due to error")

                continue

            self.itemAboutToBeDownload.emit(item)

            # TODO: Implement special Roles object for that kind of operation :)
            task = Downloading(item[self.pending_model.ROLE_NAMES.info].url,
                               item[self.pending_model.ROLE_NAMES.options])

            self.transactions.start(task, self.download_model, item)

    @Slot(Item)
    def listenForResumeDownload(self, item):
        if not self.transactions.itemExists(item):
            task = Downloading(item[self.pending_model.ROLE_NAMES.info].url,
                               item[self.pending_model.ROLE_NAMES.options])

            self.transactions.start(task, self.download_model, item)

            logger.info(f"Item {item} was resumed")

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
            "outtmpl": f"{self.output}/%(title)s.%(ext)s",
            "progress_hooks": self.progress_hooks,
            **self.format.to_opts()
        }

    def to_dict(self):
        return {
            "output": self.output,
            "format": self.format.name,
        }

    def __repr__(self):
        return f"<Options format={self.format} output={self.output}>"

    def __eq__(self, other):
        return self.format == other.format and self.output == other.output


class Format:
    name = None
    format = None
    postprocessors = []

    def to_opts(self):
        return {
            "format": self.format,
            "postprocessors": self.postprocessors
        }

    def need_convert(self):
        return self.postprocessors != []

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

    def __eq__(self, other):
        return self.name == other.name


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



class Signals(QObject):
    insert = Signal(str)
    remove = Signal(str)

    def __init__(self):
        super().__init__()

    @Slot(str)
    def emitInsert(self, url):
        self.insert.emit(url)

    @Slot(str)
    def emitRemove(self, url):
        self.remove.emit(url)
