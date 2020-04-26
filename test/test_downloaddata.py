import sys
import os
import os.path
import unittest
import pickle

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from youtubedownloader import DownloadData


class DownloadTest(unittest.TestCase):

    def setUp(self):        
        self.data = {
                "title": "test",
                "uploader": "test1",
                "uploader_url": "/foo/bar/uploader",
                "thumbnail": "None",
                "duration": 60,
        }
            
    def test_downloadPackAndUnpackData(self):   
        download_data = DownloadData(self.data)
        
        packed = DownloadData.pack(download_data)
        self.assertTrue(isinstance(packed, dict))
        expected_keys = ["title", "uploader", "uploader_url",  "thumbnail", "duration"]
        for key in packed.keys():
            self.assertTrue(key in expected_keys)
            
        unpacked = DownloadData.unpack(packed)
        self.assertEqual(unpacked._title, download_data._title)
        self.assertEqual(unpacked._uploader, download_data._uploader)
        self.assertEqual(unpacked._uploader_url, download_data._uploader_url)
        self.assertEqual(unpacked._thumbnail, download_data._thumbnail)
        self.assertEqual(unpacked._duration, download_data._duration)
            

if __name__ == "__main__":
    unittest.main()
