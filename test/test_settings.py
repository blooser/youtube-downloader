import sys
import os
import os.path
import unittest
import pickle

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide2.QtCore import QRect
from youtubedownloader import Settings


class SettingsTest(unittest.TestCase):

    def setUp(self):
        self.config_path = "testsettings"
            
    def tearDown(self):
        if os.path.isfile(self.config_path):
            os.remove(self.config_path)

    def test_settingsStoresData(self):
        settings1 = Settings(self.config_path)
        settings1.input_link = "link"
        settings1.file_format = "mp4"
        settings1.output_path = "/foo/bar/path1"
        settings1.window_rect = QRect(100, 100, 750, 750)
        del settings1
        
        settings2 = Settings(self.config_path)
        self.assertEqual(settings2.input_link, "link")
        self.assertEqual(settings2.file_format, "mp4")
        self.assertEqual(settings2.output_path, "/foo/bar/path1")
        self.assertEqual(settings2.window_rect, QRect(100, 100, 750, 750))
