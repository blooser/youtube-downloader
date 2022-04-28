import pytest

from PySide6.QtTest import (
    QSignalSpy
)

from youtubedownloader.download import (
    Pending,
    PendingManager,
    TaskResult,
    Data,
    Transaction
)

from youtubedownloader.models import (
    PendingModel
)


class TestPending:
    def test_data_populates_dict_var(self):
        data = Data(url="test", value=25, key=100, test=None)

        assert data.url == "test"
        assert data.value == 25
        assert data.key == 100
        assert data.test == None

    def test_pending_collects_data(self):
        pending = Pending("https://www.youtube.com/watch?v=2OEL4P1Rz04")

        pending.start()
        pending.wait()

        result = pending.result

        assert result.is_error() == False
        assert result.is_valid() == True
        assert isinstance(result.value, Data)

    def test_pending_sets_error(self):
        pending = Pending("badurl")
        pending.start()
        pending.wait()

        result = pending.result

        assert result.is_error() == True
        assert result.is_valid() == False
        assert isinstance(result.value, Exception)
    
    def test_transaction_interacts_with_model(self):
        model = PendingModel()
        pending = Pending("https://www.youtube.com/watch?v=2OEL4P1Rz04")

        assert model.size() == 0

        transaction = Transaction(pending, model)

        transaction.start()
        transaction.wait()

        assert model.size() == 1


        

