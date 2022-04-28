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
    @pytest.mark.parametrize(
        "test_data", [
            {
                "url": "test",
                "title": "nice",
                "categories": "multiple",
                "duration": 2500
            }
        ]
    )
    def test_data_populates_dict_var(self, test_data):
        data = Data(**test_data)

        assert data.url == test_data["url"]
        assert data.title == test_data["title"]
        assert data.categories == test_data["categories"]
        assert data.duration == test_data["duration"]

    @pytest.mark.parametrize(
        "test_data", [
            dict(first = {
                    "id": 1,
                    "url": "test",
                    "title": "nice",
                    "categories": "multiple",
                    "duration": 2500
                },
                second = {
                    "id": 2,
                    "url": "lol",
                    "title": "never",
                    "categories": "dunno",
                    "duration": 5500
                }
            )       
        ]
    )
    def test_data_eq_operator_works_correctly(self, test_data):
        assert test_data["first"] == test_data["first"]
        assert test_data["first"] != test_data["second"]


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


        

