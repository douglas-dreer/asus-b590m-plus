"""
Windows driver installation module
Handles installation of exe, msi, and zip drivers on Windows
"""

import subprocess
import logging
from pathlib import Path
from typing import Tuple, Optional

logger = logging.getLogger(__name__)


def install_exe(file_path: str, silent_args: Optional[str] = None) -> Tuple[bool, int]:
    """
    Install Windows executable with silent arguments
    
    Args:
        file_path: Path to the .exe file
        silent_args: Custom silent arguments (optional)
        
    Returns:
        Tuple of (success: bool, exit_code: int)
    """
    # List of silent arguments to try in order
    silent_args_list = [
        silent_args,  # Custom args from manifest
        '/S',
        '/silent',
        '/quiet',
        '/verysilent',
        '/s',
        '/s /v"/qn"',
        '/S /v"/qn"'
    ]
    
    for args in silent_args_list:
        if args is None:
            continue
            
        try:
            logger.info(f"Attempting installation with args: {args}")
            cmd = f'"{file_path}" {args}'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0 or result.returncode == 3010 or result.returncode == 1641:
                logger.info(f"Installation successful with exit code: {result.returncode}")
                return True, result.returncode
            else:
                logger.warning(f"Installation failed with exit code: {result.returncode}")
        except Exception as e:
            logger.error(f"Error during installation: {e}")
            continue
    
    # If all silent attempts fail, try without arguments
    logger.warning("All silent installation attempts failed, running without arguments")
    try:
        result = subprocess.run(f'"{file_path}"', shell=True)
        return False, result.returncode
    except Exception as e:
        logger.error(f"Final installation attempt failed: {e}")
        return False, -1


def install_msi(file_path: str) -> Tuple[bool, int]:
    """
    Install Windows MSI package
    
    Args:
        file_path: Path to the .msi file
        
    Returns:
        Tuple of (success: bool, exit_code: int)
    """
    try:
        cmd = f'msiexec.exe /i "{file_path}" /qn /norestart'
        logger.info(f"Executing: {cmd}")
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        # Exit codes: 0 = success, 3010 = success with reboot required, 1641 = success with reboot initiated
        if result.returncode in [0, 3010, 1641]:
            logger.info(f"MSI installation successful with exit code: {result.returncode}")
            return True, result.returncode
        else:
            logger.error(f"MSI installation failed with exit code: {result.returncode}")
            return False, result.returncode
    except Exception as e:
        logger.error(f"Error during MSI installation: {e}")
        return False, -1


def install_zip(file_path: str) -> Tuple[bool, int]:
    """
    Extract ZIP and install the installer found inside
    
    Args:
        file_path: Path to the .zip file
        
    Returns:
        Tuple of (success: bool, exit_code: int)
    """
    import zipfile
    import tempfile
    import shutil
    
    temp_dir = None
    try:
        # Create temporary directory
        temp_dir = tempfile.mkdtemp()
        logger.info(f"Extracting ZIP to: {temp_dir}")
        
        # Extract ZIP
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
        
        # Search for installers (exe or msi)
        temp_path = Path(temp_dir)
        installers = sorted(list(temp_path.rglob('*.exe')) + list(temp_path.rglob('*.msi')))
        
        if not installers:
            logger.error(f"No installer found inside ZIP: {file_path}")
            return False, -1
        
        # Use first installer found
        installer = installers[0]
        logger.info(f"Found installer: {installer}")
        
        # Install based on extension
        if installer.suffix.lower() == '.exe':
            return install_exe(str(installer))
        elif installer.suffix.lower() == '.msi':
            return install_msi(str(installer))
        else:
            logger.error(f"Unknown installer type: {installer.suffix}")
            return False, -1
            
    except Exception as e:
        logger.error(f"Error during ZIP installation: {e}")
        return False, -1
    finally:
        # Cleanup temporary directory
        if temp_dir:
            try:
                shutil.rmtree(temp_dir)
                logger.info(f"Cleaned up temporary directory: {temp_dir}")
            except Exception as e:
                logger.warning(f"Failed to cleanup temporary directory: {e}")
