#!/usr/bin/env python3

import sys
import argparse
from luma_diagnostics import cli, wizard

def main():
    parser = argparse.ArgumentParser(description="LUMA API Diagnostics Tool")
    parser.add_argument("--wizard", action="store_true", help="Run in interactive wizard mode")
    args = parser.parse_args()

    if args.wizard:
        wizard.main()
    else:
        cli.main()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nDiagnostics cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {str(e)}")
        sys.exit(1)
