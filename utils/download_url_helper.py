"""
Download URL Helper - Assists in finding and constructing driver download URLs
"""

import json
import logging
from pathlib import Path
from typing import Optional, Dict, List

logger = logging.getLogger(__name__)


# Cache for loaded patterns to avoid reloading
_patterns_cache = None

def load_vendor_patterns(patterns_file: str = None) -> Optional[Dict]:
    """
    Load vendor download patterns from JSON file (cached)
    
    Args:
        patterns_file: Path to the vendor patterns JSON file (default: utils/vendor_download_patterns.json)
        
    Returns:
        Dictionary with vendor patterns or None if loading fails
    """
    global _patterns_cache
    
    # Return cached data if available
    if _patterns_cache is not None:
        return _patterns_cache
    
    try:
        # Default to utils directory
        if patterns_file is None:
            # Get the directory where this script is located
            script_dir = Path(__file__).parent
            patterns_file = script_dir / 'vendor_download_patterns.json'
        
        patterns_path = Path(patterns_file)
        if not patterns_path.exists():
            logger.error(f"Vendor patterns file not found: {patterns_file}")
            return None
            
        with open(patterns_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Cache the loaded data
        _patterns_cache = data
        logger.info(f"Loaded patterns for {len(data.get('vendors', []))} vendors")
        return data
        
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse vendor patterns JSON: {e}")
        return None
    except Exception as e:
        logger.error(f"Error loading vendor patterns: {e}")
        return None


def get_vendor_pattern(vendor_name: str, device_type: str = None) -> Optional[Dict]:
    """
    Get download pattern for a specific vendor and device type
    
    Args:
        vendor_name: Name of the vendor (e.g., "Intel", "AMD")
        device_type: Type of device (e.g., "graphics", "network")
        
    Returns:
        Dictionary with pattern information or None if not found
    """
    patterns_data = load_vendor_patterns()
    if not patterns_data:
        return None
    
    # Find vendor (flexible matching - check if vendor name contains pattern name)
    vendor_name_lower = vendor_name.lower()
    for vendor in patterns_data.get('vendors', []):
        vendor_pattern_name = vendor['name'].lower()
        
        # Match if exact or if vendor_name contains the pattern name
        if vendor_pattern_name == vendor_name_lower or vendor_pattern_name in vendor_name_lower:
            if device_type:
                # Return specific device type pattern
                device_patterns = vendor.get('patterns', {})
                for dtype, pattern in device_patterns.items():
                    if dtype.lower() == device_type.lower():
                        return {
                            'vendor': vendor['name'],
                            'device_type': dtype,
                            'website': vendor['website'],
                            **pattern
                        }
            else:
                # Return all patterns for vendor
                return {
                    'vendor': vendor['name'],
                    'website': vendor['website'],
                    'patterns': vendor.get('patterns', {})
                }
    
    return None


def suggest_download_url(vendor_name: str, device_type: str, driver_name: str = None) -> Dict:
    """
    Suggest download URL and search page for a driver
    
    Args:
        vendor_name: Name of the vendor
        device_type: Type of device
        driver_name: Optional driver name for more specific suggestions
        
    Returns:
        Dictionary with suggestions
    """
    pattern = get_vendor_pattern(vendor_name, device_type)
    
    if not pattern:
        return {
            'found': False,
            'message': f"No pattern found for {vendor_name} {device_type}",
            'search_page': None,
            'download_pattern': None
        }
    
    return {
        'found': True,
        'vendor': pattern['vendor'],
        'device_type': pattern['device_type'],
        'search_page': pattern.get('search_page'),
        'download_pattern': pattern.get('direct_download_pattern'),
        'example': pattern.get('example'),
        'notes': pattern.get('notes'),
        'message': f"Found pattern for {vendor_name} {device_type}"
    }


def list_all_vendors() -> List[str]:
    """
    List all vendors in the patterns database
    
    Returns:
        List of vendor names
    """
    patterns_data = load_vendor_patterns()
    if not patterns_data:
        return []
    
    return [vendor['name'] for vendor in patterns_data.get('vendors', [])]


def list_vendor_device_types(vendor_name: str) -> List[str]:
    """
    List all device types available for a vendor
    
    Args:
        vendor_name: Name of the vendor
        
    Returns:
        List of device type names
    """
    pattern = get_vendor_pattern(vendor_name)
    if not pattern or 'patterns' not in pattern:
        return []
    
    return list(pattern['patterns'].keys())


def print_vendor_info(vendor_name: str):
    """
    Print detailed information about a vendor's download patterns
    
    Args:
        vendor_name: Name of the vendor
    """
    pattern = get_vendor_pattern(vendor_name)
    
    if not pattern:
        print(f"No information found for vendor: {vendor_name}")
        return
    
    print(f"\n{'='*60}")
    print(f"Vendor: {pattern['vendor']}")
    print(f"{'='*60}")
    print(f"Website: {pattern['website']}")
    print()
    
    if 'patterns' in pattern:
        print("Available Device Types:")
        for device_type, info in pattern['patterns'].items():
            print(f"\n  {device_type.upper()}:")
            print(f"    Search Page: {info.get('search_page', 'N/A')}")
            print(f"    Pattern: {info.get('direct_download_pattern', 'N/A')}")
            print(f"    Example: {info.get('example', 'N/A')}")
            if info.get('notes'):
                print(f"    Notes: {info['notes']}")
    print()


def generate_download_suggestions_report(drivers: List[Dict], output_file: str = 'download_suggestions.txt'):
    """
    Generate a report with download suggestions for a list of drivers
    
    Args:
        drivers: List of driver dictionaries
        output_file: Path to output report file
    """
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("="*80 + "\n")
            f.write("DRIVER DOWNLOAD SUGGESTIONS REPORT\n")
            f.write("="*80 + "\n\n")
            
            for i, driver in enumerate(drivers, 1):
                vendor = driver.get('manufacturer', 'Unknown')
                device_type = driver.get('deviceType', 'Other').lower()
                name = driver.get('name', 'Unknown Driver')
                
                f.write(f"{i}. {name}\n")
                f.write(f"   Vendor: {vendor}\n")
                f.write(f"   Device Type: {device_type}\n")
                
                suggestion = suggest_download_url(vendor, device_type, name)
                
                if suggestion['found']:
                    f.write(f"   Search Page: {suggestion['search_page']}\n")
                    if suggestion.get('example'):
                        f.write(f"   Example URL: {suggestion['example']}\n")
                    if suggestion.get('notes'):
                        f.write(f"   Notes: {suggestion['notes']}\n")
                else:
                    f.write(f"   Status: No pattern available - manual search required\n")
                    f.write(f"   Suggestion: Visit vendor website and search for driver\n")
                
                f.write("\n" + "-"*80 + "\n\n")
            
            f.write("\n" + "="*80 + "\n")
            f.write("END OF REPORT\n")
            f.write("="*80 + "\n")
        
        logger.info(f"Download suggestions report generated: {output_file}")
        print(f"Report generated: {output_file}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to generate report: {e}")
        print(f"Error generating report: {e}")
        return False


if __name__ == "__main__":
    # Example usage
    print("Vendor Download URL Helper")
    print("="*60)
    
    # List all vendors
    print("\nAvailable Vendors:")
    vendors = list_all_vendors()
    for vendor in vendors:
        print(f"  - {vendor}")
    
    # Show example for Intel
    print("\n" + "="*60)
    print_vendor_info("Intel")
    
    # Show example for AMD
    print_vendor_info("AMD")
    
    # Test suggestion
    print("="*60)
    print("\nExample: Suggesting URL for Intel Graphics driver")
    suggestion = suggest_download_url("Intel", "graphics")
    if suggestion['found']:
        print(f"Search Page: {suggestion['search_page']}")
        print(f"Pattern: {suggestion['download_pattern']}")
        print(f"Example: {suggestion['example']}")
