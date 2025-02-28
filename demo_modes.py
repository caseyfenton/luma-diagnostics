#!/usr/bin/env python3
"""
LUMA Diagnostics Demo Script

This script runs various demo modes of the LUMA Diagnostics tool.
It's designed to showcase the functionality without requiring API keys.
"""

import os
import sys
import time
from rich.console import Console
from rich.panel import Panel
from rich import box
import subprocess

console = Console()

def title(text):
    """Display a title banner"""
    console.print(f"\n[bold cyan]{'=' * 20} {text} {'=' * 20}[/bold cyan]\n")

def run_demo(command, description):
    """Run a demo command with description"""
    title(description)
    console.print(f"[dim]Running command:[/dim] [bold yellow]{command}[/bold yellow]\n")
    
    # Give user time to read
    time.sleep(1)
    
    # Display panel
    console.print(Panel(
        f"This will execute: [bold]{command}[/bold]\n\n"
        f"Purpose: {description}",
        title="DEMO COMMAND",
        border_style="blue",
        box=box.ROUNDED
    ))
    
    # Prompt user
    console.print("\n[bold]Press Enter to execute, or Ctrl+C to skip...[/bold]")
    try:
        input()
    except KeyboardInterrupt:
        console.print("\n[yellow]Skipped[/yellow]")
        return
    
    # Execute the command
    try:
        # Run the command and stream output to console
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        
        # Stream output to console
        for line in process.stdout:
            console.print(line, end="")
        
        # Wait for process to complete
        process.wait()
        
        # Show completion message
        console.print("\n[bold green]Command completed[/bold green]")
    except Exception as e:
        console.print(f"\n[bold red]Error: {str(e)}[/bold red]")
    
    # Pause between demos
    console.print("\n[bold]Press Enter for next demo...[/bold]")
    try:
        input()
    except KeyboardInterrupt:
        return

def main():
    """Run the demo script"""
    # Display welcome message
    console.print(Panel(
        "[bold]LUMA Diagnostics Demo Script[/bold]\n\n"
        "This script will guide you through various demo modes of the LUMA Diagnostics tool.\n"
        "You'll see how the tool works without needing an actual LUMA API key.",
        title="Welcome",
        border_style="green",
        box=box.ROUNDED
    ))
    
    console.print("\n[bold]Press Enter to start the demos, or Ctrl+C to exit...[/bold]")
    try:
        input()
    except KeyboardInterrupt:
        console.print("\n[yellow]Exiting[/yellow]")
        return
    
    # Demo 1: Basic Demo Mode
    run_demo(
        "python -m luma_diagnostics.cli --demo",
        "Basic Demo Mode"
    )
    
    # Demo 2: Demo with Image
    run_demo(
        "python -m luma_diagnostics.cli --demo --image /tmp/test.jpg",
        "Demo Mode with Image Path"
    )
    
    # Demo 3: Interactive Wizard Demo
    run_demo(
        "python -m luma_diagnostics.cli --demo --wizard",
        "Interactive Wizard Demo Mode"
    )
    
    # Completion message
    console.print(Panel(
        "[bold green]All demos completed![/bold green]\n\n"
        "You've now seen the various demo modes available in LUMA Diagnostics v1.0.1.\n"
        "These modes allow users to explore the tool's functionality without requiring API keys.",
        title="Demo Complete",
        border_style="green",
        box=box.ROUNDED
    ))

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[yellow]Demo script interrupted[/yellow]")
        sys.exit(0)
