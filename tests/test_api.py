"""Unit tests for LUMA API handling."""

import unittest
from unittest.mock import patch, MagicMock
import requests
import json
from luma_diagnostics.api_tests import LumaAPITester

class TestLumaAPI(unittest.TestCase):
    """Test suite for LUMA API functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.api = LumaAPITester("test_key")
        self.test_endpoint = "https://api.lumalabs.ai/dream-machine/v1/generations/image"
    
    def test_invalid_api_key(self):
        """Test handling of invalid API key."""
        with patch('requests.request') as mock_request:
            mock_response = MagicMock()
            mock_response.status_code = 401
            mock_response.ok = False
            mock_request.return_value = mock_response
            
            result = self.api.test_text_to_image("test prompt")
            self.assertEqual(result["status"], "error")
            self.assertIn("Invalid API key", result["details"]["error"])
    
    def test_malformed_image_url(self):
        """Test handling of malformed image URL."""
        with patch('requests.request') as mock_request:
            mock_response = MagicMock()
            mock_response.status_code = 400
            mock_response.ok = False
            mock_response.json.return_value = {"error": "Invalid image URL"}
            mock_request.return_value = mock_response
            
            result = self.api.test_image_reference("test prompt", "invalid_url")
            self.assertEqual(result["status"], "error")
            self.assertIn("Invalid", result["details"]["error"])
    
    def test_timeout_handling(self):
        """Test handling of API timeouts."""
        with patch('requests.request') as mock_request:
            mock_request.side_effect = requests.exceptions.Timeout
            
            result = self.api.test_text_to_image("test prompt")
            self.assertEqual(result["status"], "error")
            self.assertIn("timed out", result["details"]["error"])
    
    def test_network_error(self):
        """Test handling of network errors."""
        with patch('requests.request') as mock_request:
            mock_request.side_effect = requests.exceptions.ConnectionError
            
            result = self.api.test_text_to_image("test prompt")
            self.assertEqual(result["status"], "error")
            self.assertIn("Network error", result["details"]["error"])
    
    def test_successful_generation(self):
        """Test successful image generation."""
        with patch('requests.request') as mock_request:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.ok = True
            mock_response.json.return_value = {
                "id": "test_id",
                "status": "completed"
            }
            mock_request.return_value = mock_response
            
            result = self.api.test_text_to_image("test prompt")
            self.assertEqual(result["status"], "success")
            self.assertEqual(result["details"]["id"], "test_id")

if __name__ == '__main__':
    unittest.main()
