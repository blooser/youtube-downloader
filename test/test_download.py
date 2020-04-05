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
            "type": "mp3",
            "output_path": "/foo/bar/path"
        }
    
    def test_downloadSerialization(self):
        download_data = {
            "status": "Finished",
            "downloaded_bytes": 500,
            "total_bytes": 1000,
            "_eta_str": "00:25",
            "_speed_str": "25 MiB/s",
            "filename": "test"
        }

        tmp_filename = "download_test_pickle"
        predownload = PreDownload(self.yt_url,  self.options)
        download = Download(predownload)
        download.progress.update(download_data)

        with open(tmp_filename, "wb") as f:
            pickle.dump(download, f)

        self.assertTrue(os.path.isfile(tmp_filename))

        with open(tmp_filename, "rb") as f:
            unpickled_download = pickle.load(f)
        
        self.assertEqual(download.id, unpickled_download.id)
        self.assertEqual(download.url, unpickled_download.url)
        self.assertEqual(download.progress.status, unpickled_download.progress.status)
        self.assertEqual(download.progress.downloaded_bytes, unpickled_download.progress.downloaded_bytes)
        self.assertEqual(download.progress.total_bytes, unpickled_download.progress.total_bytes)
        self.assertEqual(download.progress.estimated_time, unpickled_download.progress.estimated_time)
        self.assertEqual(download.progress.speed, unpickled_download.progress.speed)
        self.assertEqual(download.progress.filename, unpickled_download.progress.filename)
       
        os.remove(tmp_filename) 
        self.assertFalse(os.path.isfile(tmp_filename))


if __name__ == "__main__":
    unittest.main()
