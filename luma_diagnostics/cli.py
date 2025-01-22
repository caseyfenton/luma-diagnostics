"""Command-line interface for LUMA Diagnostics."""

import os
import sys
import argparse
from pathlib import Path
from dotenv import load_dotenv
from . import diagnostics
from . import utils
from . import api_tests
from . import messages
import json
from rich.console import Console
from PIL import Image
import requests
from typing import Optional

console = Console()

def validate_image(image_path: str) -> Optional[str]:
    """Validate image file and return error message if invalid."""
    try:
        if not os.path.exists(image_path):
            return "Image file does not exist"
        
        with Image.open(image_path) as img:
            if img.format not in ['JPEG', 'PNG']:
                return "Image must be JPEG or PNG format"
            
            # Check reasonable size limits
            if img.size[0] * img.size[1] > 4096 * 4096:
                return "Image dimensions too large (max 4096x4096)"
            
        return None
    except Exception as e:
        return f"Invalid image file: {str(e)}"

def validate_api_key(api_key: str) -> Optional[str]:
    """Validate API key format and return error message if invalid."""
    if not api_key:
        return "API key is required"
    if not api_key.startswith("luma_"):
        return "Invalid API key format (should start with 'luma_')"
    if len(api_key) < 32:
        return "API key too short"
    return None

def run_tests(api_key: str, image_path: Optional[str] = None) -> bool:
    """Run diagnostic tests and return True if all pass."""
    tester = api_tests.LumaAPITester(api_key)
    all_passed = True
    
    # Basic API test
    messages.print_info("Running basic API test...")
    result = tester.test_text_to_image("A test prompt")
    if result["status"] == "error":
        messages.print_error(f"API test failed: {result['details']['error']}")
        all_passed = False
    else:
        messages.print_success("Basic API test passed")
    
    # Image test if provided
    if image_path:
        messages.print_info("Testing with provided image...")
        # First validate image locally
        error = validate_image(image_path)
        if error:
            messages.print_error(f"Image validation failed: {error}")
            all_passed = False
        else:
            # Test with API
            result = tester.test_image_reference("Test with this image", image_path)
            if result["status"] == "error":
                messages.print_error(f"Image test failed: {result['details']['error']}")
                all_passed = False
            else:
                messages.print_success("Image test passed")
    
    return all_passed

def create_case_directories():
    """Create necessary case directories if they don't exist."""
    base_dir = utils.get_config_dir()
    
    # Create directory structure
    for dir_name in ["templates", "active", "results"]:
        dir_path = base_dir / "cases" / dir_name
        dir_path.mkdir(parents=True, exist_ok=True)

def load_environment():
    """Load environment variables from various sources."""
    # Load from system environment first
    load_dotenv(os.path.expanduser("~/.env"))
    
    # Load from current directory if exists
    if os.path.exists(".env"):
        load_dotenv(".env")

def main():
    """Main entry point for the CLI."""
    try:
        parser = argparse.ArgumentParser(description="LUMA Diagnostics - Test and validate LUMA API functionality")
        parser.add_argument("--wizard", action="store_true", help="Run in interactive wizard mode")
        parser.add_argument("--image", help="Path to image file to test")
        parser.add_argument("--api-key", help="LUMA API key for generation tests")
        parser.add_argument("--case", help="Test case to run")
        parser.add_argument("--config", help="Path to configuration file")
        parser.add_argument("--output-dir", help="Directory to store results")
        parser.add_argument("--test", action="store_true", help="Run diagnostic tests")
        
        args = parser.parse_args()
        
        # Load environment variables
        load_environment()
        
        # Get API key from args or environment
        api_key = args.api_key or os.getenv("LUMA_API_KEY")
        
        if args.test:
            # Run diagnostic tests
            if not api_key:
                messages.print_error("API key is required. Provide with --api-key or set LUMA_API_KEY environment variable")
                sys.exit(1)
            
            error = validate_api_key(api_key)
            if error:
                messages.print_error(f"Invalid API key: {error}")
                sys.exit(1)
            
            if args.image:
                error = validate_image(args.image)
                if error:
                    messages.print_error(f"Invalid image: {error}")
                    sys.exit(1)
            
            success = run_tests(api_key, args.image)
            sys.exit(0 if success else 1)
            
        elif args.wizard:
            from . import wizard
            try:
                wizard.main()
            except KeyboardInterrupt:
                sys.exit(0)
        else:
            if args.case:
                diagnostics.run_case(args.case, api_key)
            else:
                parser.print_help()
                sys.exit(2)
                
    except Exception as e:
        console.print(f"[red]Error:[/red] {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    # Create necessary directories
    create_case_directories()
    
    # Run main CLI
    main()
