"""Command line interface for LUMA diagnostics."""

import os
import sys
import argparse
from pathlib import Path
from dotenv import load_dotenv
from . import utils
from . import api_tests
from . import messages
from . import wizard
from . import mock_tests
from .case_manager import CaseManager
from rich.console import Console
from PIL import Image
from typing import Optional
import json
from . import __version__

console = Console()

class CaseManager:
    def __init__(self):
        self.current_case = None
        self.cases_dir = utils.get_config_dir() / "cases"

    def create_case(self, title, description):
        case_id = utils.generate_id()
        case_dir = self.cases_dir / case_id
        case_dir.mkdir(parents=True, exist_ok=True)
        with open(case_dir / "case.json", "w") as f:
            json.dump({"title": title, "description": description, "test_results": []}, f)
        messages.print_success(f"Case created: {case_id}")

    def list_cases(self):
        cases = []
        for case_dir in self.cases_dir.iterdir():
            if case_dir.is_dir():
                with open(case_dir / "case.json", "r") as f:
                    case_data = json.load(f)
                    cases.append({"id": case_dir.name, "title": case_data["title"]})
        return cases

    def get_case(self, case_id):
        case_dir = self.cases_dir / case_id
        if case_dir.is_dir():
            with open(case_dir / "case.json", "r") as f:
                return json.load(f)
        return None

    def select_case(self, case_id):
        case = self.get_case(case_id)
        if case:
            self.current_case = case_id
            messages.print_success(f"Selected case: {case['title']}")
            return True
        return False

    def add_test_result(self, result):
        if not self.current_case:
            return False
        case_dir = self.cases_dir / self.current_case
        with open(case_dir / "case.json", "r") as f:
            case = json.load(f)
        case["test_results"].append(result)
        with open(case_dir / "case.json", "w") as f:
            json.dump(case, f)
        return True

    def export_case(self, case_id, output_dir):
        case = self.get_case(case_id)
        if not case:
            raise ValueError(f"Case {case_id} not found")
        output_path = Path(output_dir) / f"luma_case_{case_id}.json"
        with open(output_path, "w") as f:
            json.dump(case, f, indent=2)
        return str(output_path)

    def format_case_summary(self, case):
        if isinstance(case, dict) and "id" in case:
            case_id = case["id"]
            case = self.get_case(case_id) or case
            case["id"] = case_id
        return f"Case: {case.get('title')}\nID: {case.get('id')}\nDescription: {case.get('description')}\nTests: {len(case.get('test_results', []))}"

def validate_image(image_path: str) -> Optional[str]:
    """Validate image file and return error message if invalid."""
    try:
        if not os.path.exists(image_path):
            return f"Image file not found: {image_path}"
        img = Image.open(image_path)
        img.verify()
        return None
    except Exception as e:
        return str(e)

def main():
    """Main entry point for the CLI."""
    # Create the main parser
    parser = argparse.ArgumentParser(
        description="LUMA Diagnostics - Test and troubleshoot LUMA API issues with ease",
        epilog="For more detailed help on specific topics, try: luma-diagnostics --case-help"
    )
    
    # Common arguments group
    common_group = parser.add_argument_group("Common Tasks")
    common_group.add_argument("--wizard", action="store_true", 
                              help="Start the interactive wizard (recommended for beginners)")
    common_group.add_argument("--test", action="store_true", 
                              help="Run a basic API test to verify your setup")
    common_group.add_argument("--image", metavar="PATH", 
                              help="Test a specific image file with the LUMA API")
    common_group.add_argument("--demo", action="store_true",
                              help="Run in demo mode - no API key required")
    
    # Configuration group
    config_group = parser.add_argument_group("Configuration")
    config_group.add_argument("--api-key", help="Your LUMA API key (or set LUMA_API_KEY in env)")
    config_group.add_argument("--config", help="Path to configuration file")
    config_group.add_argument("--output-dir", help="Directory to store test results")
    config_group.add_argument("--version", action="version", 
                              version=f"LUMA Diagnostics v{__version__}")
    
    # Optional case reference (lightweight usage)
    parser.add_argument("--case", metavar="CASE_ID", 
                        help="Reference an existing test case (for adding results)")
    
    # Hidden case management arguments - only shown with --case-help
    case_group = parser.add_argument_group(
        "Case Management (Advanced)",
        "For detailed help on case management, run: luma-diagnostics --case-help"
    )
    case_group.add_argument("--create-case", help=argparse.SUPPRESS)
    case_group.add_argument("--case-description", help=argparse.SUPPRESS)
    case_group.add_argument("--list-cases", action="store_true", help=argparse.SUPPRESS)
    case_group.add_argument("--view-case", help=argparse.SUPPRESS)
    case_group.add_argument("--select-case", help=argparse.SUPPRESS)
    case_group.add_argument("--export-case", help=argparse.SUPPRESS)
    case_group.add_argument("--case-help", action="store_true", help="Show detailed help for case management")
    
    args = parser.parse_args()
    
    # Show case management help if requested
    if args.case_help:
        print_case_help()
        return
    
    # Initialize case manager
    case_manager = CaseManager()
    
    # Handle case management commands
    if args.create_case:
        description = args.case_description or "No description provided"
        case_manager.create_case(args.create_case, description)
        return
    
    if args.list_cases:
        cases = case_manager.list_cases()
        if not cases:
            messages.print_info("No cases found")
            return
        for case in cases:
            print("\n" + case_manager.format_case_summary(case))
        return
    
    if args.view_case:
        case = case_manager.get_case(args.view_case)
        if not case:
            messages.print_error(f"Case {args.view_case} not found")
            return
        print("\n" + case_manager.format_case_summary(case))
        return
    
    if args.select_case:
        if not case_manager.select_case(args.select_case):
            messages.print_error(f"Case {args.select_case} not found")
            return
    
    if args.export_case:
        try:
            output_dir = args.output_dir or os.getcwd()
            output_file = case_manager.export_case(args.export_case, output_dir)
            messages.print_success(f"Case exported to: {output_file}")
            messages.print_info("You can send this file to support@lumalabs.ai for assistance")
            return
        except ValueError as e:
            messages.print_error(str(e))
            return
    
    # If no case management commands, proceed with normal operation
    try:
        if args.wizard:
            if args.demo:
                # Run the demo wizard
                wizard.run_demo_wizard()
            else:
                wizard.run_wizard()
        elif args.demo:
            # Run in demo mode - doesn't require an API key
            image_path = args.image if args.image else None
            mock_tests.run_mock_tests(image_path)
        elif args.test or args.image:
            api_key = args.api_key or os.getenv("LUMA_API_KEY")
            if not api_key:
                messages.print_error("No API key provided. Use --api-key or set LUMA_API_KEY environment variable")
                messages.print_info("Tip: Try --demo mode if you just want to see how the tool works")
                sys.exit(1)
            
            tester = api_tests.LumaAPITester(api_key)
            result = {}
            
            if args.test:
                messages.print_info("Running basic API test...")
                result = tester.test_text_to_image(prompt="LUMA Diagnostics test prompt")
                if result["status"] == "success":
                    messages.print_success("Basic API test passed")
                else:
                    messages.print_error(f"Basic API test failed: {result.get('error', 'Unknown error')}")
                    sys.exit(1)
            
            if args.image:
                messages.print_info("Testing with provided image...")
                result = tester.test_image_reference(args.image)
                if result["status"] == "success":
                    messages.print_success("Image test passed")
                else:
                    messages.print_error(f"Image test failed: {result.get('error', 'Unknown error')}")
                    sys.exit(1)
            
            # Add test result to current case if one is selected
            if case_manager.current_case:
                case_manager.add_test_result(result)
            
            # Exit with success if we've run any tests
            if args.test or args.image:
                sys.exit(0)
        else:
            print("\nLUMA Diagnostics - Help")
            print("\nThis tool helps you troubleshoot issues with LUMA APIs.")
            print("\nRecommended commands for beginners:")
            print("  luma-diagnostics --wizard          Start the interactive guided wizard")
            print("  luma-diagnostics --test            Run a basic API test")
            print("  luma-diagnostics --image IMAGE     Test a specific image")
            print("  luma-diagnostics --demo            Run in demo mode (no API key required)\n")
            
            parser.print_help()
            sys.exit(2)
            
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        messages.print_error(str(e))
        sys.exit(1)

def print_case_help():
    """Print detailed help for case management functionality."""
    console.print("\n[bold cyan]LUMA Diagnostics - Case Management Help[/bold cyan]\n")
    console.print("Cases allow you to organize and track multiple diagnostic tests for sharing with support.")
    console.print("This is an [italic]advanced feature[/italic] primarily used when working with LUMA support team.\n")
    
    console.print("[bold]Available Commands:[/bold]\n")
    console.print("  [yellow]--create-case TITLE[/yellow]          Create a new test case with the given title")
    console.print("  [yellow]--case-description TEXT[/yellow]      Add a description to a new case")
    console.print("  [yellow]--list-cases[/yellow]                 List all your existing cases")
    console.print("  [yellow]--view-case CASE_ID[/yellow]          View details of a specific case")
    console.print("  [yellow]--select-case CASE_ID[/yellow]        Select a case to add test results to")
    console.print("  [yellow]--export-case CASE_ID[/yellow]        Export a case to send to support\n")
    
    console.print("[bold]Example Usage:[/bold]\n")
    console.print("  # Create a new case to track tests")
    console.print("  luma-diagnostics --create-case \"My API Issue\" --case-description \"Problems with landscape images\"\n")
    
    console.print("  # Run tests and add results to a case")
    console.print("  luma-diagnostics --select-case abcd1234 --test\n")
    
    console.print("  # Export a case to share with support")
    console.print("  luma-diagnostics --export-case abcd1234\n")

if __name__ == "__main__":
    main()
