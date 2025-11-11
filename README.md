# Silent Driver Installer

Universal Python script for automated driver installation on Windows and Linux systems.

## Overview

This tool automates the process of downloading, validating, and installing device drivers from a JSON manifest. It supports multiple installer formats (exe, msi, zip, deb, rpm) and provides detailed logging of all operations.

## Features

- **Cross-platform**: Works on Windows and Linux
- **Automated downloads**: Downloads drivers from URLs specified in manifest
- **SHA256 validation**: Verifies file integrity before installation
- **Silent installation**: Installs drivers without user interaction
- **Retry logic**: Automatic retry with exponential backoff for failed downloads
- **Detailed logging**: Comprehensive logs for auditing and troubleshooting
- **Single reboot**: Minimizes downtime by rebooting only once after all installations

## Requirements

- Python 3.7 or higher
- Administrator/root privileges
- Internet connection

## Installation

1. Clone or download this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Basic Usage

```bash
# Run with default settings
python setup-drivers.py

# Or as a module
python -m driver_installer
```

### Command Line Options

```bash
python setup-drivers.py [OPTIONS]

Options:
  --manifest PATH       Path to drivers.json manifest file (default: ./downloads/drivers.json)
  --auto-reboot        Automatically reboot after installation
  --force              Force re-download of existing files
  --dry-run            Simulate installation without executing
  --verbose            Enable verbose logging
```

### Examples

```bash
# Install drivers with automatic reboot
python setup-drivers.py --auto-reboot

# Force re-download all drivers
python setup-drivers.py --force

# Use custom manifest
python setup-drivers.py --manifest /path/to/custom-drivers.json

# Dry run to see what would be installed
python setup-drivers.py --dry-run --verbose
```

## Manifest Format

The `drivers.json` manifest file defines which drivers to install:

```json
[
  {
    "name": "Intel Chipset Driver",
    "url": "https://example.com/driver.exe",
    "fileName": "driver.exe",
    "sha256": "ABC123...",
    "type": "exe",
    "silentArgs": "/S"
  }
]
```

### Manifest Fields

- **name** (required): Descriptive name for logging
- **url** (required): Download URL
- **fileName** (required): Local filename to save as
- **sha256** (optional): SHA256 hash for validation
- **type** (required): Installer type (`exe`, `msi`, `zip`, `deb`, `rpm`, `manual`)
- **silentArgs** (optional): Custom silent installation arguments

## Project Structure

```
.
├── setup-drivers.py          # Main entry point
├── __main__.py               # Module entry point
├── requirements.txt          # Python dependencies
├── installer/                # Installation modules
├── utils/                    # Utility functions
├── validators/               # Validation modules
├── downloads/                # Manifest files
│   └── drivers.json
└── downloads_work/           # Downloaded files (auto-created)
```

## Logging

All operations are logged to:
- Console (stdout)
- `setup-drivers.log` file

Log format: `[YYYY-MM-DDTHH:MM:SS] LEVEL: Message`

## Security

- Always verify SHA256 hashes in production
- Use HTTPS URLs from official sources only
- Review manifest before execution
- Run with appropriate privileges only when necessary

## Troubleshooting

### "Permission denied" errors
Run with administrator/root privileges:
- Windows: Run PowerShell as Administrator
- Linux: Use `sudo python setup-drivers.py`

### Download failures
- Check internet connection
- Verify URLs are accessible
- Check firewall settings
- Use `--force` to retry downloads

### Installation failures
- Check log file for detailed error messages
- Verify installer type matches file format
- Try manual installation to test installer

## License

See LICENSE file for details.

## Contributing

Contributions are welcome! Please ensure:
- Code follows PEP 8 style guidelines
- All functions have docstrings
- Tests pass before submitting
- Commit messages are descriptive

## Changelog

### Version 1.0.0 (Initial Release)
- Cross-platform Python implementation
- Support for multiple installer formats
- SHA256 validation
- Retry logic with exponential backoff
- Comprehensive logging
- Single reboot optimization
