"""
Initialization and validation module for the driver installer
Handles Python version checks, dependency validation, OS detection, and privilege verification
"""

import sys
import os
import platform
import logging
import argparse
import subprocess
from typing import Tuple, Optional
from pathlib import Path

logger = logging.getLogger(__name__)


def check_python_version(min_version: Tuple[int, int] = (3, 7)) -> bool:
    """
    Verify if Python version meets minimum requirements
    
    Args:
        min_version: Minimum required Python version as tuple (major, minor)
        
    Returns:
        True if Python version is sufficient, False otherwise
    """
    current_version = sys.version_info[:2]
    
    if current_version >= min_version:
        logger.info(f"Python version check passed: {sys.version.split()[0]}")
        return True
    else:
        logger.error(
            f"Python version {current_version[0]}.{current_version[1]} is below "
            f"minimum required version {min_version[0]}.{min_version[1]}"
        )
        return False


def check_dependencies(requirements_file: str = 'requirements.txt') -> bool:
    """
    Verify if all dependencies from requirements.txt are installed
    
    Args:
        requirements_file: Path to requirements.txt file
        
    Returns:
        True if all dependencies are installed, False otherwise
    """
    req_path = Path(requirements_file)
    
    if not req_path.exists():
        logger.warning(f"Requirements file not found: {requirements_file}")
        return True  # No requirements file means no dependencies to check
    
    logger.info(f"Checking dependencies from: {requirements_file}")
    
    try:
        # Read requirements file
        with open(req_path, 'r') as f:
            lines = f.readlines()
        
        # Parse package names (ignore comments, empty lines, and version specifiers)
        packages = []
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):
                # Extract package name (before >=, ==, <, >, etc.)
                pkg_name = line.split('>=')[0].split('==')[0].split('<')[0].split('>')[0].split(';')[0].strip()
                if pkg_name:
                    packages.append(pkg_name)
        
        # Check each package
        missing_packages = []
        for package in packages:
            try:
                __import__(package.replace('-', '_'))
                logger.debug(f"Dependency found: {package}")
            except ImportError:
                missing_packages.append(package)
                logger.warning(f"Missing dependency: {package}")
        
        if missing_packages:
            logger.error(
                f"Missing dependencies: {', '.join(missing_packages)}\n"
                f"Install with: pip install -r {requirements_file}"
            )
            return False
        
        logger.info("All dependencies are installed")
        return True
        
    except Exception as e:
        logger.error(f"Error checking dependencies: {e}")
        return False


def detect_os() -> str:
    """
    Detect the operating system
    
    Returns:
        'Windows' or 'Linux' or 'Unknown'
    """
    system = platform.system()
    
    if system == 'Windows':
        logger.info(f"Detected OS: Windows {platform.release()}")
        return 'Windows'
    elif system == 'Linux':
        logger.info(f"Detected OS: Linux {platform.release()}")
        return 'Linux'
    else:
        logger.warning(f"Unknown or unsupported OS: {system}")
        return 'Unknown'


def check_admin_privileges() -> bool:
    """
    Check if the script is running with elevated privileges
    
    Returns:
        True if running as admin/root, False otherwise
    """
    system = platform.system()
    
    try:
        if system == 'Windows':
            # Check if running as administrator on Windows
            import ctypes
            is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
            
            if is_admin:
                logger.info("Running with Administrator privileges")
            else:
                logger.error("Not running with Administrator privileges")
                logger.error("Please run this script as Administrator")
            
            return is_admin
            
        elif system == 'Linux':
            # Check if running as root or with sudo on Linux
            is_root = os.geteuid() == 0
            
            if is_root:
                logger.info("Running with root/sudo privileges")
            else:
                logger.error("Not running with root/sudo privileges")
                logger.error("Please run this script with sudo")
            
            return is_root
            
        else:
            logger.warning(f"Cannot verify privileges on {system}")
            return False
            
    except Exception as e:
        logger.error(f"Error checking admin privileges: {e}")
        return False


def create_argument_parser() -> argparse.ArgumentParser:
    """
    Create and configure command-line argument parser
    
    Returns:
        Configured ArgumentParser instance
    """
    parser = argparse.ArgumentParser(
        description='Silent Driver Installer - Automated driver installation for Windows and Linux',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python setup-drivers.py
  python setup-drivers.py --manifest custom-drivers.json
  python setup-drivers.py --auto-reboot --force
  python setup-drivers.py --dry-run --verbose
        """
    )
    
    parser.add_argument(
        '--manifest',
        type=str,
        default='./downloads/drivers.json',
        help='Path to the driver manifest JSON file (default: ./downloads/drivers.json)'
    )
    
    parser.add_argument(
        '--auto-reboot',
        action='store_true',
        help='Automatically reboot the system after installation if required'
    )
    
    parser.add_argument(
        '--force',
        action='store_true',
        help='Force re-download of files even if they already exist'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Simulate installation without actually installing drivers'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging output'
    )
    
    parser.add_argument(
        '--no-backup',
        action='store_true',
        help='Skip driver backup (Windows only)'
    )
    
    parser.add_argument(
        '--force-reinstall',
        action='store_true',
        help='Force reinstallation even if driver is already installed'
    )
    
    return parser


def validate_environment() -> Tuple[bool, Optional[str]]:
    """
    Validate the entire environment (Python version, dependencies, OS, privileges)
    
    Returns:
        Tuple of (success: bool, error_message: Optional[str])
    """
    # Check Python version
    if not check_python_version():
        return False, "Python 3.7 or higher is required"
    
    # Check dependencies
    if not check_dependencies():
        return False, "Missing required dependencies. Run: pip install -r requirements.txt"
    
    # Detect OS
    os_type = detect_os()
    if os_type == 'Unknown':
        return False, "Unsupported operating system"
    
    # Check admin privileges
    if not check_admin_privileges():
        if os_type == 'Windows':
            return False, "Administrator privileges required. Run as Administrator."
        else:
            return False, "Root privileges required. Run with sudo."
    
    logger.info("Environment validation completed successfully")
    return True, None
