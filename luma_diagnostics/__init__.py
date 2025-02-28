"""LUMA Labs API Diagnostics Tool."""

__version__ = "1.0.1"

# Check if this is being run via pip install or direct import
import sys
import os

def _show_welcome_message():
    try:
        # Only show message when imported directly, not when imported by pip during installation
        if 'pip' not in sys.modules and not os.environ.get('LUMA_DIAGNOSTICS_NO_WELCOME'):
            # Don't show welcome when running tests
            if 'pytest' not in sys.modules and 'unittest' not in sys.modules:
                # Only show when imported directly, not when imported by another module
                if __name__ == 'luma_diagnostics':
                    # Import here to avoid errors if rich isn't installed yet
                    from .post_install import post_install_message
                    post_install_message()
    except Exception:
        # Fail silently - we don't want to break imports if the welcome message fails
        pass

# Run on first import
_show_welcome_message()
