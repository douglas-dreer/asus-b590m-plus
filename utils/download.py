"""
Download utilities with retry logic and progress tracking
"""

import requests
import logging
import time
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


def download_file(url: str, output_path: str, max_retries: int = 3, timeout: int = 600) -> bool:
    """
    Download file from URL with retry logic
    
    Args:
        url: URL to download from
        output_path: Local path to save file
        max_retries: Maximum number of retry attempts
        timeout: Timeout in seconds for each attempt
        
    Returns:
        True if download successful, False otherwise
    """
    for attempt in range(1, max_retries + 1):
        try:
            logger.info(f"Downloading from {url} (attempt {attempt}/{max_retries})")
            
            # Make request with timeout
            response = requests.get(url, timeout=timeout, stream=True)
            response.raise_for_status()
            
            # Get file size if available
            total_size = int(response.headers.get('content-length', 0))
            
            # Download with progress tracking
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'wb') as f:
                if total_size == 0:
                    # No content-length header
                    f.write(response.content)
                else:
                    downloaded = 0
                    chunk_size = 8192
                    for chunk in response.iter_content(chunk_size=chunk_size):
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)
                            # Log progress every 10MB
                            if downloaded % (10 * 1024 * 1024) < chunk_size:
                                progress = (downloaded / total_size) * 100 if total_size > 0 else 0
                                logger.info(f"Progress: {progress:.1f}% ({downloaded}/{total_size} bytes)")
            
            logger.info(f"Download completed: {output_path}")
            return True
            
        except requests.exceptions.Timeout:
            logger.warning(f"Download timeout on attempt {attempt}")
            if attempt < max_retries:
                wait_time = 2 ** (attempt - 1)  # Exponential backoff: 1s, 2s, 4s
                logger.info(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
        except requests.exceptions.RequestException as e:
            logger.error(f"Download error on attempt {attempt}: {e}")
            if attempt < max_retries:
                wait_time = 2 ** (attempt - 1)
                logger.info(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
        except Exception as e:
            logger.error(f"Unexpected error during download: {e}")
            return False
    
    logger.error(f"Download failed after {max_retries} attempts")
    return False


def download_with_progress_bar(url: str, output_path: str, max_retries: int = 3, timeout: int = 600) -> bool:
    """
    Download file with tqdm progress bar (optional enhancement)
    
    Args:
        url: URL to download from
        output_path: Local path to save file
        max_retries: Maximum number of retry attempts
        timeout: Timeout in seconds
        
    Returns:
        True if download successful, False otherwise
    """
    try:
        from tqdm import tqdm
        
        for attempt in range(1, max_retries + 1):
            try:
                logger.info(f"Downloading from {url} (attempt {attempt}/{max_retries})")
                
                response = requests.get(url, timeout=timeout, stream=True)
                response.raise_for_status()
                
                total_size = int(response.headers.get('content-length', 0))
                
                output_file = Path(output_path)
                output_file.parent.mkdir(parents=True, exist_ok=True)
                
                with open(output_path, 'wb') as f, tqdm(
                    desc=output_file.name,
                    total=total_size,
                    unit='B',
                    unit_scale=True,
                    unit_divisor=1024,
                ) as pbar:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            pbar.update(len(chunk))
                
                logger.info(f"Download completed: {output_path}")
                return True
                
            except requests.exceptions.Timeout:
                logger.warning(f"Download timeout on attempt {attempt}")
                if attempt < max_retries:
                    wait_time = 2 ** (attempt - 1)
                    logger.info(f"Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
            except requests.exceptions.RequestException as e:
                logger.error(f"Download error on attempt {attempt}: {e}")
                if attempt < max_retries:
                    wait_time = 2 ** (attempt - 1)
                    logger.info(f"Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
        
        logger.error(f"Download failed after {max_retries} attempts")
        return False
        
    except ImportError:
        # tqdm not available, fall back to basic download
        logger.info("tqdm not available, using basic download")
        return download_file(url, output_path, max_retries, timeout)
