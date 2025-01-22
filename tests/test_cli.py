"""Integration tests for LUMA CLI functionality."""

import unittest
import os
import tempfile
from unittest.mock import patch
from luma_diagnostics.cli import main  # We'll create this next

class TestLumaCLI(unittest.TestCase):
    """Test suite for LUMA CLI functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.valid_image = os.path.join(self.temp_dir, "valid.jpg")
        self.invalid_image = os.path.join(self.temp_dir, "invalid.jpg")
        
        # Create a valid test image
        with open(self.valid_image, 'wb') as f:
            f.write(b'Valid JPEG\xff\xd8\xff\xe0')
        
        # Create an invalid test image
        with open(self.invalid_image, 'wb') as f:
            f.write(b'Invalid image data')
    
    def tearDown(self):
        """Clean up test fixtures."""
        os.remove(self.valid_image)
        os.remove(self.invalid_image)
        os.rmdir(self.temp_dir)
    
    @patch('sys.argv')
    def test_cli_no_args(self, mock_argv):
        """Test CLI with no arguments."""
        mock_argv.return_value = ['luma-diagnostics']
        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 2)
    
    @patch('sys.argv')
    def test_cli_help(self, mock_argv):
        """Test CLI help command."""
        mock_argv.return_value = ['luma-diagnostics', '--help']
        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 0)
    
    @patch('sys.argv')
    @patch('luma_diagnostics.api_tests.LumaAPITester')
    def test_cli_valid_image(self, mock_api, mock_argv):
        """Test CLI with valid image."""
        mock_argv.return_value = ['luma-diagnostics', '--image', self.valid_image]
        mock_api.return_value.test_image_reference.return_value = {
            "status": "success",
            "details": {"id": "test_id"}
        }
        
        with patch('builtins.print') as mock_print:
            main()
            mock_print.assert_called_with(unittest.mock.ANY)
    
    @patch('sys.argv')
    @patch('luma_diagnostics.api_tests.LumaAPITester')
    def test_cli_invalid_image(self, mock_api, mock_argv):
        """Test CLI with invalid image."""
        mock_argv.return_value = ['luma-diagnostics', '--image', self.invalid_image]
        mock_api.return_value.test_image_reference.return_value = {
            "status": "error",
            "details": {"error": "Invalid image format"}
        }
        
        with patch('builtins.print') as mock_print:
            main()
            mock_print.assert_called_with(unittest.mock.ANY)
    
    @patch('sys.argv')
    @patch('luma_diagnostics.api_tests.LumaAPITester')
    def test_cli_invalid_api_key(self, mock_api, mock_argv):
        """Test CLI with invalid API key."""
        mock_argv.return_value = ['luma-diagnostics', '--key', 'invalid_key']
        mock_api.return_value.test_text_to_image.return_value = {
            "status": "error",
            "details": {"error": "Invalid API key"}
        }
        
        with patch('builtins.print') as mock_print:
            main()
            mock_print.assert_called_with(unittest.mock.ANY)

if __name__ == '__main__':
    unittest.main()
