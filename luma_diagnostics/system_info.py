"""Collect system information for diagnostics."""

import platform
import sys
import os
import json
from datetime import datetime
import psutil

def get_system_info():
    """Collect relevant system information for diagnostics."""
    info = {
        "timestamp": datetime.now().isoformat(),
        "system": {
            "platform": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "python_version": sys.version,
        },
        "memory": {
            "total": psutil.virtual_memory().total,
            "available": psutil.virtual_memory().available,
        },
        "disk": {
            "total": psutil.disk_usage('/').total,
            "free": psutil.disk_usage('/').free,
        },
        "environment": {
            "LUMA_API_KEY_SET": bool(os.getenv("LUMA_API_KEY")),
        }
    }
    return info

def format_system_info(info):
    """Format system information for display."""
    return f"""System Information:
Platform: {info['system']['platform']} {info['system']['release']}
Machine: {info['system']['machine']}
Python Version: {info['system']['python_version'].split()[0]}
Memory: {info['memory']['available'] / (1024**3):.1f}GB available / {info['memory']['total'] / (1024**3):.1f}GB total
Disk: {info['disk']['free'] / (1024**3):.1f}GB free / {info['disk']['total'] / (1024**3):.1f}GB total
"""
