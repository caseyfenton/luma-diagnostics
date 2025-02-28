#!/usr/bin/env python3

import os
import sys
import time
import json
from typing import Optional, Dict, Any
from pathlib import Path
import questionary
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeRemainingColumn
from rich import print as rprint
from . import diagnostics
from . import utils
from . import settings
from . import mock_tests
import datetime
import re
from rich import box

console = Console()

# Initialize settings
SETTINGS = settings.Settings()

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_welcome():
    """Print welcome message."""
    clear_screen()
    console.print(Panel.fit(
        "[bold blue]Welcome to LUMA Diagnostics![/bold blue]\n\n"
        "This wizard will help you test your images with LUMA's Dream Machine API.\n"
        "We'll guide you through the process step by step.",
        title="LUMA Diagnostics Wizard",
        border_style="blue"
    ))
    time.sleep(1)

def mask_api_key(key: str) -> str:
    """Mask API key, showing only the last 4 characters."""
    if not key or len(key) < 4:
        return "****"
    return f"{'*' * (len(key) - 4)}{key[-4:]}"

def run_wizard():
    """Entry point for the wizard, called from the CLI."""
    main()

def get_image_url() -> Optional[str]:
    """Get the image URL from the user."""
    try:
        last_url = SETTINGS.get_last_image_url()
        
        # Build choices dynamically
        choices = ["Enter a new URL"]
        if last_url != settings.Settings.DEFAULT_TEST_IMAGE:  # Only add if there's a real last tested image
            choices.append(f"Use last tested image ({last_url})")
        choices.append("Use LUMA sample image (teddy bear)")
        
        questions = [
            {
                "type": "select",
                "name": "url_source",
                "message": "Which image would you like to test?",
                "choices": choices
            },
            {
                "type": "text",
                "name": "image_url",
                "message": "Enter the URL of the image you want to test:",
                "validate": lambda url: True if url.startswith(('http://', 'https://')) else "Please enter a valid HTTP(S) URL",
                "when": lambda x: x["url_source"] == "Enter a new URL"
            }
        ]
        
        answers = questionary.prompt(questions)
        if answers is None:  # User cancelled
            return None
        
        if answers["url_source"] == "Enter a new URL":
            url = answers["image_url"]
        elif answers["url_source"].startswith("Use last tested"):
            url = last_url
        else:
            url = settings.Settings.DEFAULT_TEST_IMAGE
        
        SETTINGS.set_last_image_url(url)
        return url
    
    except KeyboardInterrupt:
        return None

def get_api_key() -> Optional[str]:
    """Get API key from environment, settings, or user input."""
    # Try environment variable first
    api_key = os.getenv("LUMA_API_KEY")
    if api_key:
        console.print("[green]Found API key in environment variables[/green]")
        return api_key
    
    # Try settings file
    api_key = SETTINGS.get_api_key()
    if api_key:
        # Show last 4 characters of existing key
        masked_key = "*" * (len(api_key) - 4) + api_key[-4:]
        console.print(f"[green]Found saved API key:[/green] {masked_key}")
        if questionary.confirm("Would you like to use this API key?").ask():
            return api_key
    
    # Ask for new key
    api_key = questionary.password("Please enter your LUMA API key:").ask()
    if not api_key:
        return None
    
    # Ask about saving the key
    save_options = [
        "Yes, save to ~/.env file (recommended)",
        "Yes, save to settings file",
        "No, don't save"
    ]
    
    save_choice = questionary.select(
        "Would you like to save this API key for future use?",
        choices=save_options,
        default=save_options[0]
    ).ask()
    
    if save_choice == save_options[0]:  # Save to ~/.env
        if SETTINGS.save_api_key_to_env(api_key):
            console.print("[green]API key saved to ~/.env file[/green]")
            console.print("Note: You may need to restart your terminal for the environment variable to take effect")
    elif save_choice == save_options[1]:  # Save to settings
        SETTINGS.set_api_key(api_key)
        console.print("[green]API key saved to settings file[/green]")
    
    return api_key

def get_test_type(api_key: Optional[str]) -> str:
    """Get the type of test to run."""
    last_test = SETTINGS.get_last_test_type()
    
    choices = ["Basic Image Test"]
    if api_key:
        choices.extend([
            "Text-to-Image Generation",
            "Image-to-Image Generation",
            "Image-to-Video Generation",
            "Full Test Suite"
        ])
    
    questions = [
        {
            "type": "select",
            "name": "test_type",
            "message": "What type of test would you like to run?",
            "choices": [f"Use last test type ({last_test})"] + choices if last_test else choices,
            "default": last_test if last_test in choices else choices[0]
        }
    ]
    
    answers = questionary.prompt(questions)
    if answers is None:  # User cancelled
        return None
    
    test_type = answers["test_type"]
    
    if test_type.startswith("Use last test type"):
        test_type = last_test
    
    SETTINGS.set_last_test_type(test_type)
    return test_type

def get_generation_params(test_type: str) -> Dict[str, Any]:
    """Get generation-specific parameters."""
    last_params = SETTINGS.get_last_params()
    
    if test_type == "Text-to-Image Generation":
        questions = [
            {
                "type": "select",
                "name": "param_source",
                "message": "Which parameters would you like to use?",
                "choices": [
                    "Use new parameters",
                    "Use last parameters" if last_params else "Use default parameters"
                ]
            },
            {
                "type": "text",
                "name": "prompt",
                "message": "Enter your text prompt:",
                "default": last_params.get("prompt", "A serene mountain lake at sunset with reflections in the water"),
                "when": lambda x: x["param_source"] == "Use new parameters"
            },
            {
                "type": "select",
                "name": "aspect_ratio",
                "message": "Choose aspect ratio:",
                "choices": ["16:9", "4:3", "1:1", "9:16"],
                "default": last_params.get("aspect_ratio", "16:9"),
                "when": lambda x: x["param_source"] == "Use new parameters"
            }
        ]
        
        answers = questionary.prompt(questions)
        if answers is None:  # User cancelled
            return None
        
        if answers["param_source"] == "Use new parameters":
            params = {
                "prompt": answers["prompt"],
                "aspect_ratio": answers["aspect_ratio"]
            }
        else:
            params = last_params if last_params else {
                "prompt": "A serene mountain lake at sunset with reflections in the water",
                "aspect_ratio": "16:9"
            }
    
    elif test_type == "Image-to-Image Generation":
        questions = [
            {
                "type": "select",
                "name": "param_source",
                "message": "Which parameters would you like to use?",
                "choices": [
                    "Use new parameters",
                    "Use last parameters" if last_params else "Use default parameters"
                ]
            },
            {
                "type": "text",
                "name": "prompt",
                "message": "Enter your modification prompt:",
                "default": last_params.get("prompt", "Make it more vibrant and colorful"),
                "when": lambda x: x["param_source"] == "Use new parameters"
            }
        ]
        
        answers = questionary.prompt(questions)
        if answers is None:  # User cancelled
            return None
        
        if answers["param_source"] == "Use new parameters":
            params = {"prompt": answers["prompt"]}
        else:
            params = last_params if last_params else {
                "prompt": "Make it more vibrant and colorful"
            }
    
    elif test_type == "Image-to-Video Generation":
        questions = [
            {
                "type": "select",
                "name": "param_source",
                "message": "Which parameters would you like to use?",
                "choices": [
                    "Use new parameters",
                    "Use last parameters" if last_params else "Use default parameters"
                ]
            },
            {
                "type": "select",
                "name": "camera_motion",
                "message": "Choose camera motion:",
                "choices": [
                    "Static", "Move Left", "Move Right", "Move Up", "Move Down",
                    "Push In", "Pull Out", "Zoom In", "Zoom Out", "Pan Left",
                    "Pan Right", "Orbit Left", "Orbit Right", "Crane Up", "Crane Down"
                ],
                "default": last_params.get("camera_motion", "Orbit Left"),
                "when": lambda x: x["param_source"] == "Use new parameters"
            },
            {
                "type": "text",
                "name": "duration",
                "message": "Enter duration in seconds:",
                "default": str(last_params.get("duration", "3.0")),
                "validate": lambda x: True if x.replace(".", "").isdigit() else "Please enter a valid number",
                "when": lambda x: x["param_source"] == "Use new parameters"
            }
        ]
        
        answers = questionary.prompt(questions)
        if answers is None:  # User cancelled
            return None
        
        if answers["param_source"] == "Use new parameters":
            params = {
                "camera_motion": answers["camera_motion"],
                "duration": float(answers["duration"])
            }
        else:
            params = last_params if last_params else {
                "camera_motion": "Orbit Left",
                "duration": 3.0
            }
    
    else:
        params = {}
    
    SETTINGS.set_last_params(params)
    return params

def sanitize_filename(text: str) -> str:
    """Convert text to filesystem-friendly format."""
    # Replace spaces and special chars with underscores
    sanitized = re.sub(r'[^\w\s-]', '_', text)
    sanitized = re.sub(r'[-\s]+', '_', sanitized)
    return sanitized.strip('_').lower()

def create_case_id(customer: str, title: str) -> str:
    """Create a case ID from customer name and title."""
    timestamp = datetime.datetime.now().strftime("%Y%m%d")
    
    # If no customer name provided, use 'no_customer'
    customer = customer.strip() if customer.strip() else "no_customer"
    
    # Sanitize both parts
    customer_part = sanitize_filename(customer)
    title_part = sanitize_filename(title)
    
    # Combine with timestamp
    return f"{customer_part}-{title_part}-{timestamp}"

def create_case(image_url: str, api_key: Optional[str], test_type: str, params: Dict[str, Any], test_results: Dict[str, Any]) -> Optional[str]:
    """Create a case file with test results and additional information. Returns case directory if created."""
    try:
        # Ask if user wants to create a case
        if not questionary.confirm("Would you like to create a case with these test results?").ask():
            return None
        
        # Get case information
        questions = [
            {
                "type": "text",
                "name": "title",
                "message": "Enter a title for this case:",
                "validate": lambda x: len(x) > 0
            },
            {
                "type": "text",
                "name": "customer",
                "message": "Customer name or organization:",
            },
            {
                "type": "text",
                "name": "description",
                "message": "Enter a description of the issue or technical context:",
                "validate": lambda x: len(x) > 0
            },
            {
                "type": "select",
                "name": "priority",
                "message": "Select priority level:",
                "choices": ["P0 - Critical", "P1 - High", "P2 - Medium", "P3 - Low"],
                "default": "P2 - Medium"
            }
        ]
        
        case_info = questionary.prompt(questions)
        if not case_info:  # User cancelled
            return None
        
        # Extract priority level
        case_info['priority'] = case_info['priority'].split(' - ')[0]
        
        # Create case ID and directory
        case_id = create_case_id(case_info['customer'], case_info['title'])
        case_dir = os.path.join("cases", "active", case_id)
        os.makedirs(case_dir, exist_ok=True)
        
        # Create test results files
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        results_base = os.path.join(case_dir, f"test_{timestamp}")
        
        # Save JSON results
        with open(f"{results_base}.json", "w") as f:
            json.dump({
                "timestamp": timestamp,
                "image_url": image_url,
                "test_type": test_type,
                "parameters": params,
                "results": test_results
            }, f, indent=2)
        
        # Save human-readable results
        with open(f"{results_base}.txt", "w") as f:
            f.write(f"Test Results - {timestamp}\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Image URL: {image_url}\n")
            f.write(f"Test Type: {test_type}\n\n")
            
            if params:
                f.write("Test Parameters:\n")
                for key, value in params.items():
                    f.write(f"- {key}: {value}\n")
                f.write("\n")
            
            f.write("Results:\n")
            for test_name, result in test_results.items():
                f.write(f"\n{test_name}:\n")
                f.write("-" * 30 + "\n")
                if isinstance(result, dict):
                    for key, value in result.items():
                        f.write(f"- {key}: {value}\n")
                else:
                    f.write(f"- {result}\n")
        
        # Create or update case file
        case_file = os.path.join(case_dir, "README.md")  # Using README.md for better GitHub/GitLab visibility
        if not os.path.exists(case_file):
            # Create new case file
            with open(case_file, "w") as f:
                f.write(f"# {case_info['title']}\n\n")
                f.write("## Case Information\n\n")
                f.write(f"- **Case ID**: {case_id}\n")
                f.write(f"- **Created**: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"- **Priority**: {case_info['priority']}\n")
                if case_info['customer']:
                    f.write(f"- **Customer**: {case_info['customer']}\n")
                f.write("\n## Description\n\n")
                f.write(case_info['description'])
                f.write("\n\n## Test Results\n\n")
        
        # Append test results to case file
        with open(case_file, "a") as f:
            f.write(f"\n### Test Run - {timestamp}\n\n")
            f.write(f"- **Image URL**: {image_url}\n")
            f.write(f"- **Test Type**: {test_type}\n")
            if params:
                f.write("- **Test Parameters**:\n")
                for key, value in params.items():
                    f.write(f"  - {key}: {value}\n")
            
            f.write("\n#### Results Summary\n\n")
            for test_name, result in test_results.items():
                f.write(f"##### {test_name}\n\n")
                if isinstance(result, dict):
                    for key, value in result.items():
                        f.write(f"- **{key}**: {value}\n")
                else:
                    f.write(f"- {result}\n")
                f.write("\n")
            
            f.write(f"\nDetailed results: [JSON](test_{timestamp}.json) | [Text](test_{timestamp}.txt)\n")
        
        # Print success messages with full paths
        console.print("\n[green]Case Information:[/green]")
        abs_case_dir = os.path.abspath(case_dir)
        abs_case_file = os.path.abspath(case_file)
        abs_results_base = os.path.abspath(results_base)
        
        console.print(f"[green]Case folder:[/green] {abs_case_dir}")
        console.print(f"[green]Case file:[/green] {abs_case_file}")
        console.print(f"\n[green]Test Results:[/green]")
        console.print(f"- JSON: {abs_results_base}.json")
        console.print(f"- Text: {abs_results_base}.txt")
        
        return case_dir
        
    except Exception as e:
        console.print(f"\n[red]Error creating case:[/red] {str(e)}")
        return None

def run_tests(image_url: str, api_key: Optional[str], test_type: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """Run the specified tests and display results."""
    results = {}
    with Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]{task.description}[/bold blue]"),
        BarColumn(),
        TimeRemainingColumn()
    ) as progress:
        try:
            # Run tests and collect results
            test_results = {}
            
            # Basic tests
            task = progress.add_task("Running basic image tests...", total=100)
            test_results["Basic Tests"] = diagnostics.run_basic_tests(image_url)
            progress.update(task, completed=100)
            
            # Additional tests based on type
            if test_type != "Basic Image Test":
                task = progress.add_task(f"Running {test_type}...", total=100)
                test_results[test_type] = diagnostics.run_generation_test(
                    image_url, 
                    api_key, 
                    test_type,
                    params
                )
                progress.update(task, completed=100)
            
            # Display results using our enhanced formatter
            console.print("\n[bold green]Test Results:[/bold green]")
            from . import messages
            messages.format_test_results(test_results)
            
            # Offer to create a case
            case_dir = create_case(image_url, api_key, test_type, params, test_results)
            
            # Ask if user wants to run another test
            if questionary.confirm("\nWould you like to run another test?").ask():
                main()
            else:
                console.print("\n[bold blue]Thanks for using LUMA Diagnostics![/bold blue]")
                if case_dir:
                    abs_case_dir = os.path.abspath(case_dir)
                    console.print(f"\n[green]Your case and test results are in:[/green] {abs_case_dir}")
                    console.print("You can view the case file and test results there.")
                
        except Exception as e:
            console.print(f"\n[bold red]Error running tests:[/bold red] {str(e)}")
            return 1
    
    return 0

def run_demo_wizard():
    """Run a demo version of the wizard without requiring an API key."""
    print_welcome()
    
    console.print(Panel(
        "[bold yellow]⚠ Demo Mode Active[/bold yellow]\n"
        "This is a demonstration of the LUMA Diagnostics wizard.\n"
        "No actual API calls will be made and all results are simulated.",
        title="LUMA Diagnostics Wizard",
        border_style="yellow",
        box=box.ROUNDED
    ))
    
    # Ask about what the user is trying to do
    what_to_do = questionary.select(
        "What would you like to do?",
        choices=[
            "Test an image I already have",
            "Test the LUMA API connection",
            "Exit demo"
        ]
    ).ask()
    
    if what_to_do == "Exit demo":
        console.print("[yellow]Exiting demo wizard.[/yellow]")
        return
    
    if what_to_do == "Test an image I already have":
        # Ask for an image path
        image_path = questionary.text(
            "Enter the path to your image file:",
            default="(Skip to use a mock image)"
        ).ask()
        
        if not image_path or image_path == "(Skip to use a mock image)":
            console.print("[yellow]Using mock image data for demonstration.[/yellow]")
            image_path = None
        else:
            # Validate image
            if not os.path.exists(image_path):
                console.print(f"[red]File not found: {image_path}[/red]")
                console.print("[yellow]Using mock image data for demonstration.[/yellow]")
                image_path = None
    else:
        image_path = None
    
    # Show "running tests" animation
    console.print("[bold]Running diagnostic tests...[/bold]")
    with console.status("[bold green]Running tests...[/bold green]", spinner="dots"):
        # Simulate API delay
        time.sleep(2)
        
    # Run mock tests
    mock_tests.run_mock_tests(image_path)
    
    # Ask if user wants to create a case
    create_case = questionary.confirm(
        "Would you like to create a support case with these results?",
        default=False
    ).ask()
    
    if create_case:
        console.print(Panel(
            "[yellow]In a real session, this would create a support case with LUMA.[/yellow]\n"
            "You could then share this case with LUMA support for assistance.",
            title="Demo: Create Support Case",
            border_style="yellow",
            box=box.ROUNDED
        ))
    
    # Final message
    console.print("\n[bold green]Demo wizard complete![/bold green]")
    console.print("This demonstration shows how the LUMA Diagnostics tool works.")
    console.print("To use the real version, you'll need a LUMA API key.\n")

def main():
    """Main entry point for the wizard."""
    try:
        print_welcome()
        
        # Check if we are in a TTY - needed for questionary
        if not sys.stdin.isatty():
            console.print("[yellow]Interactive wizard requires a terminal. Try using --test or --image instead.[/yellow]")
            return
        
        # Check if we're in a continuous integration environment
        if os.environ.get("CI") or os.environ.get("CONTINUOUS_INTEGRATION"):
            console.print("[yellow]CI environment detected. Running in demo mode...[/yellow]")
            run_demo_wizard()
            return
        
        # Get image URL
        image_url = get_image_url()
        if image_url is None:  # User cancelled
            console.print("\n[bold blue]Thanks for using LUMA Diagnostics![/bold blue]")
            return
        
        # Get API key
        api_key = get_api_key()
        if api_key == "CANCELLED":  # User cancelled
            console.print("\n[bold blue]Thanks for using LUMA Diagnostics![/bold blue]")
            return
        
        # Get test type
        test_type = get_test_type(api_key)
        if test_type is None:  # User cancelled
            console.print("\n[bold blue]Thanks for using LUMA Diagnostics![/bold blue]")
            return
        
        # Get additional parameters if needed
        params = {}
        if test_type not in ["Basic Image Test", "Full Test Suite"]:
            params = get_generation_params(test_type)
            if params is None:  # User cancelled
                console.print("\n[bold blue]Thanks for using LUMA Diagnostics![/bold blue]")
                return
        
        # Run tests
        run_tests(image_url, api_key, test_type, params)
    
    except KeyboardInterrupt:
        console.print("\n[bold blue]Thanks for using LUMA Diagnostics![/bold blue]")
    except Exception as e:
        console.print(f"\n[bold red]Error:[/bold red] {str(e)}")
        if questionary.confirm("Would you like to try again?").ask():
            main()
        else:
            console.print("\n[bold blue]Thanks for using LUMA Diagnostics![/bold blue]")

if __name__ == "__main__":
    try:
        run_wizard()
    except KeyboardInterrupt:
        console.print("\n[bold blue]Thanks for using LUMA Diagnostics![/bold blue]")
        sys.exit(0)
