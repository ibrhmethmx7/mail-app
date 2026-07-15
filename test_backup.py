import unittest
from unittest.mock import MagicMock, patch
import os
import shutil
import backup_manager
import config

class TestBackupManager(unittest.TestCase):
    def setUp(self):
        # Setup temporary backup directory
        self.test_backup_dir = "test_backups"
        config.BACKUP_DIR = self.test_backup_dir
        if os.path.exists(self.test_backup_dir):
            shutil.rmtree(self.test_backup_dir)

    def tearDown(self):
        # Clean up
        if os.path.exists(self.test_backup_dir):
            shutil.rmtree(self.test_backup_dir)

    @patch('backup_manager.imaplib.IMAP4_SSL')
    def test_backup_logic(self, mock_imap):
        # Mock IMAP connection and login
        mock_mail = MagicMock()
        mock_imap.return_value = mock_mail
        
        # Mock search response
        mock_mail.search.return_value = ('OK', [b'1 2'])
        
        # Mock fetch response for email 1
        email1_content = b'Subject: Test Email 1\r\nDate: Wed, 04 Dec 2024 12:00:00 +0000\r\n\r\nBody 1'
        # Mock fetch response for email 2
        email2_content = b'Subject: Test Email 2\r\nDate: Thu, 05 Dec 2024 12:00:00 +0000\r\n\r\nBody 2'

        # Configure fetch side effects
        def fetch_side_effect(mail_id, part):
            if mail_id == b'1':
                return ('OK', [(b'1 (RFC822 {100})', email1_content)])
            elif mail_id == b'2':
                return ('OK', [(b'2 (RFC822 {100})', email2_content)])
            return ('NO', [])

        mock_mail.fetch.side_effect = fetch_side_effect

        # Run backup
        backup_manager.backup_emails()

        # Verify files exist
        # Email 1: 2024/12
        expected_path1 = os.path.join(self.test_backup_dir, "2024", "12", "Test Email 1_1.eml")
        self.assertTrue(os.path.exists(expected_path1), "Email 1 should be saved")

        # Email 2: 2024/12
        expected_path2 = os.path.join(self.test_backup_dir, "2024", "12", "Test Email 2_2.eml")
        self.assertTrue(os.path.exists(expected_path2), "Email 2 should be saved")

if __name__ == '__main__':
    unittest.main()
