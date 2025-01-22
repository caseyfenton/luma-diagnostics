"""User-friendly messages and formatting for LUMA diagnostics."""

from typing import Dict, Any
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

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
    """Format and display test results in a table."""
    table = Table(title="Test Results", show_header=True, header_style="bold magenta")
    table.add_column("Test", style="cyan")
    table.add_column("Status", justify="center")
    table.add_column("Details", justify="left")

    for test_name, result in results.items():
        status = result.get("status", "unknown")
        details = result.get("details", {})
        
        # Format status with color
        status_color = {
            "success": "[green]✓ Pass[/green]",
            "warning": "[yellow]⚠ Warning[/yellow]",
            "error": "[red]✗ Failed[/red]",
            "unknown": "[grey]? Unknown[/grey]"
        }.get(status.lower(), status)
        
        # Format details as a list
        details_text = "\n".join(f"- {k}: {v}" for k, v in details.items())
        
        table.add_row(test_name, status_color, details_text)
    
    console.print(table)

def get_error_message(error_type: str, details: Dict[str, Any] = None) -> str:
    """Get a user-friendly error message with troubleshooting steps."""
    messages = {
        "api_key": (
            "API Key Error:\n"
            "• Check if your API key is correctly set in ~/.env\n"
            "• Verify the API key format\n"
            "• Try regenerating a new API key"
        ),
        "rate_limit": (
            "Rate Limit Exceeded:\n"
            "• Wait a few minutes before trying again\n"
            "• Check your current usage in the LUMA dashboard\n"
            "• Consider upgrading your plan if this happens frequently"
        ),
        "network": (
            "Network Error:\n"
            "• Check your internet connection\n"
            "• Verify the API endpoint is accessible\n"
            "• Check if any firewall is blocking the connection"
        ),
        "timeout": (
            "Request Timeout:\n"
            "• The server took too long to respond\n"
            "• Try again with a longer timeout setting\n"
            "• Check if the image size is too large"
        ),
        "image": (
            "Image Error:\n"
            "• Verify the image URL is accessible\n"
            "• Check if the image format is supported (JPG, PNG)\n"
            "• Ensure the image size is within limits"
        )
    }
    
    base_message = messages.get(error_type, "An unknown error occurred")
    if details:
        detail_text = "\nDetails:\n" + "\n".join(f"• {k}: {v}" for k, v in details.items())
        return base_message + detail_text
    return base_message

def print_welcome() -> None:
    """Print a welcoming message when starting the diagnostics tool."""
    welcome_text = (
        "Welcome to LUMA Diagnostics!\n\n"
        "This tool will help you test your images with LUMA's Dream Machine API.\n"
        "We'll guide you through the process step by step."
    )
    console.print(Panel(welcome_text, title="LUMA Diagnostics Wizard", border_style="blue"))
