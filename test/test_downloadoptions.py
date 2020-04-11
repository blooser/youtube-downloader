import sys
import os
import os.path
import unittest
import pickle

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from youtubedownloader import DownloadOptions

class DownloadOptionsTest(unittest.TestCase):
    
    def test_downloadOptionsCreatesValidOuttmpl(self):
        options = {
                "file_format": "mp3",
                "output_path": "/foo/bar/path/output"
        }
        
        download_options = DownloadOptions(options)
        
        ydl_opts = download_options.to_ydl_opts()
        self.assertTrue("outtmpl" in ydl_opts)
        
        outtmpl = ydl_opts["outtmpl"]
        expected_outtmpl = options["output_path"] + "/%(title)s.%(ext)s"
        self.assertEqual(outtmpl, expected_outtmpl)
        
if __name__ == "__main__":
    unittest.main()
