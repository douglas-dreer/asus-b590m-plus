"""
Core installer module with OS detection and driver installation orchestration
"""

import platform
import logging
from typing import Tuple, Dict, Any
from pathlib import Path

logger = logging.getLogger(__name__)


def detect_os() -> str:
    """
    Detect operating system
    
    Returns:
        'Windows' or 'Linux'
    """
    system = platform.system()
    logger.info(f"Detected OS: {system}")
    return system


def install_driver(entry: Dict[str, Any], file_path: str, os_type: str) -> bool:
    """
    Install driver based on type and operating system
    
    Args:
        entry: Manifest entry dictionary (name, type, silentArgs, etc.)
        file_path: Path to the driver file
        os_type: Operating system ('Windows' or 'Linux')
        
    Returns:
        True if installation successful, False otherwise
    """
    driver_name = entry.get('name', 'Unknown')
    driver_type = entry.get('type', '').lower()
    silent_args = entry.get('silentArgs')
    
    logger.info(f"Installing driver: {driver_name} (type: {driver_type})")
    
    # Handle manual installation type
    if driver_type == 'manual':
        logger.info(f"Manual installation required for: {driver_name}")
        create_manual_note(entry, file_path)
        return True
    
    # Install based on OS and type
    if os_type == 'Windows':
        return _install_windows_driver(driver_type, file_path, silent_args)
    elif os_type == 'Linux':
        return _install_linux_driver(driver_type, file_path)
    else:
        logger.error(f"Unsupported OS: {os_type}")
        return False


def _install_windows_driver(driver_type: str, file_path: str, silent_args: str = None) -> bool:
    """Install driver on Windows"""
    from installer.windows import install_exe, install_msi, install_zip
    
    if driver_type == 'exe':
        success, exit_code = install_exe(file_path, silent_args)
        return success
    elif driver_type == 'msi':
        success, exit_code = install_msi(file_path)
        return success
    elif driver_type == 'zip':
        success, exit_code = install_zip(file_path)
        return success
    else:
        logger.error(f"Unsupported Windows driver type: {driver_type}")
        return False


def _install_linux_driver(driver_type: str, file_path: str) -> bool:
    """Install driver on Linux"""
    from installer.linux import install_deb, install_rpm
    
    if driver_type == 'deb':
        success, exit_code = install_deb(file_path)
        return success
    elif driver_type == 'rpm':
        success, exit_code = install_rpm(file_path)
        return success
    else:
        logger.error(f"Unsupported Linux driver type: {driver_type}")
        return False


def create_manual_note(entry: Dict[str, Any], work_dir: str) -> None:
    """
    Create a manual installation note file
    
    Args:
        entry: Manifest entry dictionary
        work_dir: Working directory path
    """
    from datetime import datetime
    
    driver_name = entry.get('name', 'Unknown')
    url = entry.get('url', 'No URL provided')
    
    note_file = Path(work_dir) / f"{driver_name.replace(' ', '_')}.manual.txt"
    
    try:
        with open(note_file, 'w') as f:
            f.write(f"Manual Installation Required\n")
            f.write(f"{'=' * 50}\n\n")
            f.write(f"Driver: {driver_name}\n")
            f.write(f"URL: {url}\n")
            f.write(f"Timestamp: {datetime.now().isoformat()}\n\n")
            f.write(f"Please download and install this driver manually.\n")
        
        logger.info(f"Created manual installation note: {note_file}")
    except Exception as e:
        logger.error(f"Failed to create manual note: {e}")
