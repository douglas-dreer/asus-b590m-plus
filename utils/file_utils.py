"""
File management utilities
"""

import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


def ensure_directory(directory: str) -> Path:
    """
    Ensure directory exists, create if it doesn't
    
    Args:
        directory: Directory path
        
    Returns:
        Path object for the directory
    """
    dir_path = Path(directory)
    
    if dir_path.exists():
        logger.info(f"Directory already exists: {dir_path}")
    else:
        dir_path.mkdir(parents=True, exist_ok=True)
        logger.info(f"Created directory: {dir_path}")
    
    return dir_path


def file_exists(file_path: str) -> bool:
    """
    Check if file exists
    
    Args:
        file_path: Path to file
        
    Returns:
        True if file exists, False otherwise
    """
    return Path(file_path).exists()


def get_file_size(file_path: str) -> Optional[int]:
    """
    Get file size in bytes
    
    Args:
        file_path: Path to file
        
    Returns:
        File size in bytes, or None if file doesn't exist
    """
    path = Path(file_path)
    if path.exists():
        return path.stat().st_size
    return None


def cleanup_temp_files(directory: str, pattern: str = "*.tmp") -> None:
    """
    Clean up temporary files in directory
    
    Args:
        directory: Directory to clean
        pattern: File pattern to match (default: *.tmp)
    """
    dir_path = Path(directory)
    
    if not dir_path.exists():
        logger.warning(f"Directory does not exist: {dir_path}")
        return
    
    try:
        temp_files = list(dir_path.glob(pattern))
        for temp_file in temp_files:
            try:
                temp_file.unlink()
                logger.info(f"Deleted temporary file: {temp_file}")
            except Exception as e:
                logger.warning(f"Failed to delete {temp_file}: {e}")
        
        if temp_files:
            logger.info(f"Cleaned up {len(temp_files)} temporary files")
    except Exception as e:
        logger.error(f"Error during cleanup: {e}")
