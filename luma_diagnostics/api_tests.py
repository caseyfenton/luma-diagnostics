"""LUMA Dream Machine API test functions."""

import os
import json
import time
import requests
from typing import Dict, List, Optional, Union

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
    
    def test_text_to_image(self, prompt: str, aspect_ratio: str = "16:9", 
                          model: str = "photon-1") -> Dict:
        """Test text to image generation."""
        endpoint = f"{self.api_url}/generations/image"
        payload = {
            "prompt": prompt,
            "aspect_ratio": aspect_ratio,
            "model": model
        }
        
        response = requests.post(endpoint, headers=self.headers, json=payload)
        return {
            "test_name": "Text to Image Generation",
            "endpoint": endpoint,
            "status_code": response.status_code,
            "response": response.json() if response.ok else None,
            "error": str(response.text) if not response.ok else None
        }
    
    def test_image_reference(self, prompt: str, image_url: str, 
                           weight: float = 0.85) -> Dict:
        """Test image reference generation."""
        endpoint = f"{self.api_url}/generations/image"
        payload = {
            "prompt": prompt,
            "image_ref": [{
                "url": image_url,
                "weight": weight
            }]
        }
        
        response = requests.post(endpoint, headers=self.headers, json=payload)
        return {
            "test_name": "Image Reference Generation",
            "endpoint": endpoint,
            "status_code": response.status_code,
            "response": response.json() if response.ok else None,
            "error": str(response.text) if not response.ok else None
        }
    
    def test_modify_image(self, prompt: str, image_url: str, 
                         weight: float = 1.0) -> Dict:
        """Test image modification."""
        endpoint = f"{self.api_url}/generations/image"
        payload = {
            "prompt": prompt,
            "modify_image_ref": {
                "url": image_url,
                "weight": weight
            }
        }
        
        response = requests.post(endpoint, headers=self.headers, json=payload)
        return {
            "test_name": "Image Modification",
            "endpoint": endpoint,
            "status_code": response.status_code,
            "response": response.json() if response.ok else None,
            "error": str(response.text) if not response.ok else None
        }
    
    def test_generation_status(self, generation_id: str) -> Dict:
        """Test getting generation status."""
        endpoint = f"{self.api_url}/generations/{generation_id}"
        response = requests.get(endpoint, headers=self.headers)
        return {
            "test_name": "Generation Status Check",
            "endpoint": endpoint,
            "status_code": response.status_code,
            "response": response.json() if response.ok else None,
            "error": str(response.text) if not response.ok else None
        }
    
    def test_list_generations(self, limit: int = 10, offset: int = 0) -> Dict:
        """Test listing generations."""
        endpoint = f"{self.api_url}/generations"
        params = {"limit": limit, "offset": offset}
        response = requests.get(endpoint, headers=self.headers, params=params)
        return {
            "test_name": "List Generations",
            "endpoint": endpoint,
            "status_code": response.status_code,
            "response": response.json() if response.ok else None,
            "error": str(response.text) if not response.ok else None
        }
    
    def test_delete_generation(self, generation_id: str) -> Dict:
        """Test deleting a generation."""
        endpoint = f"{self.api_url}/generations/{generation_id}"
        response = requests.delete(endpoint, headers=self.headers)
        return {
            "test_name": "Delete Generation",
            "endpoint": endpoint,
            "status_code": response.status_code,
            "response": response.json() if response.ok else None,
            "error": str(response.text) if not response.ok else None
        }
    
    def test_camera_motions(self) -> Dict:
        """Test getting supported camera motions."""
        endpoint = f"{self.api_url}/generations/camera_motion/list"
        response = requests.get(endpoint, headers=self.headers)
        return {
            "test_name": "Camera Motions List",
            "endpoint": endpoint,
            "status_code": response.status_code,
            "response": response.json() if response.ok else None,
            "error": str(response.text) if not response.ok else None
        }
    
    def run_all_tests(self, test_image_url: Optional[str] = None) -> List[Dict]:
        """Run all API tests."""
        results = []
        
        # Basic text to image test
        results.append(self.test_text_to_image(
            "A serene mountain lake at sunset with reflections in the water"
        ))
        
        # If test image provided, run image-based tests
        if test_image_url:
            results.append(self.test_image_reference(
                "Make it more vibrant and colorful",
                test_image_url
            ))
            
            results.append(self.test_modify_image(
                "Add snow falling in the scene",
                test_image_url
            ))
        
        # Get list of generations
        list_result = self.test_list_generations(limit=1)
        results.append(list_result)
        
        # If we have generations, test status and delete
        if list_result["response"] and list_result["response"].get("generations"):
            generation_id = list_result["response"]["generations"][0]["id"]
            results.append(self.test_generation_status(generation_id))
            # Don't delete by default, just test status
            # results.append(self.test_delete_generation(generation_id))
        
        # Test camera motions
        results.append(self.test_camera_motions())
        
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
