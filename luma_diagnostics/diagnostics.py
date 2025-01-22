"""Core diagnostic functionality."""

import os
import json
from datetime import datetime
from pathlib import Path
from . import utils

def run_with_config(case_id=None, config_path=None, output_dir=None):
    """Run diagnostics with the specified configuration."""
    # Load configuration
    if config_path:
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        os.environ["LUMA_CONFIG_FILE"] = config_path
    
    # Set up output directory
    if output_dir:
        utils.ensure_dir_exists(output_dir)
    else:
        output_dir = utils.get_default_output_dir()
        if case_id:
            output_dir = output_dir / case_id
        utils.ensure_dir_exists(output_dir)
    
    # Generate output filenames with timestamp
    timestamp = datetime.now().strftime("%Y-%m-%dT%H%M%S")
    json_file = output_dir / f"{timestamp}-diagnostic.json"
    text_file = output_dir / f"{timestamp}-diagnostic.txt"
    
    # Run tests and collect results
    results = run_all_tests()
    
    # Add case information if available
    if case_id:
        case_info = {
            "test_name": "Case Information",
            "case_id": case_id,
            "timestamp": timestamp,
            "platform": utils.get_platform_info()
        }
        results.insert(0, case_info)
    
    # Save results
    save_results(results, json_file, text_file)
    
    return str(json_file), str(text_file)

def run_all_tests():
    """Run all diagnostic tests."""
    # Import the original test functions
    from .tests import (
        test_public_access,
        test_cert_validation,
        test_redirect,
        test_headers_content,
        test_image_validity,
        test_luma_json_request,
        test_rate_limit,
        test_http_head,
        test_latency_timeout,
        test_dns_records,
        test_sni_mismatch,
        test_traceroute,
        test_cors_check,
        test_firewall_ip_blocklist,
        test_hsts,
        test_user_agent_variation,
        test_image_metadata,
        test_content_encoding,
        test_api_auth,
        test_proxy_detection,
        test_advanced_image_analysis,
        test_enhanced_network_diagnostics
    )
    
    results = []
    url = os.environ.get("TEST_IMAGE_URL")
    if not url:
        raise ValueError("TEST_IMAGE_URL environment variable is required")
    
    # Run tests
    results.extend([
        test_public_access(url),
        test_cert_validation(url),
        test_redirect(url),
        test_headers_content(url),
        test_image_validity(url),
        test_http_head(url),
        test_latency_timeout(url),
        test_dns_records(url),
        test_sni_mismatch(url),
        test_traceroute(url),
        test_cors_check(url),
        test_firewall_ip_blocklist(url),
        test_hsts(url),
        test_user_agent_variation(url),
        test_image_metadata(url),
        test_content_encoding(url),
        test_proxy_detection(url),
        test_advanced_image_analysis(url),
        test_enhanced_network_diagnostics(url)
    ])
    
    # Run API tests if credentials available
    api_url = os.environ.get("LUMA_API_URL")
    bearer_token = os.environ.get("LUMA_API_KEY")
    if api_url and bearer_token:
        results.extend([
            test_luma_json_request(api_url, bearer_token, url),
            test_rate_limit(api_url, bearer_token, url),
            test_api_auth(api_url, bearer_token)
        ])
    
    return results

def save_results(results, json_file, text_file):
    """Save results to JSON and text files."""
    # Save JSON
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    
    # Save text
    with open(text_file, "w", encoding="utf-8") as f:
        for item in results:
            f.write(f"Test: {item['test_name']}\n")
            for k, v in item.items():
                if k != "test_name":
                    f.write(f"  {k}: {v}\n")
            f.write("\n")
