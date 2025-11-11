"""
Linux driver installation module
Handles installation of deb and rpm packages on Linux
"""

import subprocess
import logging
from typing import Tuple

logger = logging.getLogger(__name__)


def install_deb(file_path: str) -> Tuple[bool, int]:
    """
    Install Debian package (deb)
    
    Args:
        file_path: Path to the .deb file
        
    Returns:
        Tuple of (success: bool, exit_code: int)
    """
    try:
        # Try dpkg first
        cmd = f'dpkg -i "{file_path}"'
        logger.info(f"Executing: {cmd}")
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            logger.info("DEB installation successful")
            return True, result.returncode
        
        # If dpkg fails, try apt
        logger.warning("dpkg failed, trying apt install")
        cmd = f'apt install -y "{file_path}"'
        logger.info(f"Executing: {cmd}")
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            logger.info("DEB installation successful via apt")
            return True, result.returncode
        else:
            logger.error(f"DEB installation failed with exit code: {result.returncode}")
            return False, result.returncode
            
    except Exception as e:
        logger.error(f"Error during DEB installation: {e}")
        return False, -1


def install_rpm(file_path: str) -> Tuple[bool, int]:
    """
    Install RPM package
    
    Args:
        file_path: Path to the .rpm file
        
    Returns:
        Tuple of (success: bool, exit_code: int)
    """
    try:
        # Try rpm first
        cmd = f'rpm -i "{file_path}"'
        logger.info(f"Executing: {cmd}")
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            logger.info("RPM installation successful")
            return True, result.returncode
        
        # If rpm fails, try dnf
        logger.warning("rpm failed, trying dnf install")
        cmd = f'dnf install -y "{file_path}"'
        logger.info(f"Executing: {cmd}")
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            logger.info("RPM installation successful via dnf")
            return True, result.returncode
        
        # If dnf fails, try yum
        logger.warning("dnf failed, trying yum install")
        cmd = f'yum install -y "{file_path}"'
        logger.info(f"Executing: {cmd}")
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            logger.info("RPM installation successful via yum")
            return True, result.returncode
        else:
            logger.error(f"RPM installation failed with exit code: {result.returncode}")
            return False, result.returncode
            
    except Exception as e:
        logger.error(f"Error during RPM installation: {e}")
        return False, -1


def detect_distribution() -> str:
    """
    Detect Linux distribution
    
    Returns:
        Distribution name (debian, ubuntu, fedora, arch, unknown)
    """
    try:
        with open('/etc/os-release', 'r') as f:
            content = f.read().lower()
            
        if 'debian' in content:
            return 'debian'
        elif 'ubuntu' in content:
            return 'ubuntu'
        elif 'fedora' in content:
            return 'fedora'
        elif 'arch' in content:
            return 'arch'
        else:
            return 'unknown'
    except Exception as e:
        logger.warning(f"Failed to detect distribution: {e}")
        return 'unknown'
