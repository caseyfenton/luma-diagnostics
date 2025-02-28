"""
File utility functions for LUMA Diagnostics.
These functions help with handling image files and retrieving their properties.
"""

import os
from typing import Dict, Any, Optional
from PIL import Image
import mimetypes

def get_file_info(file_path: str) -> Dict[str, Any]:
    """
    Get detailed information about a file, with special handling for images.
    
    Args:
        file_path: Path to the file to analyze
    
    Returns:
        Dict containing file information including size, format, dimensions (for images), etc.
    
    Raises:
        FileNotFoundError: If the file doesn't exist
        ValueError: If there's a problem reading the file
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    # Get basic file info
    file_stats = os.stat(file_path)
    size_bytes = file_stats.st_size
    size_kb = size_bytes / 1024
    
    # Get file type
    mime_type, _ = mimetypes.guess_type(file_path)
    
    # Basic info all files will have
    info = {
        "path": file_path,
        "size_bytes": size_bytes,
        "size_kb": round(size_kb, 2),
        "mime_type": mime_type or "application/octet-stream"
    }
    
    # For images, get extra info
    try:
        if mime_type and mime_type.startswith('image/'):
            with Image.open(file_path) as img:
                info.update({
                    "format": img.format,
                    "width": img.width,
                    "height": img.height,
                    "mode": img.mode,
                    "is_animated": getattr(img, "is_animated", False),
                    "n_frames": getattr(img, "n_frames", 1)
                })
    except Exception as e:
        # If there's an error reading as image, still return basic info
        info["error"] = str(e)
        
    return info

def is_valid_image(file_path: str) -> bool:
    """
    Check if a file is a valid image that can be processed by LUMA APIs.
    
    Args:
        file_path: Path to the file to check
    
    Returns:
        Boolean indicating if the file is a valid image
    """
    try:
        info = get_file_info(file_path)
        
        # Check if it's an image
        if not info.get("mime_type", "").startswith("image/"):
            return False
            
        # Check if we could read image properties
        if "width" not in info or "height" not in info:
            return False
            
        # Check for a supported format (based on LUMA API requirements)
        supported_formats = ["JPEG", "PNG", "WEBP", "GIF", "TIFF"]
        if info.get("format") not in supported_formats:
            return False
            
        # Check for reasonable size constraints
        if info.get("size_bytes", 0) > 15 * 1024 * 1024:  # Max 15MB
            return False
            
        return True
    except Exception:
        return False

def create_temp_image(dimensions: tuple = (512, 512), 
                     color: tuple = (255, 255, 255), 
                     format: str = "JPEG") -> str:
    """
    Create a temporary test image file.
    
    Args:
        dimensions: Tuple of (width, height)
        color: RGB color tuple
        format: Image format (JPEG, PNG, etc.)
    
    Returns:
        Path to the created temporary file
    """
    import tempfile
    
    # Create a temporary file with the correct extension
    ext = format.lower()
    fd, path = tempfile.mkstemp(suffix=f'.{ext}')
    os.close(fd)
    
    # Create and save the image
    img = Image.new('RGB', dimensions, color)
    img.save(path, format=format)
    
    return path
