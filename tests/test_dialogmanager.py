import sys
import os.path
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from youtubedownloader.paths import Paths
from youtubedownloader.dialog_manager import DialogManager


class DialogManagerTest(unittest.TestCase):
    
    def test_dialogManagerCollectsDialogs(self):
        dialog_manager = DialogManager()
        
        self.assertEqual(len(dialog_manager.dialogs), 9)
        
        expected_dialogs = ["ConfirmDeleteDialog", "SelectDirectoryDialog", "YDDialog", 
                            "DropUrlDialog", "ThumbnailDialog", "FileFormatsDialog", 
                            "SupportedSitesDialog", "HistoryDialog", "ThemeColorsDialog"]
        for key in dialog_manager.dialogs.keys():
            self.assertTrue(key in expected_dialogs)
            
            dialog = dialog_manager.dialogs[key]
            self.assertTrue(dialog.startswith("file:"))

if __name__ == "__main__":
    unittest.main()
