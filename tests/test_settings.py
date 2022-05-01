import pytest
import os
import os.path

from youtubedownloader.settings import (
    Settings
)


@pytest.fixture()
def path():
    path =  os.path.join(os.path.dirname(__file__), "test.ini")

    yield path

    #os.remove(path)


class TestSettigs:
    def test_settings_initializes_with_default_values(self, path):
        settings = Settings(path)

        assert settings._input == ""
        assert settings._format == "webm"
        assert settings._singleLine == True
        assert settings._themeColor == "#004d99"

        #os.remove(path)
