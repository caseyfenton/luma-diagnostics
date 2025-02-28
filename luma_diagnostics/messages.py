"""User-friendly messages and formatting for LUMA diagnostics."""

from typing import Dict, Any
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box
import json

console = Console()

def print_test_header(test_name: str) -> None:
    """Print a nicely formatted test header."""
    console.print(f"\n[bold blue]Running {test_name}...[/bold blue]")

def print_success(message: str) -> None:
    """Print a success message."""
    console.print(f"[bold green]✓[/bold green] {message}")

def print_warning(message: str) -> None:
    """Print a warning message."""
    console.print(f"[bold yellow]![/bold yellow] {message}")

def print_error(message: str) -> None:
    """Print an error message."""
    console.print(f"[bold red]✗[/bold red] {message}")

def print_info(message: str) -> None:
    """Print an info message."""
    console.print(f"[bold cyan]ℹ[/bold cyan] {message}")

def format_test_results(results: Dict[str, Any]) -> None:
    """Format and display test results in a user-friendly way."""
    # Check if results is a string (JSON)
    if isinstance(results, str):
        try:
            results = json.loads(results)
        except:
            # Not valid JSON, just show as is
            print_info("Test Result:")
            console.print(results)
            return
    
    # If it's a simple result, display it in a user-friendly way
    if isinstance(results, dict) and "status" in results:
        _format_single_result("API Test", results)
        return
    
    # Get the image URL from the first test that has it
    image_url = None
    for test_name, test_data in results.items():
        if isinstance(test_data, dict) and "details" in test_data:
            details = test_data["details"]
            if isinstance(details, dict) and "url" in details:
                image_url = details["url"]
                break
    
    # Display a summary banner for the test session
    if image_url:
        console.print(Panel(
            f"[bold]Testing Image:[/bold] {image_url}",
            title="Test Session",
            border_style="blue",
            box=box.ROUNDED
        ))
    
    # Process and display each test group
    for test_group, tests_data in results.items():
        console.print(f"\n[bold cyan]{test_group}[/bold cyan]")
        
        # For each test in this group
        for test_name, test_data in tests_data.items():
            # Skip if not a proper test data structure
            if not isinstance(test_data, dict) or "status" not in test_data:
                console.print(f"  [dim]{test_name}:[/dim] {test_data}")
                continue
            
            # Get test details
            status = test_data.get("status", "unknown")
            details = test_data.get("details", {})
            
            # Determine the test description and help text
            test_info = _get_test_description(test_name)
            
            # Create the test status indicator
            status_info = {
                "completed": ("✓", "green", "Passed"),
                "passed": ("✓", "green", "Passed"),
                "success": ("✓", "green", "Passed"),
                "warning": ("⚠", "yellow", "Warning"),
                "error": ("✗", "red", "Failed"),
                "failed": ("✗", "red", "Failed"),
                "unknown": ("?", "blue", "Unknown")
            }.get(status.lower(), ("?", "blue", "Unknown"))
            
            # Build panel title
            title = f"[{status_info[1]}]{status_info[0]} Test {test_info['number']}: {test_name} - {status_info[2]}[/{status_info[1]}]"
            
            # Build panel content
            content = []
            content.append(f"[bold]What this test checks:[/bold] {test_info['description']}")
            
            # Add specific result details
            if status.lower() in ["completed", "success", "passed"]:
                content.append(f"\n[green]✓ {test_info['success_message']}[/green]")
            elif status.lower() in ["error", "failed"]:
                content.append(f"\n[red]✗ {test_info['failure_message']}[/red]")
                
                # Add troubleshooting advice
                if "error" in details:
                    content.append(f"\n[bold]Error:[/bold] {details['error']}")
                    
                content.append(f"\n[bold]Troubleshooting:[/bold] {test_info['troubleshooting']}")
            
            # Add important details but skip the URL since we show it once at the top
            for key, value in details.items():
                if key == "url" or key == "info" and not value:
                    continue
                
                # Format the key name to be more user-friendly
                friendly_key = key.replace("_", " ").title()
                
                # Format the value based on its type
                if isinstance(value, bool):
                    value_text = "[green]Yes[/green]" if value else "[red]No[/red]"
                elif isinstance(value, dict):
                    value_text = f"Contains {len(value)} properties"
                elif isinstance(value, list):
                    value_text = f"{len(value)} items"
                else:
                    value_text = str(value)
                
                content.append(f"[bold]{friendly_key}:[/bold] {value_text}")
            
            # Create and display the panel
            console.print(Panel(
                "\n".join(content),
                title=title,
                border_style=status_info[1],
                box=box.ROUNDED,
                expand=False
            ))

def _get_test_description(test_name: str) -> Dict[str, str]:
    """Get description and help text for a specific test."""
    test_descriptions = {
        "Public Access": {
            "number": "1",
            "description": "Verifies that the image URL is publicly accessible and DNS is resolving correctly.",
            "success_message": "The image is publicly accessible and can be reached by Luma servers.",
            "failure_message": "The image cannot be accessed. This may be due to DNS issues or server restrictions.",
            "troubleshooting": "Check that the URL is correct and the hosting server is publicly accessible. Make sure there are no IP restrictions."
        },
        "Certificate": {
            "number": "2",
            "description": "Checks that the SSL/TLS certificate for the hosting server is valid.",
            "success_message": "The SSL certificate is valid and trusted.",
            "failure_message": "There's an issue with the SSL certificate on the hosting server.",
            "troubleshooting": "The host server needs to fix their SSL certificate. This isn't an issue with your image but with where it's hosted."
        },
        "Redirects": {
            "number": "3",
            "description": "Checks if the image URL redirects to another location.",
            "success_message": "No problematic redirects detected.",
            "failure_message": "The URL is redirecting, which might cause issues with some LUMA API requests.",
            "troubleshooting": "Try using the final URL directly instead of one that redirects."
        },
        "Headers": {
            "number": "4", 
            "description": "Examines the HTTP headers returned by the server to verify content type and size.",
            "success_message": "The image headers are correctly formatted.",
            "failure_message": "There's an issue with the HTTP headers for this image.",
            "troubleshooting": "Verify that the server is correctly identifying the file as an image with the proper content type."
        },
        "Validity": {
            "number": "5",
            "description": "Validates that the file is a properly formatted image in a supported format.",
            "success_message": "The file is a valid image in a supported format.",
            "failure_message": "The file doesn't appear to be a valid image or is in an unsupported format.",
            "troubleshooting": "Try converting your image to JPEG, PNG, or another standard format."
        }
    }
    
    # Default values for unknown tests
    default = {
        "number": "?",
        "description": "Performs diagnostic checks on your image.",
        "success_message": "This test passed successfully.",
        "failure_message": "This test encountered an issue.",
        "troubleshooting": "Verify your image meets LUMA's requirements and try again."
    }
    
    return test_descriptions.get(test_name, default)

def _format_single_result(test_name: str, result: Dict[str, Any]) -> None:
    """Format a single test result in a user-friendly panel."""
    status = result.get("status", "unknown")
    error = result.get("error", "")
    details = result.get("details", {})
    
    # Set panel style based on status
    status_info = {
        "success": ("✓ Test Passed", "green"),
        "warning": ("⚠ Warning", "yellow"),
        "error": ("✗ Test Failed", "red"),
        "unknown": ("? Unknown Status", "blue")
    }.get(status.lower(), ("? Unknown Status", "blue"))
    
    # Create panel title
    title = f"[bold {status_info[1]}]{status_info[0]}: {test_name}[/bold {status_info[1]}]"
    
    # Format details for display
    content_lines = []
    
    if error:
        error_type = "unknown"
        if isinstance(error, dict) and "type" in error:
            error_type = error["type"]
        elif isinstance(error, str) and ":" in error:
            error_type = error.split(":", 1)[0].lower()
            
        friendly_msg = get_error_message(error_type, details)
        content_lines.append(f"[bold red]Problem:[/bold red] {friendly_msg}")
    
    # Add details in user-friendly format
    if details:
        content_lines.append("\n[bold]Test Details:[/bold]")
        for k, v in details.items():
            # Make keys more friendly
            friendly_key = k.replace("_", " ").title()
            
            # Format the value to be more readable
            if isinstance(v, dict):
                # Summarize dictionaries
                content_lines.append(f"  • {friendly_key}: " + 
                                    f"{len(v)} properties")
            elif isinstance(v, (list, tuple)):
                # Summarize lists
                content_lines.append(f"  • {friendly_key}: " +
                                    f"{len(v)} items")
            else:
                # Display simple values
                content_lines.append(f"  • {friendly_key}: {v}")
    
    # Create and print the panel
    panel = Panel(
        "\n".join(content_lines) if content_lines else "No details available",
        title=title,
        border_style=status_info[1],
        box=box.ROUNDED
    )
    console.print(panel)

def get_error_message(error_type: str, details: Dict[str, Any] = None) -> str:
    """Get a user-friendly error message with troubleshooting steps."""
    messages = {
        "connectionerror": "Could not connect to the server. Check your internet connection and the URL.",
        "sslerror": "SSL certificate validation failed. The server's security certificate is not trusted.",
        "timeout": "The request timed out. The server is taking too long to respond.",
        "httperror": "The server returned an error status code.",
        "jsondecodeerror": "Could not parse the response as valid JSON. The server returned invalid data.",
        "auth": "Authentication failed. Check your API key and permissions."
    }
    
    # Get specific HTTP status code message if present
    if details and "status_code" in details:
        code = details["status_code"]
        if code == 401:
            return "Authentication required. Check your API key."
        elif code == 403:
            return "Access forbidden. You don't have permission to access this resource."
        elif code == 404:
            return "Resource not found. The URL may be incorrect."
        elif code == 429:
            return "Too many requests. You've hit a rate limit on the API."
        elif code >= 500:
            return "Server error. The LUMA API server encountered an error processing your request."
    
    return messages.get(error_type.lower(), f"An error occurred: {error_type}")

def print_welcome() -> None:
    """Print a welcoming message when starting the diagnostics tool."""
    welcome_text = (
        "Welcome to LUMA Diagnostics!\n\n"
        "This tool will help you test your images with LUMA's Dream Machine API.\n"
        "We'll guide you through the process step by step."
    )
    console.print(Panel(welcome_text, title="LUMA Diagnostics Wizard", border_style="blue", box=box.ROUNDED))
