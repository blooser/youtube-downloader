import sys
import os.path
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from youtubedownloader import Paths, DialogManager


class DialogManagerTest(unittest.TestCase):
    
    def test_dialogManagerCollectsDialogs(self):
        dialog_manager = DialogManager()
        
        self.assertEqual(len(dialog_manager.dialogs), 3)
        
        expected_dialogs = ["ConfirmDeleteDialog", "SelectDirectoryDialog", "YDDialog"]
        for key in dialog_manager.dialogs.keys():
            self.assertTrue(key in expected_dialogs)
            
            dialog = dialog_manager.dialogs[key]
            self.assertTrue(dialog.startswith("file:"))
