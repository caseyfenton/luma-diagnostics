"""Main diagnostics module for LUMA API."""

import os
import json
import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any

from . import tests
from . import api_tests
from . import utils
from . import generation_tests

def run_with_config(case_id: Optional[str] = None,
                   config_path: Optional[str] = None,
                   image_url: Optional[str] = None,
                   output_dir: Optional[str] = None) -> List[Dict[str, Any]]:
    """Run diagnostics with the given configuration."""
    results = []
    
    # Load configuration
    config = {}
    if config_path:
        with open(config_path, 'r') as f:
            config = json.load(f)
    if image_url:
        config["TEST_IMAGE_URL"] = image_url
    
    # Get API key if available
    api_key = config.get("LUMA_API_KEY")
    test_image_url = config.get("TEST_IMAGE_URL", os.environ.get("TEST_IMAGE_URL"))
    
    # Run basic tests
    if test_image_url:
        results.extend([
            tests.test_public_access(test_image_url),
            tests.test_cert_validation(test_image_url),
            tests.test_redirect(test_image_url),
            tests.test_headers_and_content(test_image_url),
            tests.test_image_validity(test_image_url)
        ])
    
    # Run API tests if key available
    if api_key:
        api_results = api_tests.run_api_tests(api_key, test_image_url)
        results.extend(api_results)
    
    # Generate output paths
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    if not output_dir:
        output_dir = config.get("OUTPUT_DIR", os.path.join(utils.get_config_dir(), "results"))
    if case_id:
        output_dir = os.path.join(output_dir, case_id)
    
    # Run generation tests
    if api_key:
        try:
            generation_report = generation_tests.run_generation_tests(
                api_key,
                test_image_url,
                output_dir
            )
            results.append({
                "test_name": "Generation Tests",
                "status": "completed",
                "details": generation_report
            })
        except Exception as e:
            results.append({
                "test_name": "Generation Tests",
                "status": "failed",
                "details": {
                    "error": str(e),
                    "info": "Failed to run generation tests"
                }
            })
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Save results
    json_file = os.path.join(output_dir, f"diagnostic_results_{timestamp}.json")
    text_file = os.path.join(output_dir, f"diagnostic_results_{timestamp}.txt")
    
    # Save JSON results
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump({
            "timestamp": timestamp,
            "case_id": case_id,
            "results": results
        }, f, indent=2)
    
    # Save text results
    with open(text_file, "w", encoding="utf-8") as f:
        f.write("LUMA API Diagnostics Results\n")
        f.write("=" * 30 + "\n\n")
        
        if case_id:
            f.write(f"Case ID: {case_id}\n")
        f.write(f"Timestamp: {timestamp}\n\n")
        
        for result in results:
            f.write(f"Test: {result['test_name']}\n")
            f.write("-" * 40 + "\n")
            
            if "details" in result:
                for k, v in result["details"].items():
                    f.write(f"{k}: {v}\n")
            
            f.write("\n")
    
    # Add output files to results
    results.append({
        "test_name": "Output Files",
        "status": "completed",
        "details": {
            "output_files": [
                json_file,
                text_file
            ]
        }
    })
    
    return results
