"""
Logging configuration utilities
"""

import logging
import sys
from pathlib import Path
from datetime import datetime


def setup_logging(log_file: str = 'setup-drivers.log', verbose: bool = False) -> None:
    """
    Configure logging for the application
    
    Args:
        log_file: Path to log file
        verbose: Enable verbose (DEBUG) logging
    """
    # Determine log level
    log_level = logging.DEBUG if verbose else logging.INFO
    
    # Create formatters
    file_formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s - %(name)s - %(message)s',
        datefmt='%Y-%m-%dT%H:%M:%S'
    )
    
    console_formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s - %(message)s',
        datefmt='%Y-%m-%dT%H:%M:%S'
    )
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # Remove existing handlers
    root_logger.handlers.clear()
    
    # File handler
    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    
    file_handler = logging.FileHandler(log_file, mode='a', encoding='utf-8')
    file_handler.setLevel(log_level)
    file_handler.setFormatter(file_formatter)
    root_logger.addHandler(file_handler)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)
    
    # Log startup message
    logging.info("=" * 70)
    logging.info(f"Driver Installation Script Started - {datetime.now().isoformat()}")
    logging.info("=" * 70)


def log_system_info() -> None:
    """Log system information"""
    import platform
    import sys
    
    logger = logging.getLogger(__name__)
    
    logger.info("System Information:")
    logger.info(f"  OS: {platform.system()} {platform.release()}")
    logger.info(f"  Platform: {platform.platform()}")
    logger.info(f"  Python: {sys.version}")
    logger.info(f"  Architecture: {platform.machine()}")


def log_summary(total: int, successful: int, failed: int) -> None:
    """
    Log installation summary
    
    Args:
        total: Total number of drivers processed
        successful: Number of successful installations
        failed: Number of failed installations
    """
    logger = logging.getLogger(__name__)
    
    logger.info("=" * 70)
    logger.info("Installation Summary:")
    logger.info(f"  Total drivers: {total}")
    logger.info(f"  Successful: {successful}")
    logger.info(f"  Failed: {failed}")
    logger.info(f"  Success rate: {(successful/total*100) if total > 0 else 0:.1f}%")
    logger.info("=" * 70)
