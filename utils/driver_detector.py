"""
Driver Detection Module
Provides functionality to detect installed drivers and compare with available drivers
"""

import json
import logging
import platform
import subprocess
from pathlib import Path
from typing import List, Dict, Optional, Tuple

logger = logging.getLogger(__name__)


def load_drivers_manifest(manifest_path: str) -> Optional[List[Dict]]:
    """
    Load drivers from a JSON manifest file
    
    Args:
        manifest_path: Path to the drivers JSON manifest file
        
    Returns:
        List of driver dictionaries or None if loading fails
    """
    try:
        manifest_file = Path(manifest_path)
        if not manifest_file.exists():
            logger.error(f"Manifest file not found: {manifest_path}")
            return None
            
        with open(manifest_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        # Support both {"drivers": [...]} and direct array format
        if isinstance(data, dict) and 'drivers' in data:
            drivers = data['drivers']
        elif isinstance(data, list):
            drivers = data
        else:
            logger.error("Invalid manifest format: expected 'drivers' key or array")
            return None
            
        logger.info(f"Loaded {len(drivers)} drivers from manifest: {manifest_path}")
        return drivers
        
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON manifest: {e}")
        return None
    except Exception as e:
        logger.error(f"Error loading manifest: {e}")
        return None


def list_available_drivers(manifest_path: str, os_filter: Optional[str] = None) -> List[Dict]:
    """
    List all available drivers from the manifest
    
    Args:
        manifest_path: Path to the drivers JSON manifest file
        os_filter: Optional OS filter ('windows' or 'linux')
        
    Returns:
        List of available driver dictionaries
    """
    drivers = load_drivers_manifest(manifest_path)
    if drivers is None:
        return []
    
    # Filter by OS if specified
    if os_filter:
        os_filter = os_filter.lower()
        drivers = [d for d in drivers if d.get('os', '').lower() == os_filter]
        logger.info(f"Filtered to {len(drivers)} drivers for OS: {os_filter}")
    
    return drivers


def get_installed_drivers_windows() -> List[Dict]:
    """
    Get list of installed drivers on Windows using DISM and WMI
    
    Returns:
        List of installed driver dictionaries with name, version, deviceId
    """
    installed = []
    
    try:
        # Use DISM to get driver information
        result = subprocess.run(
            ['dism', '/online', '/get-drivers', '/format:table'],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            logger.debug("Successfully retrieved driver list from DISM")
            # Parse DISM output (simplified - would need more robust parsing)
            lines = result.stdout.split('\n')
            for line in lines:
                if 'Published Name' in line or '---' in line or not line.strip():
                    continue
                # Basic parsing - this is a simplified version
                parts = line.split('|')
                if len(parts) >= 3:
                    installed.append({
                        'name': parts[0].strip() if len(parts) > 0 else '',
                        'version': parts[2].strip() if len(parts) > 2 else '',
                        'deviceId': ''
                    })
        
        # Alternative: Use WMI via PowerShell for more detailed info
        ps_command = """
        Get-WmiObject Win32_PnPSignedDriver | 
        Select-Object DeviceName, DriverVersion, HardwareID | 
        ConvertTo-Json -Compress
        """
        
        result = subprocess.run(
            ['powershell', '-Command', ps_command],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0 and result.stdout.strip():
            try:
                wmi_drivers = json.loads(result.stdout)
                if isinstance(wmi_drivers, dict):
                    wmi_drivers = [wmi_drivers]
                    
                for driver in wmi_drivers:
                    hardware_id = driver.get('HardwareID', [''])[0] if isinstance(driver.get('HardwareID'), list) else driver.get('HardwareID', '')
                    installed.append({
                        'name': driver.get('DeviceName', ''),
                        'version': driver.get('DriverVersion', ''),
                        'deviceId': hardware_id
                    })
                    
                logger.info(f"Retrieved {len(installed)} drivers from WMI")
            except json.JSONDecodeError:
                logger.warning("Failed to parse WMI driver information")
                
    except subprocess.TimeoutExpired:
        logger.error("Timeout while retrieving installed drivers")
    except FileNotFoundError:
        logger.error("Required tools (DISM/PowerShell) not found")
    except Exception as e:
        logger.error(f"Error retrieving installed drivers: {e}")
    
    return installed


def get_installed_drivers_linux() -> List[Dict]:
    """
    Get list of installed drivers on Linux using lsmod and modinfo
    
    Returns:
        List of installed driver dictionaries with name, version, deviceId
    """
    installed = []
    
    try:
        # Get loaded kernel modules
        result = subprocess.run(
            ['lsmod'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            lines = result.stdout.split('\n')[1:]  # Skip header
            module_names = []
            
            for line in lines:
                if line.strip():
                    parts = line.split()
                    if parts:
                        module_names.append(parts[0])
            
            # Get detailed info for each module
            for module_name in module_names[:50]:  # Limit to first 50 to avoid timeout
                try:
                    modinfo_result = subprocess.run(
                        ['modinfo', module_name],
                        capture_output=True,
                        text=True,
                        timeout=5
                    )
                    
                    if modinfo_result.returncode == 0:
                        version = ''
                        alias = ''
                        
                        for line in modinfo_result.stdout.split('\n'):
                            if line.startswith('version:'):
                                version = line.split(':', 1)[1].strip()
                            elif line.startswith('alias:') and 'pci:' in line:
                                alias = line.split(':', 1)[1].strip()
                        
                        installed.append({
                            'name': module_name,
                            'version': version,
                            'deviceId': alias
                        })
                        
                except subprocess.TimeoutExpired:
                    continue
                except Exception:
                    continue
            
            logger.info(f"Retrieved {len(installed)} drivers from lsmod/modinfo")
            
    except subprocess.TimeoutExpired:
        logger.error("Timeout while retrieving installed drivers")
    except FileNotFoundError:
        logger.error("Required tools (lsmod/modinfo) not found")
    except Exception as e:
        logger.error(f"Error retrieving installed drivers: {e}")
    
    return installed


def list_installed_drivers() -> List[Dict]:
    """
    List all installed drivers on the current system
    
    Returns:
        List of installed driver dictionaries
    """
    os_type = platform.system().lower()
    
    if os_type == 'windows':
        logger.info("Detecting installed drivers on Windows...")
        return get_installed_drivers_windows()
    elif os_type == 'linux':
        logger.info("Detecting installed drivers on Linux...")
        return get_installed_drivers_linux()
    else:
        logger.warning(f"Unsupported OS for driver detection: {os_type}")
        return []


def normalize_device_id(device_id: str) -> str:
    """
    Normalize device ID for comparison (remove prefixes, convert to lowercase)
    
    Args:
        device_id: Device ID string
        
    Returns:
        Normalized device ID
    """
    if not device_id:
        return ''
    
    # Remove common prefixes and normalize
    device_id = device_id.upper()
    device_id = device_id.replace('PCI\\', '').replace('HDAUDIO\\', '')
    device_id = device_id.replace('USB\\', '').replace('ACPI\\', '')
    
    # Extract VEN and DEV if present
    if 'VEN_' in device_id and 'DEV_' in device_id:
        try:
            ven_start = device_id.index('VEN_') + 4
            ven_end = device_id.index('&', ven_start) if '&' in device_id[ven_start:] else len(device_id)
            vendor = device_id[ven_start:ven_end]
            
            dev_start = device_id.index('DEV_') + 4
            dev_end = device_id.index('&', dev_start) if '&' in device_id[dev_start:] else len(device_id)
            device = device_id[dev_start:dev_end]
            
            return f"VEN_{vendor}&DEV_{device}"
        except (ValueError, IndexError):
            pass
    
    return device_id


def match_driver(available_driver: Dict, installed_drivers: List[Dict]) -> Optional[Dict]:
    """
    Find matching installed driver for an available driver
    
    Args:
        available_driver: Driver from manifest
        installed_drivers: List of installed drivers
        
    Returns:
        Matching installed driver or None
    """
    available_device_id = normalize_device_id(available_driver.get('deviceId', ''))
    available_name = (available_driver.get('name') or '').lower()
    
    for installed in installed_drivers:
        installed_device_id = normalize_device_id(installed.get('deviceId', ''))
        installed_name = (installed.get('name') or '').lower()
        
        # Match by device ID (most reliable)
        if available_device_id and installed_device_id:
            if available_device_id == installed_device_id:
                return installed
        
        # Fallback: Match by name (partial match)
        if available_name and installed_name:
            # Check if key terms match
            available_terms = set(available_name.split())
            installed_terms = set(installed_name.split())
            common_terms = available_terms & installed_terms
            
            # If at least 2 significant terms match, consider it a match
            if len(common_terms) >= 2:
                return installed
    
    return None


def list_not_installed_drivers(manifest_path: str, os_filter: Optional[str] = None) -> List[Dict]:
    """
    List drivers from manifest that are not currently installed
    
    Args:
        manifest_path: Path to the drivers JSON manifest file
        os_filter: Optional OS filter ('windows' or 'linux')
        
    Returns:
        List of driver dictionaries that are not installed
    """
    available = list_available_drivers(manifest_path, os_filter)
    installed = list_installed_drivers()
    
    not_installed = []
    for driver in available:
        if not match_driver(driver, installed):
            not_installed.append(driver)
    
    logger.info(f"Found {len(not_installed)} drivers not installed")
    return not_installed


def compare_versions(version1: str, version2: str) -> int:
    """
    Compare two version strings
    
    Args:
        version1: First version string
        version2: Second version string
        
    Returns:
        -1 if version1 < version2, 0 if equal, 1 if version1 > version2
    """
    if not version1 or not version2:
        return 0
    
    try:
        # Split versions and compare numerically
        parts1 = [int(x) for x in version1.split('.') if x.isdigit()]
        parts2 = [int(x) for x in version2.split('.') if x.isdigit()]
        
        # Pad shorter version with zeros
        max_len = max(len(parts1), len(parts2))
        parts1.extend([0] * (max_len - len(parts1)))
        parts2.extend([0] * (max_len - len(parts2)))
        
        for p1, p2 in zip(parts1, parts2):
            if p1 < p2:
                return -1
            elif p1 > p2:
                return 1
        
        return 0
    except (ValueError, AttributeError):
        # Fallback to string comparison
        if version1 < version2:
            return -1
        elif version1 > version2:
            return 1
        return 0


def list_drivers_with_different_versions(manifest_path: str, os_filter: Optional[str] = None) -> List[Tuple[Dict, Dict]]:
    """
    List drivers that are installed but with different versions than in manifest
    
    Args:
        manifest_path: Path to the drivers JSON manifest file
        os_filter: Optional OS filter ('windows' or 'linux')
        
    Returns:
        List of tuples (available_driver, installed_driver) with version differences
    """
    available = list_available_drivers(manifest_path, os_filter)
    installed = list_installed_drivers()
    
    different_versions = []
    for driver in available:
        matched = match_driver(driver, installed)
        if matched:
            available_version = driver.get('version', '')
            installed_version = matched.get('version', '')
            
            if available_version and installed_version:
                comparison = compare_versions(installed_version, available_version)
                if comparison != 0:
                    different_versions.append((driver, matched))
    
    logger.info(f"Found {len(different_versions)} drivers with different versions")
    return different_versions


def list_drivers_needing_update(manifest_path: str, os_filter: Optional[str] = None) -> List[Dict]:
    """
    List all drivers that need installation or update
    Combines not installed drivers and drivers with different versions
    
    Args:
        manifest_path: Path to the drivers JSON manifest file
        os_filter: Optional OS filter ('windows' or 'linux')
        
    Returns:
        List of driver dictionaries that need installation or update
    """
    not_installed = list_not_installed_drivers(manifest_path, os_filter)
    different_versions = list_drivers_with_different_versions(manifest_path, os_filter)
    
    # Combine results
    needing_update = not_installed.copy()
    
    # Add drivers with different versions (use available driver info)
    for available, installed in different_versions:
        if available not in needing_update:
            # Add note about current version
            driver_copy = available.copy()
            driver_copy['current_version'] = installed.get('version', 'unknown')
            needing_update.append(driver_copy)
    
    logger.info(f"Total drivers needing installation/update: {len(needing_update)}")
    return needing_update


def export_driver_list(drivers: List[Dict], output_path: str) -> bool:
    """
    Export driver list to a JSON file
    
    Args:
        drivers: List of driver dictionaries to export
        output_path: Path where to save the JSON file
        
    Returns:
        True if export successful, False otherwise
    """
    try:
        output_file = Path(output_path)
        
        # Create parent directory if it doesn't exist
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Write JSON with pretty formatting
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({'drivers': drivers}, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Exported {len(drivers)} drivers to: {output_path}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to export driver list: {e}")
        return False
