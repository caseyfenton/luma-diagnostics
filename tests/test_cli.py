"""Integration tests for LUMA CLI functionality."""

import unittest
import os
import tempfile
from unittest.mock import patch, MagicMock
from luma_diagnostics.cli import main
from PIL import Image
import numpy as np

class TestLumaCLI(unittest.TestCase):
    """Test suite for LUMA CLI functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.valid_image = os.path.join(self.temp_dir, "valid.jpg")
        self.invalid_image = os.path.join(self.temp_dir, "invalid.jpg")
        
        # Create a valid test image using PIL
        img = Image.fromarray(np.zeros((100, 100, 3), dtype=np.uint8))
        img.save(self.valid_image, format='JPEG')
        
        # Create an invalid test image
        with open(self.invalid_image, 'wb') as f:
            f.write(b'Invalid image data')
    
    def tearDown(self):
        """Clean up test fixtures."""
        os.remove(self.valid_image)
        os.remove(self.invalid_image)
        os.rmdir(self.temp_dir)
    
    def test_cli_no_args(self):
        """Test CLI with no arguments."""
        test_args = ['luma-diagnostics']
        with patch('sys.argv', test_args), \
             patch('builtins.print') as mock_print, \
             self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 2)
    
    def test_cli_help(self):
        """Test CLI help command."""
        test_args = ['luma-diagnostics', '--help']
        with patch('sys.argv', test_args), \
             patch('builtins.print') as mock_print, \
             self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 0)
    
    def test_cli_valid_image(self):
        """Test CLI with valid image."""
        test_args = ['luma-diagnostics', '--test', '--image', self.valid_image, '--api-key', 'luma_test_key_123456789012345678901234567890']
        with patch('sys.argv', test_args), \
             patch('luma_diagnostics.api_tests.LumaAPITester') as mock_api, \
             patch('builtins.print') as mock_print:
            
            # Configure mock
            mock_instance = mock_api.return_value
            mock_instance.test_text_to_image.return_value = {
                "status": "success",
                "details": {"id": "test_id"}
            }
            mock_instance.test_image_reference.return_value = {
                "status": "success",
                "details": {"id": "test_id"}
            }
            
            with self.assertRaises(SystemExit) as cm:
                main()
            self.assertEqual(cm.exception.code, 0)
    
    def test_cli_invalid_image(self):
        """Test CLI with invalid image."""
        test_args = ['luma-diagnostics', '--test', '--image', self.invalid_image, '--api-key', 'luma_test_key_123456789012345678901234567890']
        with patch('sys.argv', test_args), \
             patch('builtins.print') as mock_print, \
             self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 1)
    
    def test_cli_invalid_api_key(self):
        """Test CLI with invalid API key."""
        test_args = ['luma-diagnostics', '--test', '--api-key', 'invalid_key']
        with patch('sys.argv', test_args), \
             patch('builtins.print') as mock_print, \
             self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 1)

if __name__ == '__main__':
    unittest.main()
