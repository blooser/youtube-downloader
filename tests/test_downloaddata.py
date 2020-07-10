import sys
import os
import os.path
import unittest
import pickle

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from youtubedownloader.download import DownloadData


class DownloadTest(unittest.TestCase):

    def setUp(self):        
        self.data = {
                "title": "test",
                "uploader": "test1",
                "uploader_url": "/foo/bar/uploader",
                "thumbnail": "None",
                "duration": 60,
                "upload_date": "2017",
                "view_count": 80
        }
            
    def test_downloadPackAndUnpackData(self):   
        download_data = DownloadData(self.data)
        
        packed = DownloadData.pack(download_data)
        self.assertTrue(isinstance(packed, dict))
        expected_keys = ["title", "uploader", "uploader_url",  "thumbnail", "duration", "upload_date", "view_count"]
        for key in packed.keys():
            self.assertTrue(key in expected_keys)
            
        unpacked = DownloadData.unpack(packed)
        self.assertEqual(unpacked._title, download_data._title)
        self.assertEqual(unpacked._uploader, download_data._uploader)
        self.assertEqual(unpacked._uploader_url, download_data._uploader_url)
        self.assertEqual(unpacked._thumbnail, download_data._thumbnail)
        self.assertEqual(unpacked._duration, download_data._duration)
        self.assertEqual(unpacked._upload_date, download_data._upload_date)
        self.assertEqual(unpacked._view_count, download_data._view_count)

            

if __name__ == "__main__":
    unittest.main()
