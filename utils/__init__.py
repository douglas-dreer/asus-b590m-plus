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

# Initialization and validation utilities
from utils.init_validator import (
    check_python_version,
    check_dependencies,
    detect_os,
    check_admin_privileges,
    create_argument_parser,
    validate_environment
)

# Driver detection utilities
from utils.driver_detector import (
    load_drivers_manifest,
    list_available_drivers,
    list_installed_drivers,
    list_not_installed_drivers,
    list_drivers_with_different_versions,
    list_drivers_needing_update,
    export_driver_list
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
    # Initialization and validation
    'check_python_version',
    'check_dependencies',
    'detect_os',
    'check_admin_privileges',
    'create_argument_parser',
    'validate_environment',
    # Driver detection
    'load_drivers_manifest',
    'list_available_drivers',
    'list_installed_drivers',
    'list_not_installed_drivers',
    'list_drivers_with_different_versions',
    'list_drivers_needing_update',
    'export_driver_list',
]
