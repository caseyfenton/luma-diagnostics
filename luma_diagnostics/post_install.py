#!/usr/bin/env python3
"""Post-installation script for LUMA Diagnostics."""

import sys
import os
from rich.console import Console
from rich.panel import Panel
from rich import box

def post_install_message():
    """Display a helpful message after package installation."""
    console = Console()
    
    # Make sure we're not running in pip's subprocess
    if 'pip-build' in sys.argv[0] or 'pip/_vendor' in sys.argv[0]:
        return
    
    # Create a stylish welcome panel
    title = "[bold cyan]LUMA Diagnostics[/bold cyan] [green]v1.0.2[/green]"
    
    welcome_text = (
        "\n[bold]Thank you for installing LUMA Diagnostics![/bold]\n\n"
        "This tool helps you troubleshoot image processing issues with LUMA APIs.\n\n"
        "[bold]Quick Start Commands:[/bold]\n\n"
        "[yellow]➤[/yellow] Launch Wizard: [bold]luma-diagnostics --wizard[/bold]\n"
        "[yellow]➤[/yellow] Run Basic Test: [bold]luma-diagnostics --test[/bold]\n"
        "[yellow]➤[/yellow] Test an Image: [bold]luma-diagnostics --image /path/to/image.jpg[/bold]\n"
        "[yellow]➤[/yellow] Create a Case: [bold]luma-diagnostics --create-case \"My Test Case\"[/bold]\n"
        "[yellow]➤[/yellow] Show Help: [bold]luma-diagnostics --help[/bold]"
    )
    
    panel = Panel(
        welcome_text,
        title=title,
        border_style="blue",
        box=box.ROUNDED,
        padding=(1, 2),
        title_align="center"
    )
    
    console.print(panel)

if __name__ == "__main__":
    post_install_message()
