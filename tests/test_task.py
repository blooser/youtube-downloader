import pytest

from youtubedownloader.task import (
    Task,
    
    TaskResult,
    
    TaskFinished,
    TaskError,
    TaskStopped,
    TaskPaused,
    
    TaskPause,
    TaskStop
)


class TaskFixture(Task):
    def __init__(self, url):
        super().__init__(url)

    def run(self):
        try:
            while True:
                for event in self.events:
                    event()
        
        except TaskStop as err:
            self.set_result(TaskStopped())

        except TaskPause as err:
            self.set_result(TaskPaused())


def test_task_pause_event_system_works():
    task = TaskFixture("url")
    task.start()
    task.pause()

    task.wait()

    assert isinstance(task.result, TaskPaused)
    assert len(task.events) == 0

def test_task_stop_event_system_works():
    task = TaskFixture("url")
    task.start()
    task.stop()

    task.wait()

    assert isinstance(task.result, TaskStopped)
    assert len(task.events) == 0



