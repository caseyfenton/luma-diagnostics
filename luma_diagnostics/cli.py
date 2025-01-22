"""Command-line interface for LUMA Diagnostics."""

import os
import sys
import argparse
from pathlib import Path
from dotenv import load_dotenv
from . import diagnostics
from . import utils

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
    parser = argparse.ArgumentParser(description="LUMA Labs API Diagnostics Tool")
    parser.add_argument("--case", help="Case ID to load configuration from")
    parser.add_argument("--image-url", help="Direct URL of image to test")
    parser.add_argument("--config", help="Path to configuration file")
    parser.add_argument("--output-dir", help="Directory to store results")
    args = parser.parse_args()

    # Create necessary directories
    create_case_directories()

    # Load environment variables
    load_environment()

    # Handle direct image URL testing
    if args.image_url:
        os.environ["TEST_IMAGE_URL"] = args.image_url

    # Verify required environment variables
    if not os.environ.get("TEST_IMAGE_URL"):
        print("Error: TEST_IMAGE_URL is required. Provide it via --image-url or environment variable.", 
              file=sys.stderr)
        sys.exit(1)

    # Run diagnostics
    try:
        json_file, text_file = diagnostics.run_with_config(
            case_id=args.case,
            config_path=args.config,
            output_dir=args.output_dir
        )
        print(f"\nDiagnostics completed successfully!")
        print(f"Results saved to:")
        print(f"  JSON: {json_file}")
        print(f"  Text: {text_file}\n")
        
        # Print summary from text file
        print("Summary of results:")
        print("-" * 40)
        with open(text_file, 'r') as f:
            print(f.read())
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
