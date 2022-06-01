from PySide6.QtCore import (
    Signal,
    Slot,

    Qt,
    QObject,
    QThread
)

from youtubedownloader.logger import create_logger

logger = create_logger(__name__)


class EmptyFunction:
    def __call__(self):
        pass

class TaskStop(Exception):
    """The task stopped"""

class TaskStopEvent:
    def __call__(self):
        raise TaskStop()

class TaskPause(Exception):
    """The task paused"""

class TaskPauseEvent:
    def __call__(self):
        raise TaskPause()

class TaskResult:
    def __init__(self, value, status):
        self.value = value
        self.status = status

    def to_dict(self):
        return {
            "info": self.value,
            "status": self.status
        }


class TaskWaiting(TaskResult):
    def __init__(self, value={}):
        super().__init__(value, "waiting")

    def __str__(self):
        return "Task waiting"

class TaskFinished(TaskResult):
    def __init__(self, value={}):
        super().__init__(value, "ready")

    def __str__(self):
        return "Task finished"


class TaskError(TaskResult):
    def __init__(self, value):
        super().__init__(value, "error")

        from youtubedownloader.download import Error

        self.value = Error(**value)

    def __str__(self):
        return "Task error"


class TaskStopped(TaskResult):
    def __init__(self):
        super().__init__({}, "stopped")

    def __str__(self):
        return "Task stopped"


class TaskPaused(TaskResult):
    def __init__(self):
        super().__init__({}, "paused")

    def __str__(self):
        return "Task paused"


class Task(QThread):
    resultReady = Signal(QObject)

    def __init__(self, url):
        super().__init__(None)

        self.url = url
        self.result = TaskWaiting()

        self.events = []

        self.finished.connect(self.clear_events, Qt.DirectConnection)

    def __eq__(self, other):
       return self.id() == other.id()

    def runningOnly(f):
        def runningOnlyWrapper(self, *args, **kwargs):
            if not self.isRunning():
                return EmptyFunction()

            return f(self, *args, **kwargs)

        return runningOnlyWrapper

    def id(self):
        return QThread.currentThreadId()

    def set_result(self, result):
        self.result = result

        logger.info(f"Result for {self.url}: {self.result}")

    def run(self):
        return NotImplemented

    @Slot()
    def clear_events(self):
        logger.info("Clearing")

        self.events.clear()

    @runningOnly
    def stop(self):
        self.events.append(TaskStopEvent())

    @runningOnly
    def pause(self):
        self.events.append(TaskPauseEvent())

