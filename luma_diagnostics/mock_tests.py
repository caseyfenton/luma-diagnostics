"""
LUMA Diagnostics Mock Tests
This module provides mock test functionality for demo/testing purposes.
"""

from typing import Dict, Any, List, Optional
from rich.console import Console
from rich.panel import Panel
from rich import box

from luma_diagnostics import messages
from luma_diagnostics.file_utils import get_file_info

console = Console()

def run_mock_tests(image_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Run simulated diagnostic tests that don't require API keys.
    This is useful for demonstrations and for testing the UI.
    
    Args:
        image_path: Optional path to an image file to use in the mock tests
        
    Returns:
        Dict containing mock test results
    """
    console.print(Panel(
        "[bold yellow]⚠ Demonstration Mode[/bold yellow]\n"
        "Running in demo mode with simulated test results.\n"
        "No API calls will be made and no diagnostics will be performed.",
        title="LUMA Diagnostics",
        border_style="yellow",
        box=box.ROUNDED
    ))
    
    mock_results = {"Image Tests": {}}
    
    # If we have an actual image file, get its info
    image_info = {}
    if image_path:
        try:
            image_info = get_file_info(image_path)
            console.print(f"[bold]Using image:[/bold] {image_path}")
        except Exception as e:
            console.print(f"[yellow]Note: Unable to read the provided image: {str(e)}[/yellow]")
    
    # Create mock test results
    mock_results["Image Tests"] = {
        "Public Access": {
            "status": "success",
            "message": "The image is publicly accessible and can be reached by Luma servers.",
            "details": {"response_time_ms": 120, "content_length": image_info.get("size_bytes", 54321)}
        },
        "Certificate": {
            "status": "success",
            "message": "SSL certificate is valid and trusted.",
            "details": {"issuer": "Let's Encrypt", "expiry": "2025-12-31"}
        },
        "Redirects": {
            "status": "warning",
            "message": "URL redirects to another location. This may cause issues with some API endpoints.",
            "details": {"original_url": "http://example.com/image.jpg", "final_url": "https://cdn.example.com/image.jpg"}
        },
        "Headers": {
            "status": "success",
            "message": "All required HTTP headers are present.",
            "details": {"content_type": image_info.get("mime_type", "image/jpeg"), 
                       "content_length": str(image_info.get("size_bytes", 54321))}
        },
        "Validity": {
            "status": "success",
            "message": "The file is a valid image in a supported format.",
            "details": {
                "format": image_info.get("format", "JPEG").upper(),
                "dimensions": f"{image_info.get('width', 1024)}x{image_info.get('height', 768)}",
                "size_kb": image_info.get("size_kb", 450)
            }
        }
    }
    
    # For more interesting demos, we can randomize some results or
    # add errors based on the image_info (if provided)
    
    # Display the results
    display_mock_results(mock_results)
    
    return mock_results

def display_mock_results(results: Dict[str, Any]) -> None:
    """
    Display mock test results in a user-friendly way.
    
    Args:
        results: Dict containing test results
    """
    for test_group, tests in results.items():
        console.print(f"\n[bold cyan]{test_group}[/bold cyan]")
        
        for test_name, test_data in tests.items():
            # Get test description info
            test_info = messages._get_test_description(test_name)
            
            # Style based on status
            status = test_data.get("status")
            status_info = {
                "success": ("✓", "green", "Passed"),
                "warning": ("⚠", "yellow", "Warning"),
                "error": ("✗", "red", "Failed"),
            }.get(status, ("?", "blue", "Unknown"))
            
            # Build panel title
            title = f"[{status_info[1]}]{status_info[0]} Test {test_info['number']}: {test_name} - {status_info[2]}[/{status_info[1]}]"
            
            # Build panel content
            content = []
            content.append(f"[bold]What this test checks:[/bold] {test_info['description']}")
            
            # Add the message from the test
            message = test_data.get("message", "")
            if message:
                if status == "success":
                    content.append(f"\n[green]✓ {message}[/green]")
                elif status == "warning":
                    content.append(f"\n[yellow]⚠ {message}[/yellow]")
                elif status == "error":
                    content.append(f"\n[red]✗ {message}[/red]")
            
            # Add details
            details = test_data.get("details", {})
            if details:
                content.append("\n[bold]Details:[/bold]")
                for key, value in details.items():
                    friendly_key = key.replace("_", " ").title()
                    content.append(f"  • {friendly_key}: {value}")
            
            # Create and display the panel
            console.print(Panel(
                "\n".join(content),
                title=title,
                border_style=status_info[1],
                box=box.ROUNDED,
                expand=False
            ))
    
    # Add a note about demo mode
    console.print("\n[yellow]Note: These are simulated test results for demonstration purposes.[/yellow]")
