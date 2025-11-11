"""
Vendor Database - Maps hardware vendor IDs to manufacturer information
"""

# Vendor ID to Manufacturer mapping (PCI Vendor IDs)
VENDOR_DATABASE = {
    '8086': {
        'name': 'Intel Corporation',
        'website': 'https://www.intel.com/content/www/us/en/download-center/home.html',
        'common_products': ['Chipset', 'Network', 'Graphics', 'Management Engine', 'Wireless']
    },
    '1002': {
        'name': 'AMD / ATI',
        'website': 'https://www.amd.com/en/support',
        'common_products': ['Graphics', 'Chipset', 'Audio']
    },
    '10DE': {
        'name': 'NVIDIA Corporation',
        'website': 'https://www.nvidia.com/Download/index.aspx',
        'common_products': ['Graphics', 'Audio']
    },
    '10EC': {
        'name': 'Realtek Semiconductor',
        'website': 'https://www.realtek.com/en/downloads',
        'common_products': ['Audio', 'Network', 'Card Reader', 'Storage']
    },
    '14E4': {
        'name': 'Broadcom',
        'website': 'https://www.broadcom.com/support/download-search',
        'common_products': ['Network', 'Wireless', 'Bluetooth']
    },
    '1CC1': {
        'name': 'ADATA Technology',
        'website': 'https://www.adata.com/en/support/downloads',
        'common_products': ['Storage', 'NVMe']
    },
    '1043': {
        'name': 'ASUSTeK Computer',
        'website': 'https://www.asus.com/support/download-center/',
        'common_products': ['Motherboard', 'Utilities']
    },
    '1462': {
        'name': 'Micro-Star International (MSI)',
        'website': 'https://www.msi.com/support/download',
        'common_products': ['Motherboard', 'Graphics']
    },
    '1458': {
        'name': 'Gigabyte Technology',
        'website': 'https://www.gigabyte.com/Support',
        'common_products': ['Motherboard', 'Graphics']
    },
    '1022': {
        'name': 'AMD',
        'website': 'https://www.amd.com/en/support',
        'common_products': ['Processor', 'Chipset']
    },
}

# Device type detection based on device ID patterns
DEVICE_TYPE_PATTERNS = {
    'HDAUDIO': 'Audio',
    'DISPLAY': 'Graphics',
    'NET': 'Network',
    'SCSI': 'Storage',
    'USB': 'USB Controller',
    'PCI': 'PCI Device',
}

# Windows generic drivers that should be excluded
WINDOWS_GENERIC_DRIVERS = [
    'WAN Miniport',
    'Generic software',
    'Microsoft',
    'ACPI',
    'System timer',
    'Programmable interrupt controller',
    'Numeric data processor',
    'High precision event timer',
    'PCI standard',
    'PCI-to-PCI Bridge',
    'Motherboard resources',
    'Computer Device',
    'Remote Desktop',
    'Plug and Play',
    'NDIS Virtual',
    'Local Print Queue',
    'Audio Endpoint',
    'Generic PnP Monitor',
    'Device Firmware',
    'System Firmware',
    'UEFI',
]


def extract_vendor_id(device_id: str) -> str:
    """
    Extract vendor ID from device ID string
    
    Args:
        device_id: Device ID string (e.g., "PCI\\VEN_8086&DEV_15FA...")
        
    Returns:
        Vendor ID (e.g., "8086") or empty string if not found
    """
    if not device_id:
        return ''
    
    device_id = device_id.upper()
    
    # Try to extract VEN_ pattern
    if 'VEN_' in device_id:
        try:
            start = device_id.index('VEN_') + 4
            end = device_id.index('&', start) if '&' in device_id[start:] else start + 4
            vendor_id = device_id[start:end]
            return vendor_id
        except (ValueError, IndexError):
            pass
    
    return ''


def extract_device_id(device_id: str) -> str:
    """
    Extract device ID from device ID string
    
    Args:
        device_id: Device ID string (e.g., "PCI\\VEN_8086&DEV_15FA...")
        
    Returns:
        Device ID (e.g., "15FA") or empty string if not found
    """
    if not device_id:
        return ''
    
    device_id = device_id.upper()
    
    # Try to extract DEV_ pattern
    if 'DEV_' in device_id:
        try:
            start = device_id.index('DEV_') + 4
            end = device_id.index('&', start) if '&' in device_id[start:] else start + 4
            dev_id = device_id[start:end]
            return dev_id
        except (ValueError, IndexError):
            pass
    
    return ''


def get_vendor_info(device_id: str) -> dict:
    """
    Get vendor information from device ID
    
    Args:
        device_id: Device ID string
        
    Returns:
        Dictionary with vendor name and website, or None if not found
    """
    vendor_id = extract_vendor_id(device_id)
    
    if vendor_id in VENDOR_DATABASE:
        return VENDOR_DATABASE[vendor_id]
    
    return None


def is_generic_windows_driver(driver_name: str) -> bool:
    """
    Check if driver is a generic Windows driver that shouldn't be included
    
    Args:
        driver_name: Name of the driver
        
    Returns:
        True if it's a generic Windows driver, False otherwise
    """
    if not driver_name:
        return True
    
    driver_name_lower = driver_name.lower()
    
    for generic_pattern in WINDOWS_GENERIC_DRIVERS:
        if generic_pattern.lower() in driver_name_lower:
            return True
    
    return False


def detect_device_type(driver_name: str, device_id: str) -> str:
    """
    Detect device type from driver name and device ID
    
    Args:
        driver_name: Name of the driver
        device_id: Device ID string
        
    Returns:
        Device type (e.g., "Audio", "Network", "Graphics")
    """
    if not driver_name:
        return 'Unknown'
    
    driver_name_lower = driver_name.lower()
    
    # Check common patterns in driver name
    if 'audio' in driver_name_lower or 'sound' in driver_name_lower:
        return 'Audio'
    elif 'network' in driver_name_lower or 'ethernet' in driver_name_lower or 'lan' in driver_name_lower:
        return 'Network'
    elif 'wireless' in driver_name_lower or 'wi-fi' in driver_name_lower or 'wifi' in driver_name_lower:
        return 'Wireless'
    elif 'graphics' in driver_name_lower or 'display' in driver_name_lower or 'video' in driver_name_lower or 'radeon' in driver_name_lower or 'geforce' in driver_name_lower:
        return 'Graphics'
    elif 'chipset' in driver_name_lower:
        return 'Chipset'
    elif 'storage' in driver_name_lower or 'disk' in driver_name_lower or 'nvme' in driver_name_lower or 'sata' in driver_name_lower:
        return 'Storage'
    elif 'usb' in driver_name_lower:
        return 'USB'
    elif 'bluetooth' in driver_name_lower:
        return 'Bluetooth'
    elif 'management engine' in driver_name_lower or 'mei' in driver_name_lower:
        return 'Management Engine'
    
    # Check device ID patterns
    if device_id:
        device_id_upper = device_id.upper()
        for pattern, device_type in DEVICE_TYPE_PATTERNS.items():
            if pattern in device_id_upper:
                return device_type
    
    return 'Other'


def generate_filename(vendor_name: str, driver_name: str, device_type: str, version: str) -> str:
    """
    Generate a suggested filename for the driver
    
    Args:
        vendor_name: Vendor/manufacturer name
        driver_name: Driver name
        device_type: Type of device
        version: Driver version
        
    Returns:
        Suggested filename
    """
    # Clean up vendor name
    vendor_clean = vendor_name.replace(' Corporation', '').replace(' Semiconductor', '').replace(' Technology', '')
    vendor_clean = vendor_clean.replace('/', '-').replace(' ', '_')
    
    # Use device type if driver name is too generic
    if len(driver_name) > 50 or 'device' in driver_name.lower():
        base_name = f"{vendor_clean}_{device_type}"
    else:
        # Clean up driver name
        driver_clean = driver_name.replace('(R)', '').replace('(TM)', '').strip()
        driver_clean = driver_clean.replace(' ', '_').replace('/', '-')
        # Limit length
        if len(driver_clean) > 40:
            driver_clean = driver_clean[:40]
        base_name = driver_clean
    
    # Add version if available
    if version and version != 'unknown':
        version_clean = version.replace('.', '_')
        filename = f"{base_name}_v{version_clean}.exe"
    else:
        filename = f"{base_name}.exe"
    
    return filename
