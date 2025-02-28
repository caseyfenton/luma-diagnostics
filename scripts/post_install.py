#!/usr/bin/env python3
"""Post-installation script for LUMA Diagnostics."""

import subprocess
import sys

def main():
    # This script is run by setuptools after installation
    print("\n=== LUMA Diagnostics Installation Complete ===")
    print("\nTo get started, run one of the following commands:")
    print("  luma-diagnostics --wizard         # Start the interactive wizard")
    print("  luma-diagnostics --help           # Show all available options")
    print("\nVisit https://github.com/caseyfenton/luma-diagnostics for documentation\n")
    
    # Try to run the more beautiful version if rich is available
    try:
        subprocess.run(
            [sys.executable, "-c", "from luma_diagnostics.post_install import post_install_message; post_install_message()"],
            check=False
        )
    except Exception:
        # If that fails, the simple text version above will have been shown instead
        pass

if __name__ == "__main__":
    main()
