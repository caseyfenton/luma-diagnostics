"""Utility functions for LUMA Diagnostics."""

import os
import sys
import platform
import subprocess
from pathlib import Path

def get_config_dir():
    """Get the appropriate configuration directory for the current platform."""
    if platform.system() == "Windows":
        base_dir = os.environ.get("APPDATA")
        if not base_dir:
            base_dir = os.path.expanduser("~")
        return Path(base_dir) / "LumaDiagnostics"
    else:
        # Linux/Mac
        xdg_config_home = os.environ.get("XDG_CONFIG_HOME")
        if xdg_config_home:
            return Path(xdg_config_home) / "luma-diagnostics"
        return Path.home() / ".config" / "luma-diagnostics"

def get_temp_dir():
    """Get the appropriate temporary directory for the current platform."""
    if platform.system() == "Windows":
        return Path(os.environ.get("TEMP", os.path.expanduser("~\\AppData\\Local\\Temp")))
    else:
        return Path("/tmp")

def run_command(cmd, timeout=30):
    """Run a system command in a cross-platform way."""
    try:
        # On Windows, we need shell=True for some commands
        shell = platform.system() == "Windows"
        
        result = subprocess.run(
            cmd,
            shell=shell,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "Command timed out"
    except Exception as e:
        return -1, "", str(e)

def get_traceroute_command(host):
    """Get the appropriate traceroute command for the current platform."""
    if platform.system() == "Windows":
        return ["tracert", "-d", "-h", "30", host]
    else:
        return ["traceroute", "-n", "-m", "30", host]

def ensure_dir_exists(path):
    """Create directory if it doesn't exist."""
    Path(path).mkdir(parents=True, exist_ok=True)

def get_default_output_dir():
    """Get the default output directory for results."""
    config_dir = get_config_dir()
    return config_dir / "results"

def is_admin():
    """Check if the script is running with administrative privileges."""
    try:
        if platform.system() == "Windows":
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        else:
            return os.geteuid() == 0
    except:
        return False

def get_network_info():
    """Get network interface information in a cross-platform way."""
    if platform.system() == "Windows":
        cmd = ["ipconfig", "/all"]
    else:
        cmd = ["ifconfig" if os.path.exists("/sbin/ifconfig") else "ip", "addr"]
    
    return run_command(cmd)

def get_dns_servers():
    """Get configured DNS servers in a cross-platform way."""
    if platform.system() == "Windows":
        # Parse ipconfig /all output
        code, out, _ = run_command(["ipconfig", "/all"])
        if code == 0:
            dns_servers = []
            for line in out.split("\n"):
                if "DNS Servers" in line:
                    server = line.split(":")[-1].strip()
                    if server:
                        dns_servers.append(server)
            return dns_servers
    else:
        # Try to read /etc/resolv.conf
        try:
            with open("/etc/resolv.conf") as f:
                dns_servers = []
                for line in f:
                    if line.startswith("nameserver"):
                        server = line.split()[1].strip()
                        dns_servers.append(server)
                return dns_servers
        except:
            pass
    
    return []

def sanitize_filename(filename):
    """Create a safe filename that works across platforms."""
    # Replace invalid characters
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    
    # Ensure filename isn't a reserved name on Windows
    if platform.system() == "Windows":
        reserved_names = {
            "CON", "PRN", "AUX", "NUL",
            "COM1", "COM2", "COM3", "COM4",
            "LPT1", "LPT2", "LPT3", "LPT4"
        }
        name_without_ext = filename.split('.')[0].upper()
        if name_without_ext in reserved_names:
            filename = f"_{filename}"
    
    return filename

def get_program_files():
    """Get Program Files directory on Windows, or /usr/local on Unix."""
    if platform.system() == "Windows":
        return os.environ.get("ProgramFiles", r"C:\Program Files")
    else:
        return "/usr/local"
