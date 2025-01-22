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
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import print as rprint
from . import diagnostics
from . import utils

console = Console()

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

def get_image_url() -> str:
    """Get the image URL from the user."""
    questions = [
        {
            "type": "text",
            "name": "image_url",
            "message": "What's the URL of the image you want to test?",
            "validate": lambda url: True if url.startswith(('http://', 'https://')) else "Please enter a valid HTTP(S) URL"
        }
    ]
    answers = questionary.prompt(questions)
    return answers["image_url"]

def get_api_key() -> Optional[str]:
    """Get the API key from the user."""
    questions = [
        {
            "type": "confirm",
            "name": "has_key",
            "message": "Do you have a LUMA API key? (Required for generation tests)",
            "default": False
        },
        {
            "type": "password",
            "name": "api_key",
            "message": "Please enter your LUMA API key:",
            "when": lambda x: x["has_key"]
        }
    ]
    answers = questionary.prompt(questions)
    return answers.get("api_key")

def get_test_type(api_key: Optional[str]) -> str:
    """Get the type of test to run."""
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
            "choices": choices
        }
    ]
    answers = questionary.prompt(questions)
    return answers["test_type"]

def get_generation_params(test_type: str) -> Dict[str, Any]:
    """Get generation-specific parameters."""
    params = {}
    
    if test_type == "Text-to-Image Generation":
        questions = [
            {
                "type": "text",
                "name": "prompt",
                "message": "Enter your text prompt:",
                "default": "A serene mountain lake at sunset with reflections in the water"
            },
            {
                "type": "select",
                "name": "aspect_ratio",
                "message": "Choose aspect ratio:",
                "choices": ["16:9", "4:3", "1:1", "9:16"],
                "default": "16:9"
            }
        ]
        params = questionary.prompt(questions)
    
    elif test_type == "Image-to-Image Generation":
        questions = [
            {
                "type": "text",
                "name": "prompt",
                "message": "Enter your modification prompt:",
                "default": "Make it more vibrant and colorful"
            }
        ]
        params = questionary.prompt(questions)
    
    elif test_type == "Image-to-Video Generation":
        questions = [
            {
                "type": "select",
                "name": "camera_motion",
                "message": "Choose camera motion:",
                "choices": [
                    "Static", "Move Left", "Move Right", "Move Up", "Move Down",
                    "Push In", "Pull Out", "Zoom In", "Zoom Out", "Pan Left",
                    "Pan Right", "Orbit Left", "Orbit Right", "Crane Up", "Crane Down"
                ],
                "default": "Orbit Left"
            },
            {
                "type": "text",
                "name": "duration",
                "message": "Enter duration in seconds:",
                "default": "3.0",
                "validate": lambda x: True if x.replace(".", "").isdigit() else "Please enter a valid number"
            }
        ]
        params = questionary.prompt(questions)
        params["duration"] = float(params["duration"])
    
    return params

def run_tests(image_url: str, api_key: Optional[str], test_type: str, params: Dict[str, Any]):
    """Run the selected tests and show progress."""
    case_id = f"wizard_{int(time.time())}"
    config = {
        "TEST_IMAGE_URL": image_url,
        "LUMA_API_KEY": api_key
    }
    
    if test_type != "Basic Image Test":
        config.update(params)
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task(description="Running tests...", total=None)
        
        try:
            results = diagnostics.run_with_config(
                case_id=case_id,
                config_path=None,
                image_url=image_url,
                output_dir=None
            )
            progress.update(task, completed=True)
            
            # Find output files
            output_files = []
            for result in results:
                if result["test_name"] == "Output Files":
                    output_files = result["details"]["output_files"]
                    break
            
            # Show results
            clear_screen()
            console.print("\n[bold green]Tests completed![/bold green]\n")
            
            if output_files:
                console.print("[bold]Results saved to:[/bold]")
                for f in output_files:
                    console.print(f"  {f}")
            
            console.print("\n[bold]Summary of results:[/bold]")
            console.print("=" * 40)
            
            for result in results:
                if result["test_name"] != "Output Files":
                    console.print(f"\n[bold]{result['test_name']}[/bold]")
                    console.print("-" * 40)
                    
                    if result["status"] == "completed":
                        if "details" in result:
                            for k, v in result["details"].items():
                                if isinstance(v, dict):
                                    console.print(f"{k}:")
                                    for sub_k, sub_v in v.items():
                                        console.print(f"  {sub_k}: {sub_v}")
                                else:
                                    console.print(f"{k}: {v}")
                    else:
                        if "details" in result and "error" in result["details"]:
                            console.print(f"[red]Error: {result['details']['error']}[/red]")
                        else:
                            console.print(f"Status: {result['status']}")
            
            # Ask if they want to run another test
            if questionary.confirm("Would you like to run another test?").ask():
                main()
            else:
                console.print("\n[bold blue]Thank you for using LUMA Diagnostics![/bold blue]")
        
        except Exception as e:
            progress.update(task, completed=True)
            console.print(f"\n[bold red]Error:[/bold red] {str(e)}")
            if questionary.confirm("Would you like to try again?").ask():
                main()

def main():
    """Main entry point for the wizard."""
    print_welcome()
    
    # Get image URL
    image_url = get_image_url()
    
    # Get API key
    api_key = get_api_key()
    
    # Get test type
    test_type = get_test_type(api_key)
    
    # Get additional parameters if needed
    params = {}
    if test_type not in ["Basic Image Test", "Full Test Suite"]:
        params = get_generation_params(test_type)
    
    # Run tests
    run_tests(image_url, api_key, test_type, params)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[bold blue]Thanks for using LUMA Diagnostics![/bold blue]")
        sys.exit(0)
