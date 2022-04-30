import pytest

from PySide6.QtTest import (
    QSignalSpy
)

from youtubedownloader.download import (
    Pending,
    TaskResult,
    Data,
    Transaction,
    Options,
    
    FLAC,
    MP3
)

from youtubedownloader.models import (
    PendingModel,
    Item
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
        pending = Pending("https://www.youtube.com/watch?v=OaXaGfNYEUk")
        options = dict(output="home", format="mp3")

        assert model.size() == 0

        transaction = Transaction(pending, model, options)

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
                "output_path": "home/%(title)s.%(ext)s",
                "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4",
                "postprocessors": None
            }),
            ("documents", "flac", {
                "output_path": "documents/%(title)s.%(ext)s",
                "format" : "bestaudio/best",
                "postprocessors":[{
                    "key": 'FFmpegExtractAudio',
                    "preferredcodec": 'flac',
                 }]
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

    def test_options_creates_valid_dict_format(self):
        d = {
            "output": "home",
            "format": "mp3"
        }

        options = Options(**d)

        options_d = options.to_dict()
        assert options_d["output"] == "home"
        assert options_d["format"] == "mp3"
        assert options_d["progress_hooks"] == []

