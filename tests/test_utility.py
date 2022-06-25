import pytest


from youtubedownloader.utility import Utility


class TestUtility:
    def test_utility_converts_ms_to_human(self):
        utility = Utility()

        utility.msToHuman("360") == "00:05:00"

    def test_utility_converts_date_to_human(self):
        utility = Utility()

#        TODO: Support multiple languages
#        assert utility.dateToHuman("20190212") == ""

    def test_utility_converts_big_number_to_human(self):
        utility = Utility()

        utility.bigNumberToHuman(100000) == "100,000"
