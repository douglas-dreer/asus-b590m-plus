#!/usr/bin/env python3
"""
Driver Detection CLI Tool
Utility to detect and list drivers for installation
"""

import sys
import argparse
import logging
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

logger = logging.getLogger(__name__)


def main():
    """Main entry point for driver detection tool"""
    parser = argparse.ArgumentParser(
        description='Driver Detection Tool - Detect and list drivers for installation'
    )
    
    parser.add_argument(
        '--manifest',
        type=str,
        default='drivers-example.json',
        help='Path to drivers manifest JSON file (default: drivers-example.json)'
    )
    
    parser.add_argument(
        '--action',
        type=str,
        choices=['available', 'installed', 'not-installed', 'different-versions', 'needing-update'],
        default='needing-update',
        help='Action to perform (default: needing-update)'
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
    
    # Setup logging
    setup_logging(log_file='detect-drivers.log', verbose=args.verbose)
    
    logger.info("=" * 60)
    logger.info("Driver Detection Tool - Starting")
    logger.info("=" * 60)
    logger.info(f"Manifest: {args.manifest}")
    logger.info(f"Action: {args.action}")
    logger.info(f"OS Filter: {args.os_filter or 'None'}")
    
    # Check if manifest exists
    if not Path(args.manifest).exists():
        logger.error(f"Manifest file not found: {args.manifest}")
        print(f"Error: Manifest file not found: {args.manifest}")
        return 1
    
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
