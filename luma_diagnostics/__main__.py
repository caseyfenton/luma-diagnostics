#!/usr/bin/env python3

"""Main entry point for LUMA Diagnostics CLI."""

import sys
import argparse
from luma_diagnostics import cli

if __name__ == "__main__":
    try:
        cli.main()
    except KeyboardInterrupt:
        print("\nDiagnostics cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {str(e)}")
        sys.exit(1)
