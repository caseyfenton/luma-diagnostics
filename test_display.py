#!/usr/bin/env python3
"""
Demonstration script for LUMA Diagnostics test result display.
This doesn't require API keys or interactive prompts.
"""

from luma_diagnostics.api_tests import LumaAPITester
from luma_diagnostics import messages
from rich.console import Console
from rich import box
from rich.panel import Panel

console = Console()

def main():
    """Run a mock test and display the enhanced test results."""
    console.print("\n[bold]LUMA Diagnostics Test Results Demo[/bold]\n")
    
    # Create a tester with a dummy API key
    tester = LumaAPITester("dummy_api_key")
    
    # Run the mock test
    mock_result = tester.mock_test()
    
    # Show banner for the demo
    console.print(Panel(
        "[bold]Demonstration Mode[/bold]\nThe following results simulate a real diagnostic test run.",
        title="LUMA Diagnostics",
        border_style="blue",
        box=box.ROUNDED
    ))
    
    # Use our format function to display individual test results from mock data
    console.print("\n[bold cyan]Image Diagnostic Tests[/bold cyan]")
    for test_name, test_data in mock_result["details"].items():
        # Format all keys as in our test data description dictionary
        if test_name == "SSL Certificate":
            test_name = "Certificate"
        elif test_name == "URL Redirect":
            test_name = "Redirects" 
        elif test_name == "HTTP Headers":
            test_name = "Headers"
        elif test_name == "Image Validity":
            test_name = "Validity"
            
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
    
    console.print("\n[bold]This is a demonstration of the enhanced test results display.[/bold]")
    console.print("In a real run, these results would come from actual API tests.")

if __name__ == "__main__":
    main()
