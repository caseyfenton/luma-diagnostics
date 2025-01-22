"""Command-line interface for LUMA Diagnostics."""

import os
import sys
import argparse
from pathlib import Path
from dotenv import load_dotenv
from . import diagnostics
from . import utils
import json

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
    parser.add_argument("--wizard", action="store_true", help="Run in interactive wizard mode")
    parser.add_argument("--case", help="Case ID to load configuration from")
    parser.add_argument("--image-url", help="Direct URL of image to test")
    parser.add_argument("--config", help="Path to configuration file")
    parser.add_argument("--output-dir", help="Directory to store results")
    
    args = parser.parse_args()
    
    try:
        if args.wizard:
            from . import wizard
            wizard.main()
            return
        
        results = diagnostics.run_with_config(
            case_id=args.case,
            config_path=args.config,
            image_url=args.image_url,
            output_dir=args.output_dir
        )
        
        # Find the output files from the results
        output_files = []
        for result in results:
            if result["test_name"] == "Output Files":
                output_files = result["details"]["output_files"]
                break
        
        print("\nDiagnostics completed successfully!")
        if output_files:
            print("Results saved to:")
            for f in output_files:
                print(f"  {f}")
        
        print("\nSummary of results:")
        print("-" * 40)
        for result in results:
            if result["test_name"] != "Output Files":  # Skip output files from summary
                print(f"\nTest: {result['test_name']}")
                print("-" * 40)
                
                if result["status"] == "completed":
                    if "details" in result:
                        for k, v in result["details"].items():
                            if isinstance(v, dict):
                                print(f"{k}:")
                                for sub_k, sub_v in v.items():
                                    print(f"  {sub_k}: {sub_v}")
                            else:
                                print(f"{k}: {v}")
                else:
                    if "details" in result and "error" in result["details"]:
                        print(f"Error: {result['details']['error']}")
                    else:
                        print(f"Status: {result['status']}")
        
    except Exception as e:
        print(f"Error running diagnostics: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    # Create necessary directories
    create_case_directories()

    # Load environment variables
    load_environment()

    main()
