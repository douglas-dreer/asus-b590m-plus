"""
SHA256 hash validation utilities
"""

import hashlib
import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


def calculate_sha256(file_path: str, chunk_size: int = 8192) -> str:
    """
    Calculate SHA256 hash of a file
    
    Args:
        file_path: Path to file
        chunk_size: Size of chunks to read (default: 8192 bytes)
        
    Returns:
        SHA256 hash as hexadecimal string (lowercase)
    """
    sha256_hash = hashlib.sha256()
    
    try:
        with open(file_path, 'rb') as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                sha256_hash.update(chunk)
        
        hash_value = sha256_hash.hexdigest()
        logger.debug(f"Calculated SHA256 for {file_path}: {hash_value}")
        return hash_value
        
    except Exception as e:
        logger.error(f"Error calculating SHA256 for {file_path}: {e}")
        raise


def verify_hash(file_path: str, expected_hash: Optional[str]) -> bool:
    """
    Verify file integrity using SHA256 hash
    
    Args:
        file_path: Path to file to verify
        expected_hash: Expected SHA256 hash (can be None or empty)
        
    Returns:
        True if hash matches or no expected hash provided, False if mismatch
    """
    # If no expected hash, log warning but return True
    if not expected_hash or expected_hash.strip() == '':
        logger.warning(f"No SHA256 hash provided for {file_path}, skipping validation")
        return True
    
    try:
        # Calculate actual hash
        actual_hash = calculate_sha256(file_path)
        
        # Compare (case-insensitive)
        expected_hash_lower = expected_hash.lower().strip()
        actual_hash_lower = actual_hash.lower().strip()
        
        if actual_hash_lower == expected_hash_lower:
            logger.info(f"SHA256 validation successful for {file_path}")
            return True
        else:
            logger.error(f"SHA256 validation failed for {file_path}")
            logger.error(f"  Expected: {expected_hash_lower}")
            logger.error(f"  Actual:   {actual_hash_lower}")
            return False
            
    except Exception as e:
        logger.error(f"Error during hash verification: {e}")
        return False


def verify_file_integrity(file_path: str, expected_hash: Optional[str], file_size: Optional[int] = None) -> bool:
    """
    Verify file integrity using hash and optionally file size
    
    Args:
        file_path: Path to file
        expected_hash: Expected SHA256 hash
        file_size: Expected file size in bytes (optional)
        
    Returns:
        True if all checks pass, False otherwise
    """
    path = Path(file_path)
    
    # Check file exists
    if not path.exists():
        logger.error(f"File does not exist: {file_path}")
        return False
    
    # Check file size if provided
    if file_size is not None:
        actual_size = path.stat().st_size
        if actual_size != file_size:
            logger.error(f"File size mismatch for {file_path}")
            logger.error(f"  Expected: {file_size} bytes")
            logger.error(f"  Actual:   {actual_size} bytes")
            return False
        logger.debug(f"File size check passed: {actual_size} bytes")
    
    # Verify hash
    return verify_hash(file_path, expected_hash)
