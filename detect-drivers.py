#!/usr/bin/env python3
"""
Driver Detection CLI Tool
Utility to detect and list drivers for installation
"""

import sys
import argparse
import logging
import json
from pathlib import Path

from utils.logging_config import setup_logging
from utils.driver_detector import (
    list_available_drivers,
    list_installed_drivers,
    list_not_installed_drivers,
    list_drivers_with_different_versions,
    list_drivers_needing_update,
    export_driver_list
)
from utils.vendor_database import (
    get_vendor_info,
    is_generic_windows_driver,
    detect_device_type,
    generate_filename
)
from utils.download_url_helper import suggest_download_url

logger = logging.getLogger(__name__)


def main():
    """Main entry point for driver detection tool"""
    parser = argparse.ArgumentParser(
        description='Driver Detection Tool - Detect and list drivers for installation'
    )
    
    parser.add_argument(
        '--manifest',
        type=str,
        default=None,
        help='Path to drivers manifest JSON file (required for scan action)'
    )
    
    parser.add_argument(
        '--action',
        type=str,
        choices=['available', 'installed', 'not-installed', 'different-versions', 'needing-update', 'scan', 'create'],
        default='needing-update',
        help='Action to perform. Use "create" to generate new manifest from installed drivers, "scan" to find missing drivers'
    )
    
    parser.add_argument(
        '--os-filter',
        type=str,
        choices=['windows', 'linux'],
        help='Filter drivers by operating system'
    )
    
    parser.add_argument(
        '--export',
        type=str,
        help='Export results to JSON file at specified path'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    # Setup logging in logs directory
    setup_logging(log_file='logs/detect-drivers.log', verbose=args.verbose)
    
    logger.info("=" * 60)
    logger.info("Driver Detection Tool - Starting")
    logger.info("=" * 60)
    logger.info(f"Action: {args.action}")
    if args.manifest:
        logger.info(f"Manifest: {args.manifest}")
    logger.info(f"OS Filter: {args.os_filter or 'None'}")
    
    # Execute requested action
    results = []
    
    try:
        if args.action == 'available':
            logger.info("Listing available drivers from manifest...")
            results = list_available_drivers(args.manifest, args.os_filter)
            print(f"\n{'='*60}")
            print(f"Available Drivers: {len(results)}")
            print(f"{'='*60}")
            for driver in results:
                print(f"  - {driver.get('name')} (v{driver.get('version', 'unknown')})")
                print(f"    OS: {driver.get('os', 'unknown')}, Type: {driver.get('type', 'unknown')}")
                print(f"    Device ID: {driver.get('deviceId', 'N/A')}")
                print()
        
        elif args.action == 'installed':
            logger.info("Listing installed drivers...")
            results = list_installed_drivers()
            print(f"\n{'='*60}")
            print(f"Installed Drivers: {len(results)}")
            print(f"{'='*60}")
            for driver in results:
                print(f"  - {driver.get('name')} (v{driver.get('version', 'unknown')})")
                print(f"    Device ID: {driver.get('deviceId', 'N/A')}")
                print()
        
        elif args.action == 'not-installed':
            logger.info("Listing drivers not installed...")
            results = list_not_installed_drivers(args.manifest, args.os_filter)
            print(f"\n{'='*60}")
            print(f"Drivers Not Installed: {len(results)}")
            print(f"{'='*60}")
            for driver in results:
                print(f"  - {driver.get('name')} (v{driver.get('version', 'unknown')})")
                print(f"    OS: {driver.get('os', 'unknown')}, Type: {driver.get('type', 'unknown')}")
                print(f"    URL: {driver.get('url', 'N/A')}")
                print()
        
        elif args.action == 'different-versions':
            logger.info("Listing drivers with different versions...")
            version_diffs = list_drivers_with_different_versions(args.manifest, args.os_filter)
            print(f"\n{'='*60}")
            print(f"Drivers with Different Versions: {len(version_diffs)}")
            print(f"{'='*60}")
            for available, installed in version_diffs:
                print(f"  - {available.get('name')}")
                print(f"    Available: v{available.get('version', 'unknown')}")
                print(f"    Installed: v{installed.get('version', 'unknown')}")
                print(f"    URL: {available.get('url', 'N/A')}")
                print()
            # For export, convert to list of dicts
            results = [
                {
                    **available,
                    'installed_version': installed.get('version', 'unknown')
                }
                for available, installed in version_diffs
            ]
        
        elif args.action == 'needing-update':
            logger.info("Listing drivers needing installation or update...")
            results = list_drivers_needing_update(args.manifest, args.os_filter)
            print(f"\n{'='*60}")
            print(f"Drivers Needing Installation/Update: {len(results)}")
            print(f"{'='*60}")
            for driver in results:
                current_ver = driver.get('current_version')
                if current_ver:
                    print(f"  - {driver.get('name')} (UPDATE)")
                    print(f"    Current: v{current_ver}")
                    print(f"    Available: v{driver.get('version', 'unknown')}")
                else:
                    print(f"  - {driver.get('name')} (NEW)")
                    print(f"    Version: v{driver.get('version', 'unknown')}")
                print(f"    OS: {driver.get('os', 'unknown')}, Type: {driver.get('type', 'unknown')}")
                print(f"    URL: {driver.get('url', 'N/A')}")
                print()
        
        elif args.action == 'create':
            logger.info("Creating new manifest from installed drivers...")
            
            # Get currently installed drivers
            installed_drivers = list_installed_drivers()
            logger.info(f"Found {len(installed_drivers)} installed drivers")
            
            # Process installed drivers and enhance with patterns
            export_path = args.export or 'drivers.json'
            results = []
            seen_drivers = {}  # Track duplicates
            skipped_count = 0
            
            for driver in installed_drivers:
                driver_name = driver.get('name', 'Unknown Driver')
                device_id = driver.get('deviceId', '')
                version = driver.get('version', 'unknown')
                
                # Skip generic Windows drivers
                if is_generic_windows_driver(driver_name):
                    skipped_count += 1
                    logger.debug(f"Skipping generic Windows driver: {driver_name}")
                    continue
                
                # Skip duplicates
                duplicate_key = device_id if device_id else f"{driver_name}_{version}"
                if duplicate_key in seen_drivers:
                    skipped_count += 1
                    logger.debug(f"Skipping duplicate: {driver_name}")
                    continue
                
                seen_drivers[duplicate_key] = True
                
                # Get vendor information
                vendor_info = get_vendor_info(device_id)
                vendor_name = vendor_info['name'] if vendor_info else 'Unknown Manufacturer'
                vendor_website = vendor_info['website'] if vendor_info else ''
                
                # Detect device type
                device_type = detect_device_type(driver_name, device_id)
                
                # Get download URL suggestion from patterns
                url_suggestion = suggest_download_url(vendor_name, device_type.lower())
                suggested_url = ''
                suggested_notes = ''
                download_example = ''
                
                if url_suggestion and url_suggestion.get('found'):
                    # Use example URL as template (direct download link)
                    download_example = url_suggestion.get('example', '')
                    suggested_url = download_example if download_example else vendor_website
                    
                    if url_suggestion.get('notes'):
                        suggested_notes = url_suggestion['notes']
                    logger.debug(f"Found download pattern for {vendor_name} {device_type}")
                else:
                    # Fallback to vendor website
                    suggested_url = vendor_website
                    logger.debug(f"No download pattern for {vendor_name} {device_type}")
                
                # Use data from reference manifest if available, enhance with patterns
                suggested_filename = generate_filename(vendor_name, driver_name, device_type, version)
                
                manifest_entry = {
                    'name': driver_name,
                    'manufacturer': vendor_name,
                    'deviceType': device_type,
                    'version': version,
                    'deviceId': device_id,
                    'url': driver.get('url', suggested_url),  # Use manifest URL or suggested
                    'fileName': driver.get('fileName', suggested_filename),
                    'sha256': driver.get('sha256', ''),
                    'type': driver.get('type', 'exe'),
                    'os': driver.get('os', 'windows' if sys.platform == 'win32' else 'linux'),
                    'silentArgs': driver.get('silentArgs', '/S /v"/qn"')
                }
                
                # Add notes if available from patterns
                if suggested_notes and not driver.get('notes'):
                    manifest_entry['notes'] = suggested_notes
                
                results.append(manifest_entry)
            
            print(f"\n{'='*60}")
            print(f"Detected Drivers: {len(results)}")
            print(f"{'='*60}")
            print(f"System scan complete.")
            print(f"  - Found {len(installed_drivers)} total drivers")
            print(f"  - Skipped {skipped_count} (generic/duplicate drivers)")
            print(f"  - Included {len(results)} unique hardware drivers")
            print()
            
            # Group drivers by manufacturer
            drivers_by_manufacturer = {}
            for driver in results:
                mfr = driver.get('manufacturer', 'Unknown Manufacturer')
                if mfr not in drivers_by_manufacturer:
                    drivers_by_manufacturer[mfr] = []
                drivers_by_manufacturer[mfr].append(driver)
            
            print("Drivers by Manufacturer:")
            for mfr in sorted(drivers_by_manufacturer.keys()):
                count = len(drivers_by_manufacturer[mfr])
                print(f"  - {mfr}: {count} driver(s)")
            print()
            
            # Create grouped structure
            grouped_results = {
                'manufacturers': []
            }
            
            for mfr in sorted(drivers_by_manufacturer.keys()):
                grouped_results['manufacturers'].append({
                    'name': mfr,
                    'drivers': drivers_by_manufacturer[mfr]
                })
            
            # Also keep flat structure for compatibility
            results = grouped_results
            
            print("Generated manifest includes:")
            print("  [+] Manufacturer names")
            print("  [+] Direct download URLs (where available)")
            print("  [+] Auto-generated filenames")
            print("  [+] Device types")
            print("  [+] Duplicates removed")
            print()
            print("Next steps:")
            print("  1. Review and update URLs/versions as needed")
            print("  2. Use this as reference: python detect-drivers.py --action scan --manifest drivers.json")
            print()
            
            # Export grouped structure
            logger.info(f"Exporting detected drivers to: {export_path}")
            
            try:
                output_file = Path(export_path)
                output_file.parent.mkdir(parents=True, exist_ok=True)
                
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(results, f, indent=2, ensure_ascii=False)
                
                logger.info(f"Exported drivers grouped by manufacturer to: {export_path}")
                print(f"\n[OK] Drivers manifest created: {export_path}")
                print(f"\nThis file contains all detected hardware drivers.")
                print(f"Use as reference for future scans!")
                
            except Exception as e:
                logger.error(f"Failed to export drivers: {e}")
                print(f"[ERROR] Failed to create drivers manifest: {e}")
                return 1
        
        elif args.action == 'scan':
            logger.info("Scanning for missing drivers...")
            
            # Check if manifest is provided
            if not args.manifest:
                logger.error("Manifest file required for scan action")
                print("\nError: --manifest parameter is required for scan action")
                print("Example: python detect-drivers.py --action scan --manifest drivers.json")
                return 1
            
            # Check if manifest exists
            if not Path(args.manifest).exists():
                logger.error(f"Manifest file not found: {args.manifest}")
                print(f"\nError: Manifest file not found: {args.manifest}")
                print("Please provide a reference manifest with --manifest option")
                return 1
            
            # Load reference manifest
            reference_drivers = list_available_drivers(args.manifest, args.os_filter)
            if not reference_drivers:
                logger.error("Failed to load reference drivers from manifest")
                print("Error: Could not load drivers from manifest")
                return 1
            
            logger.info(f"Loaded {len(reference_drivers)} reference drivers from manifest")
            
            # Get currently installed drivers
            installed_drivers = list_installed_drivers()
            logger.info(f"Found {len(installed_drivers)} installed drivers")
            
            # Find drivers that are NOT installed (missing drivers)
            missing_drivers = list_not_installed_drivers(args.manifest, args.os_filter)
            logger.info(f"Found {len(missing_drivers)} missing drivers")
            
            # Process missing drivers
            export_path = args.export or 'drivers-missing.json'
            results = []
            seen_drivers = {}
            
            for driver in missing_drivers:
                driver_name = driver.get('name', 'Unknown Driver')
                device_id = driver.get('deviceId', '')
                
                # Skip duplicates
                duplicate_key = device_id if device_id else driver_name
                if duplicate_key in seen_drivers:
                    continue
                seen_drivers[duplicate_key] = True
                
                # Keep driver as-is from manifest (already has URLs, etc.)
                results.append(driver)
            
            print(f"\n{'='*60}")
            print(f"Missing Drivers: {len(results)}")
            print(f"{'='*60}")
            print(f"Scan complete.")
            print(f"  - Reference manifest: {len(reference_drivers)} drivers")
            print(f"  - Currently installed: {len(installed_drivers)} drivers")
            print(f"  - Missing (not installed): {len(results)} drivers")
            print()
            
            if len(results) == 0:
                print("All drivers from manifest are already installed!")
                print("No action needed.")
            else:
                # Group by manufacturer
                drivers_by_manufacturer = {}
                for driver in results:
                    mfr = driver.get('manufacturer', driver.get('name', 'Unknown'))
                    if mfr not in drivers_by_manufacturer:
                        drivers_by_manufacturer[mfr] = []
                    drivers_by_manufacturer[mfr].append(driver)
                
                print("Missing drivers by manufacturer:")
                for mfr in sorted(drivers_by_manufacturer.keys()):
                    count = len(drivers_by_manufacturer[mfr])
                    print(f"  - {mfr}: {count} driver(s)")
                print()
                
                print("Ready for installation:")
                print("  [+] Direct download URLs")
                print("  [+] Installation parameters")
                print("  [+] Ready for automated install")
                print()
                print("Next steps:")
                print(f"  1. python setup-drivers.py --manifest {export_path} --auto-reboot")
            print()
            
            # Export missing drivers
            if results:
                try:
                    output_file = Path(export_path)
                    output_file.parent.mkdir(parents=True, exist_ok=True)
                    
                    # Group by manufacturer
                    grouped_results = {'manufacturers': []}
                    for mfr in sorted(drivers_by_manufacturer.keys()):
                        grouped_results['manufacturers'].append({
                            'name': mfr,
                            'drivers': drivers_by_manufacturer[mfr]
                        })
                    
                    with open(output_file, 'w', encoding='utf-8') as f:
                        json.dump(grouped_results, f, indent=2, ensure_ascii=False)
                    
                    logger.info(f"Exported missing drivers to: {export_path}")
                    print(f"[OK] Missing drivers manifest created: {export_path}")
                    print(f"This file contains only drivers NOT currently installed.")
                    
                except Exception as e:
                    logger.error(f"Failed to export drivers: {e}")
                    print(f"[ERROR] Failed to create manifest: {e}")
                    return 1
        
        # Export if requested
        if args.export and results:
            logger.info(f"Exporting results to: {args.export}")
            if export_driver_list(results, args.export):
                print(f"\nResults exported to: {args.export}")
            else:
                print(f"\nFailed to export results to: {args.export}")
                return 1
        
        logger.info("Driver detection completed successfully")
        return 0
        
    except Exception as e:
        logger.error(f"Error during driver detection: {e}", exc_info=True)
        print(f"\nError: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
