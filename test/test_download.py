import sys
import os
import os.path
import unittest
import pickle

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from youtubedownloader import PreDownload, Download, DownloadProgress

class DownloadTest(unittest.TestCase):
    def setUp(self):
        self.yt_url = "https://www.youtube.com/watch?v=_mVW8tgGY_w"
        
        self.options = {
            "file_format": "mp3",
            "output_path": "/foo/bar/path"
        }
    
    def test_downloadInitializesByPreDownload(self):
        info = {
                "title": "test1",
                "uploader": "admin",
                "thumbnail": "None",
                "duration": 60
        }
        
        predownload = PreDownload(self.yt_url, self.options)
        predownload.collect_info(info)
        
        download = Download.fromPreDownload(predownload)
        self.assertEqual(download.url, predownload.url)
        self.assertEqual(download.download_options, predownload.download_options)
        self.assertEqual(download.title, predownload.title)
        self.assertEqual(download.uploader, predownload.uploader)
        self.assertEqual(download.thumbnail, predownload.thumbnail)
        
    def test_downloadPackAndUnpackData(self):
        data = {
                "id": 23123,
                "url": "https://foo.bar.test",
                "title": "test",
                "uploader": "test1",
                "thumbnail": "None",
                "duration": 60,
                "download_options": self.options
        }
        
        download = Download(data)
        packed = Download.pack(download)
        expected_keys = ["id", "url", "title", "uploader", "thumbnail", "duration", "download_options", "progress"]
        for key in packed.keys():
            self.assertTrue(key in expected_keys)
            
        unpacked = Download.unpack(packed)
        self.assertEqual(unpacked.id, download.id)    
        self.assertEqual(unpacked.url, download.url)    
        self.assertEqual(unpacked.title, download.title)    
        self.assertEqual(unpacked.uploader, download.uploader)    
        self.assertEqual(unpacked.thumbnail, download.thumbnail)    
        self.assertEqual(unpacked.duration, download.duration)    
        self.assertEqual(unpacked.download_options, download.download_options)    
            

if __name__ == "__main__":
    unittest.main()
