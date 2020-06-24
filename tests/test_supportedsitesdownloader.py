import sys
import os.path
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from youtubedownloader import SupportedSitesDownloader

class DownloadModelTest(unittest.TestCase):
    
    def test_supportedSitesDownloaderDownloadsAndParsesSites(self):
        supported_sites_downloader = SupportedSitesDownloader()
        self.assertTrue(isinstance(supported_sites_downloader.sites), list)
        self.assertTrue(len(supported_sites_downloader.sites) != 0)


if __name__ == "__main__":
    unittest.main()

