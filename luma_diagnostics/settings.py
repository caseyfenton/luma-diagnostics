"""Settings management for LUMA Diagnostics."""

import os
import json
from pathlib import Path
from typing import Optional, Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv(os.path.expanduser("~/.env"))

class Settings:
    """Manages persistent settings and defaults."""
    
    DEFAULT_TEST_IMAGE = "https://files.readme.io/35fc85755a99eba889ebd196ed5891b11e52813393249c334c377b6c30e8f2f3-teddy.jpg"
    SETTINGS_DIR = os.path.expanduser("~/.config/luma-diagnostics")
    SETTINGS_FILE = os.path.join(SETTINGS_DIR, "settings.json")
    
    def __init__(self):
        """Initialize settings manager."""
        self._settings = {}
        self._session = {}  # For temporary session storage
        self._ensure_settings_dir()
        self._load_settings()
    
    def _ensure_settings_dir(self):
        """Ensure settings directory exists."""
        os.makedirs(self.SETTINGS_DIR, exist_ok=True)
    
    def _load_settings(self):
        """Load settings from file."""
        try:
            if os.path.exists(self.SETTINGS_FILE):
                with open(self.SETTINGS_FILE, 'r') as f:
                    self._settings = json.load(f)
        except Exception:
            self._settings = {}
    
    def _save_settings(self):
        """Save settings to file."""
        try:
            with open(self.SETTINGS_FILE, 'w') as f:
                json.dump(self._settings, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save settings: {e}")
    
    def get_api_key(self) -> Optional[str]:
        """Get API key from various sources."""
        # Try environment variable first
        api_key = os.getenv("LUMA_API_KEY")
        if api_key:
            return api_key
        
        # Try saved settings
        return self._settings.get("api_key")
    
    def set_api_key(self, api_key: str):
        """Save API key to settings."""
        self._settings["api_key"] = api_key
        self._save_settings()
    
    def save_api_key_to_env(self, api_key: str) -> bool:
        """Save API key to user's ~/.env file."""
        try:
            env_file = os.path.expanduser("~/.env")
            key_line = f"LUMA_API_KEY={api_key}"
            
            # Read existing content if file exists
            existing_lines = []
            key_exists = False
            if os.path.exists(env_file):
                with open(env_file, "r") as f:
                    for line in f:
                        if line.strip().startswith("LUMA_API_KEY="):
                            existing_lines.append(key_line)
                            key_exists = True
                        else:
                            existing_lines.append(line.rstrip())
            
            # Add key if it doesn't exist
            if not key_exists:
                existing_lines.append(key_line)
            
            # Write back to file
            with open(env_file, "w") as f:
                f.write("\n".join(existing_lines))
                if existing_lines:
                    f.write("\n")
            
            return True
            
        except Exception as e:
            print(f"[red]Error saving API key to ~/.env:[/red] {str(e)}")
            return False
    
    def get_last_image_url(self) -> Optional[str]:
        """Get last used image URL from session."""
        return self._session.get("last_image_url")
    
    def set_last_image_url(self, url: str):
        """Save last used image URL to session."""
        self._session["last_image_url"] = url
    
    def get_last_test_type(self) -> Optional[str]:
        """Get last used test type from session."""
        return self._session.get("last_test_type", "Basic Image Test")
    
    def set_last_test_type(self, test_type: str):
        """Save last used test type to session."""
        self._session["last_test_type"] = test_type
    
    def get_last_params(self) -> Dict[str, Any]:
        """Get last used test parameters from session."""
        return self._session.get("last_params", {})
    
    def set_last_params(self, params: Dict[str, Any]):
        """Save last used test parameters to session."""
        self._session["last_params"] = params
    
    def clear_session(self):
        """Clear all session data."""
        self._session = {}
    
    def clear(self):
        """Clear all settings."""
        self._settings = {}
        self._save_settings()
