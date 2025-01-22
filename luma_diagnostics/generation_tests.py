"""LUMA Dream Machine Generation Tests.

This module contains tests for LUMA's image and video generation capabilities.
"""
import os
import time
import json
from typing import Dict, Optional, Any
import requests
from datetime import datetime

class GenerationTest:
    """Test LUMA's generation capabilities."""

    def __init__(self, api_key: str, test_image_url: str):
        self.api_key = api_key
        self.test_image_url = test_image_url
        self.base_url = "https://api.lumalabs.ai/dream-machine/v1"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        self.results = []

    def _wait_for_completion(self, generation_id: str, timeout: int = 300) -> Dict[str, Any]:
        """Wait for a generation to complete."""
        start_time = time.time()
        while True:
            response = requests.get(
                f"{self.base_url}/generations/{generation_id}",
                headers=self.headers
            )
            data = response.json()
            
            if data["state"] == "completed":
                return data
            elif data["state"] == "failed":
                raise Exception(f"Generation failed: {data.get('failure_reason')}")
            elif time.time() - start_time > timeout:
                raise TimeoutError(f"Generation timed out after {timeout} seconds")
            
            time.sleep(5)

    def _save_result(self, test_name: str, result: Dict[str, Any], output_dir: str):
        """Save test result to the output directory."""
        os.makedirs(output_dir, exist_ok=True)
        
        # Add metadata
        result["test_name"] = test_name
        result["test_timestamp"] = datetime.now().isoformat()
        result["test_image_url"] = self.test_image_url
        
        # Save to results list
        self.results.append(result)
        
        # Save individual test result
        filename = f"{test_name}_{result['id']}.json"
        with open(os.path.join(output_dir, filename), "w") as f:
            json.dump(result, f, indent=2)

    def test_text_to_image(self, prompt: str, output_dir: str) -> Dict[str, Any]:
        """Test text-to-image generation."""
        data = {
            "model": "photon-1",
            "prompt": prompt,
            "aspect_ratio": "16:9"
        }
        
        response = requests.post(
            f"{self.base_url}/generations/image",
            headers=self.headers,
            json=data
        )
        response.raise_for_status()
        
        result = self._wait_for_completion(response.json()["id"])
        self._save_result("text_to_image", result, output_dir)
        return result

    def test_image_to_image(self, prompt: str, output_dir: str) -> Dict[str, Any]:
        """Test image-to-image generation."""
        data = {
            "model": "photon-1",
            "prompt": prompt,
            "image_ref": [{
                "url": self.test_image_url,
                "weight": 0.85
            }],
            "aspect_ratio": "16:9"
        }
        
        response = requests.post(
            f"{self.base_url}/generations/image",
            headers=self.headers,
            json=data
        )
        response.raise_for_status()
        
        result = self._wait_for_completion(response.json()["id"])
        self._save_result("image_to_image", result, output_dir)
        return result

    def test_image_to_video(self, prompt: str, camera_motion: str, output_dir: str) -> Dict[str, Any]:
        """Test image-to-video generation."""
        data = {
            "model": "ray-1-6",
            "prompt": prompt,
            "keyframes": {
                "frame0": {
                    "type": "image",
                    "url": self.test_image_url
                }
            },
            "loop": False,
            "aspect_ratio": "16:9",
            "camera_motion": camera_motion
        }
        
        response = requests.post(
            f"{self.base_url}/generations",
            headers=self.headers,
            json=data
        )
        response.raise_for_status()
        
        result = self._wait_for_completion(response.json()["id"])
        self._save_result("image_to_video", result, output_dir)
        return result

    def generate_report(self, output_dir: str) -> str:
        """Generate a human-readable report of all test results."""
        report = []
        report.append("LUMA Dream Machine Generation Test Results")
        report.append("=" * 50)
        report.append(f"Test Image: {self.test_image_url}")
        report.append(f"Timestamp: {datetime.now().isoformat()}")
        report.append("-" * 50)
        
        for result in self.results:
            report.append(f"\nTest: {result['test_name']}")
            report.append(f"Generation ID: {result['id']}")
            report.append(f"Status: {result['state']}")
            report.append(f"Model: {result['model']}")
            
            if result['state'] == 'completed':
                if result['assets'].get('image'):
                    report.append(f"Generated Image: {result['assets']['image']}")
                if result['assets'].get('video'):
                    report.append(f"Generated Video: {result['assets']['video']}")
            elif result['state'] == 'failed':
                report.append(f"Failure Reason: {result.get('failure_reason')}")
            
            report.append(f"Creation Time: {result['created_at']}")
            report.append("-" * 30)
        
        report_text = "\n".join(report)
        
        # Save report
        report_path = os.path.join(output_dir, "generation_test_report.txt")
        with open(report_path, "w") as f:
            f.write(report_text)
        
        return report_text

def run_generation_tests(api_key: str, test_image_url: str, output_dir: str) -> str:
    """Run all generation tests and return the report."""
    tester = GenerationTest(api_key, test_image_url)
    
    # Test text-to-image
    tester.test_text_to_image(
        "A teddy bear in sunglasses playing electric guitar and dancing",
        output_dir
    )
    
    # Test image-to-image
    tester.test_image_to_image(
        "Transform into a futuristic cyborg teddy bear",
        output_dir
    )
    
    # Test image-to-video with different camera motions
    for motion in ["Orbit Left", "Push In", "Pan Right"]:
        tester.test_image_to_video(
            "A lively scene with dynamic movement",
            motion,
            output_dir
        )
    
    return tester.generate_report(output_dir)
