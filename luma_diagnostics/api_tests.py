"""LUMA Dream Machine API test functions."""

import os
import json
import time
import requests
from typing import Dict, List, Optional, Union
from . import messages

class LumaAPITester:
    """Test suite for LUMA Dream Machine API."""
    
    def __init__(self, api_key: str, api_url: str = "https://api.lumalabs.ai/dream-machine/v1"):
        """Initialize the API tester."""
        self.api_key = api_key
        self.api_url = api_url.rstrip('/')
        self.headers = {
            'accept': 'application/json',
            'authorization': f'Bearer {api_key}',
            'content-type': 'application/json'
        }
    
    def _make_request(self, method: str, endpoint: str, payload: Dict = None, 
                     timeout: int = 30) -> Dict:
        """Make an API request with error handling."""
        try:
            response = requests.request(
                method=method,
                url=endpoint,
                headers=self.headers,
                json=payload,
                timeout=timeout
            )
            
            if response.status_code == 401:
                return {
                    "status": "error",
                    "details": {
                        "error": "Invalid API key. Please check your credentials.",
                        "status_code": 401
                    }
                }
            elif response.status_code == 400:
                return {
                    "status": "error",
                    "details": {
                        "error": response.json().get("error", "Invalid request parameters"),
                        "status_code": 400
                    }
                }
            elif not response.ok:
                return {
                    "status": "error",
                    "details": {
                        "error": f"API request failed: {response.text}",
                        "status_code": response.status_code
                    }
                }
            
            return {
                "status": "success",
                "details": response.json()
            }
            
        except requests.exceptions.Timeout:
            return {
                "status": "error",
                "details": {
                    "error": f"Request timed out after {timeout} seconds",
                    "status_code": None
                }
            }
        except requests.exceptions.RequestException as e:
            return {
                "status": "error",
                "details": {
                    "error": f"Network error: {str(e)}",
                    "status_code": None
                }
            }
    
    def test_text_to_image(self, prompt: str, aspect_ratio: str = "16:9", 
                          model: str = "photon-1", timeout: int = 30) -> Dict:
        """Test text to image generation."""
        endpoint = f"{self.api_url}/generations/image"
        payload = {
            "prompt": prompt,
            "aspect_ratio": aspect_ratio,
            "model": model
        }
        
        result = self._make_request("POST", endpoint, payload, timeout)
        return {
            "test_name": "Text to Image Generation",
            "status": result["status"],
            "details": {
                "endpoint": endpoint,
                **result["details"]
            }
        }
    
    def test_image_reference(self, prompt: str, image_url: str, 
                           weight: float = 0.85, timeout: int = 30) -> Dict:
        """Test image reference generation."""
        endpoint = f"{self.api_url}/generations/image"
        payload = {
            "prompt": prompt,
            "image_ref": [{
                "url": image_url,
                "weight": weight
            }]
        }
        
        result = self._make_request("POST", endpoint, payload, timeout)
        return {
            "test_name": "Image Reference Generation",
            "status": result["status"],
            "details": {
                "endpoint": endpoint,
                **result["details"]
            }
        }
    
    def test_generation_status(self, generation_id: str, timeout: int = 30) -> Dict:
        """Test getting generation status."""
        endpoint = f"{self.api_url}/generations/{generation_id}"
        
        result = self._make_request("GET", endpoint, timeout=timeout)
        return {
            "test_name": "Generation Status Check",
            "status": result["status"],
            "details": {
                "endpoint": endpoint,
                **result["details"]
            }
        }
    
    def mock_test(self) -> Dict:
        """Run a simulated test that demonstrates test result formatting without making actual API calls."""
        return {
            "status": "success",
            "test_name": "Mock Test",
            "details": {
                # Basic tests
                "Public Access": {
                    "status": "success",
                    "message": "The image is publicly accessible and can be reached by Luma servers.",
                    "details": {"response_time_ms": 120, "content_length": 54321}
                },
                "SSL Certificate": {
                    "status": "success",
                    "message": "SSL certificate is valid and trusted.",
                    "details": {"issuer": "Let's Encrypt", "expiry": "2025-12-31"}
                },
                "URL Redirect": {
                    "status": "warning",
                    "message": "URL redirects to another location. This may cause issues with some API endpoints.",
                    "details": {"original_url": "http://example.com/image.jpg", "final_url": "https://cdn.example.com/image.jpg"}
                },
                "HTTP Headers": {
                    "status": "success",
                    "message": "All required HTTP headers are present.",
                    "details": {"content_type": "image/jpeg", "content_length": "54321"}
                },
                "Image Validity": {
                    "status": "success",
                    "message": "Image format is valid and supported by LUMA APIs.",
                    "details": {"format": "JPEG", "dimensions": "1024x768", "size_kb": 450}
                }
            }
        }
    
    def run_all_tests(self, test_image_url: Optional[str] = None) -> List[Dict]:
        """Run all API tests."""
        results = []
        
        # Test text to image generation
        text_result = self.test_text_to_image(
            "A beautiful sunset over mountains",
            aspect_ratio="16:9"
        )
        results.append(text_result)
        
        # If we have an image URL, test image reference
        if test_image_url:
            ref_result = self.test_image_reference(
                "Make this more vibrant",
                test_image_url
            )
            results.append(ref_result)
        
        # Check generation status if we got a successful generation
        if text_result["status"] == "success" and "id" in text_result["details"]:
            status_result = self.test_generation_status(text_result["details"]["id"])
            results.append(status_result)
        
        return results

def run_api_tests(api_key: Optional[str] = None, 
                 test_image_url: Optional[str] = None) -> List[Dict]:
    """Run all API tests with the provided key or from environment."""
    if not api_key:
        api_key = os.environ.get("LUMA_API_KEY")
    
    if not api_key:
        return [{
            "test_name": "API Tests",
            "error": "No API key provided. Get one from https://lumalabs.ai/dream-machine/api/keys"
        }]
    
    tester = LumaAPITester(api_key)
    return tester.run_all_tests(test_image_url)
