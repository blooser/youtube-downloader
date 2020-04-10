import sys
import os.path
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from youtubedownloader import DownloadProgress

class DownloadDataTest(unittest.TestCase):
    def setUp(self):
        self.data = {
           "status": "Finished",
           "downloaded_bytes": 4523,
           "total_bytes": 10000,
           "_eta_str": "00:43",
           "_speed_str": "4mb/s",
           "filename": "test"
        }

    def test_downloadDataParsesDict(self):
        download_data = DownloadProgress()
        download_data.update(self.data)

        self.assertEqual(download_data.status, self.data["status"])
        self.assertEqual(download_data.downloaded_bytes, self.data["downloaded_bytes"])
        self.assertEqual(download_data.total_bytes, self.data["total_bytes"])
        self.assertEqual(download_data.estimated_time, self.data["_eta_str"])
        self.assertEqual(download_data.speed, self.data["_speed_str"])
        self.assertEqual(download_data.filename, self.data["filename"])

    def test_downloadDataPutsDefaultValuesIfDictDoesntContainsKeys(self):
        download_data = DownloadProgress()
        download_data.update(dict())

        self.assertEqual(download_data.status, "Starting")
        self.assertEqual(download_data.downloaded_bytes, "0")
        self.assertEqual(download_data.total_bytes, "0")
        self.assertEqual(download_data.estimated_time, "00:00")
        self.assertEqual(download_data.speed, "0 MiB/s")
        self.assertEqual(download_data.filename, "Unknown")


if __name__ == "__main__":
    unittest.main()
