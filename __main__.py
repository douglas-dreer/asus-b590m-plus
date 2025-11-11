#!/usr/bin/env python3
"""
Alternative entry point for running as a module
Usage: python __main__.py
"""

import sys
import logging
from pathlib import Path

from utils.logging_config import setup_logging, log_system_info

logger = logging.getLogger(__name__)


def main():
    """Main entry point for the driver installer"""
    # Setup logging with default configuration
    setup_logging(log_file='setup-drivers.log', verbose=False)
    
    # Log system information
    log_system_info()
    
    # TODO: Implement main logic in subsequent tasks
    logger.info("Project structure initialized successfully")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
