"""
Installer module for handling driver installations across different platforms
"""

__version__ = "1.0.0"

# Core functionality
from installer.core import (
    detect_os,
    install_driver,
    create_manual_note
)

# Windows-specific installers
from installer.windows import (
    install_exe,
    install_msi,
    install_zip
)

# Linux-specific installers
from installer.linux import (
    install_deb,
    install_rpm,
    detect_distribution
)

__all__ = [
    # Core
    'detect_os',
    'install_driver',
    'create_manual_note',
    # Windows
    'install_exe',
    'install_msi',
    'install_zip',
    # Linux
    'install_deb',
    'install_rpm',
    'detect_distribution',
]
