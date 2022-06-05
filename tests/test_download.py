import pytest

from PySide6.QtTest import (
    QSignalSpy
)

from youtubedownloader.download import (
    Pending,
    Downloading,
    Transaction,
    TaskResult,
    Data,
    Error,
    ProgressData,
    Transaction,
    Transactions,
    Options,
    
    FLAC,
    MP3,

    DownloadingLivestreamNotSupportedError,
)

from youtubedownloader.models import (
    PendingModel,
    RoleNames,
    Item
)

from youtubedownloader.task import (
    TaskFinished,
    TaskError
)


class PendingModelFixture(PendingModel):
    def __init__(self):
        super().__init__()

    def save(self):
        ...

    def load(self):
        ...


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

    @pytest.mark.parametrize(
        "test_data", [
            {
                "downloaded_bytes": 1000,
                "total_bytes": 5000,
                "speed": 250,
                "elapsed": 909090
            }
        ]
    ) 
    def test_progressdata_populates_dict_var(self, test_data):
        progress_data = ProgressData(**test_data)

        assert progress_data.downloaded_bytes == test_data["downloaded_bytes"]
        assert progress_data.total_bytes == test_data["total_bytes"]
        assert progress_data.speed == test_data["speed"]
        assert progress_data.elapsed == test_data["elapsed"]

    def test_pending_collects_data(self):
        pending = Pending("https://www.youtube.com/watch?v=2OEL4P1Rz04")

        pending.start()
        pending.wait()

        result = pending.result

        assert isinstance(result, TaskFinished)
        assert isinstance(result.value, Data)

    def test_pending_sets_error(self):
        pending = Pending("badurl")
        pending.start()
        pending.wait()

        result = pending.result

        assert isinstance(result, TaskError)
        assert isinstance(result.value, Error)
        assert isinstance(result.value.error, str)
        assert result.value.error != ""

    def test_pending_sets_error_if_trying_to_download_livestream(self):
        pending = Pending("https://www.youtube.com/watch?v=5qap5aO4i9A")
        pending.start()
        pending.wait()

        result = pending.result

        assert isinstance(result, TaskError)
        assert result.value.error == str(DownloadingLivestreamNotSupportedError())        

    def test_transaction_interacts_with_model(self):
        model = PendingModelFixture()
        pending = Pending("https://www.youtube.com/watch?v=OaXaGfNYEUk")
        item = Item(model.ROLE_NAMES, options=Options(output="home", format="mp3"))

        assert model.size() == 0

        transaction = Transaction(pending, model, item)

        transaction.start()
        transaction.wait()
         
        assert model.size() == 1

        item = model.items[0]
        
        assert isinstance(item, Item)
        assert item.status == "ready"
        assert isinstance(item.info, Data)
        assert item.info.url == "https://www.youtube.com/watch?v=OaXaGfNYEUk"
        assert item.info.title == "Deficio - Egyptica"
        assert item.options.output == "home"
        assert isinstance(item.options.format, MP3)


    @pytest.mark.parametrize(
        "output, format, expected_opts", [
            ("home", "mp4", {
                "outtmpl": "home/%(title)s.%(ext)s",
                "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4",
                "postprocessors": [],
                "progress_hooks": []
            }),
            ("documents", "flac", {
                "outtmpl": "documents/%(title)s.%(ext)s",
                "format" : "bestaudio/best",
                "postprocessors":[{
                    "key": 'FFmpegExtractAudio',
                    "preferredcodec": 'flac',
                 }],
                "progress_hooks": []
            })
        ]
    )
    def test_options_are_compatibile_with_yd_opts(self, output, format, expected_opts):
        options = Options(output, format)

        assert options.to_opts() == expected_opts

    
    def test_options_can_be_created_from_dict_kwargs(self):
        d = {
            "output": "home",
            "format": "flac"
        }

        options = Options(**d)

        assert options.output == "home"
        assert isinstance(options.format, FLAC)

    def test_options_eq_operator_works(self):
        options1 = Options(output="home", format="mp3")
        options2 = Options(output="home", format="mp3")
        options3 = Options(output="etc", format="mp4")

        assert options1 == options2
        assert options1 != options3
        assert options2 != options3

    def test_options_creates_valid_dict_format(self):
        d = {
            "output": "home",
            "format": "mp3"
        }

        options = Options(**d)

        options_d = options.to_dict()
        assert options_d["output"] == "home"
        assert options_d["format"] == "mp3"

    def test_transaction_eq_operator_works_correctly(self):
        roles = RoleNames("title")

        pending = Pending("url")
        model = PendingModelFixture()

        item1 = Item(roles)
        item2 = Item(roles)

        transaction1 = Transaction(pending, model, item1)
        transaction2 = Transaction(pending, model, item1)
        transaction3 = Transaction(pending, model, item2)

        assert transaction1 == transaction2
        assert transaction1 != transaction3


    def test_transactions_can_search_for_particural_item(self):
        roles = RoleNames("url")
        pending = Pending("url")
        model = PendingModelFixture()

        item1 = Item(roles)
        item2 = Item(roles)
        item3 = Item(roles)

        transaction1 = Transaction(pending, model, item1)
        transaction2 = Transaction(pending, model, item2)
        transaction3 = Transaction(pending, model, item1)

        transactions = Transactions()
        transactions.transactions = [transaction1, transaction2, transaction3]

        assert transactions.itemExists(item1)
        assert transactions.itemExists(item2)
        assert not transactions.itemExists(item3)






    
