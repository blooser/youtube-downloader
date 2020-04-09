import sys
import os
import os.path
import unittest
import pickle

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from youtubedownloader import Settings


class SettingsTest(unittest.TestCase):
    def setUp(self):
        self.config_path = "testsettings"

    def test_settingsStoresData(self):
        settings1 = Settings(self.config_path)
        settings1.type = "mp4"
        settings1.output_path = "/foo/bar/path1"
        del settings1
        
        settings2 = Settings(self.config_path)
        self.assertEqual(settings2.type, "mp4")
        self.assertEqual(settings2.output_path, "/foo/bar/path1")
