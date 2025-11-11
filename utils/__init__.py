"""
Utility module for common helper functions
"""

__version__ = "1.0.0"

# Download utilities
from utils.download import (
    download_file,
    download_with_progress_bar
)

# File utilities
from utils.file_utils import (
    ensure_directory,
    file_exists,
    get_file_size,
    cleanup_temp_files
)

# Logging utilities
from utils.logging_config import (
    setup_logging,
    log_system_info,
    log_summary
)

__all__ = [
    # Download
    'download_file',
    'download_with_progress_bar',
    # File utilities
    'ensure_directory',
    'file_exists',
    'get_file_size',
    'cleanup_temp_files',
    # Logging
    'setup_logging',
    'log_system_info',
    'log_summary',
]
