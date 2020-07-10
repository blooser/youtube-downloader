import sys
import os
import os.path
import unittest
import pickle

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from youtubedownloader.download import DownloadOptions


class DownloadOptionsTest(unittest.TestCase):
    
    def setUp(self):
        self.options = {
                "file_format": "mp3",
                "output_path": "/foo/bar/path/output"
        }
    
    
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
        
        
    def test_downloadOptionsPackAndUnpack(self):
            download_options = DownloadOptions(self.options)
            download_options.post_process_file_size = 650
            
            packed = DownloadOptions.pack(download_options)
            expected_keys = ["file_format", "output_path", "post_process_file_size"]
            for key in packed.keys():
                self.assertTrue(key in expected_keys)
                
            unpacked = DownloadOptions.unpack(packed)
            self.assertEqual(unpacked.file_format, download_options.file_format)
            self.assertEqual(unpacked.output_path, download_options.output_path)
            self.assertEqual(unpacked.post_process_file_size, download_options.post_process_file_size)

        
if __name__ == "__main__":
    unittest.main()
