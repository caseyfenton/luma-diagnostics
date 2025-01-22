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
        console=console,
        transient=True
    ) as progress:
        task = progress.add_task(description="Initializing...", total=None)
        
        try:
            # Define test sequence
            test_sequence = [
                ("Public Access", lambda: diagnostics.tests.test_public_access(image_url)),
                ("Certificate Validation", lambda: diagnostics.tests.test_cert_validation(image_url)),
                ("Redirect Check", lambda: diagnostics.tests.test_redirect(image_url)),
                ("Headers and Content", lambda: diagnostics.test_image_headers(image_url, timeout=30)),
                ("Image Validity", lambda: diagnostics.test_image_validity(image_url, timeout=30))
            ]
            
            results = []
            
            # Run each test with progress updates
            for test_name, test_func in test_sequence:
                # Clear previous progress
                progress.update(task, description=f"Running {test_name} test...")
                
                try:
                    result = test_func()
                    results.append(result)
                    
                    # Show immediate feedback and clear progress
                    progress.stop()
                    if result["status"] == "failed":
                        console.print(f"\n[red]✗ {test_name} failed: {result['details'].get('error', 'Unknown error')}[/red]")
                        
                        # Handle timeout specifically
                        if "timeout" in str(result.get("details", {}).get("error", "")).lower():
                            if questionary.confirm("Would you like to retry this test with a longer timeout?").ask():
                                progress.start()
                                progress.update(task, description=f"Retrying {test_name} with longer timeout...")
                                
                                # Retry with longer timeout
                                if test_name in ["Headers and Content", "Image Validity"]:
                                    result = test_func()
                                    # Replace the failed result with the retry result
                                    results[-1] = result
                                    progress.stop()
                                    
                                    if result["status"] == "completed":
                                        console.print(f"[green]✓ {test_name} completed successfully on retry[/green]")
                                    else:
                                        console.print(f"[red]✗ {test_name} failed again: {result['details'].get('error', 'Unknown error')}[/red]")
                    else:
                        console.print(f"[green]✓ {test_name} completed successfully[/green]")
                        
                        # Show test details immediately
                        if "details" in result:
                            for k, v in result["details"].items():
                                if isinstance(v, dict):
                                    console.print(f"  {k}:")
                                    for sub_k, sub_v in v.items():
                                        console.print(f"    {sub_k}: {sub_v}")
                                else:
                                    console.print(f"  {k}: {v}")
                
                except Exception as e:
                    progress.stop()
                    console.print(f"\n[red]✗ Error in {test_name}: {str(e)}[/red]")
                    results.append({
                        "test_name": test_name,
                        "status": "failed",
                        "details": {"error": str(e)}
                    })
                
                # Add a newline between tests
                console.print()
                
                # Small pause between tests for readability
                time.sleep(0.5)
                progress.start()
            
            progress.stop()
            console.print("\n[bold green]All tests completed![/bold green]")
            
            # Show final results
            clear_screen()
            console.print("\n[bold]Summary of results:[/bold]")
            console.print("=" * 40)
            
            for result in results:
                console.print(f"\n[bold]{result['test_name']}[/bold]")
                console.print("-" * 40)
                
                if result["status"] == "completed":
                    console.print("[green]✓ Passed[/green]")
                    if "details" in result:
                        for k, v in result["details"].items():
                            if isinstance(v, dict):
                                console.print(f"{k}:")
                                for sub_k, sub_v in v.items():
                                    console.print(f"  {sub_k}: {sub_v}")
                            else:
                                console.print(f"{k}: {v}")
                else:
                    console.print(f"[red]✗ Failed[/red]")
                    if "details" in result and "error" in result["details"]:
                        error_msg = str(result["details"]["error"])
                        console.print(f"[red]Error: {error_msg}[/red]")
                        
                        # Show suggestions based on error type
                        if "timeout" in error_msg.lower():
                            console.print("\n[yellow]Suggestion: The server might be slow. Try:[/yellow]")
                            console.print("1. Check your internet connection")
                            console.print("2. Try a different image URL")
                            console.print("3. Run the test again with a longer timeout")
                        elif "certificate" in error_msg.lower():
                            console.print("\n[yellow]Suggestion: SSL/Certificate issue. Try:[/yellow]")
                            console.print("1. Use an HTTPS URL")
                            console.print("2. Check if the website's SSL certificate is valid")
                        elif "dns" in error_msg.lower():
                            console.print("\n[yellow]Suggestion: DNS resolution failed. Try:[/yellow]")
                            console.print("1. Check if the URL is correct")
                            console.print("2. Check if the website is accessible")
                        elif "connection" in error_msg.lower():
                            console.print("\n[yellow]Suggestion: Connection failed. Try:[/yellow]")
                            console.print("1. Check your internet connection")
                            console.print("2. Check if the website is accessible")
                            console.print("3. Try a different image URL")
            
            # Ask if they want to run another test
            if questionary.confirm("\nWould you like to run another test?").ask():
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
