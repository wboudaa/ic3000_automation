# Changelog

All notable changes to the IC3000 Automation Toolkit will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-12-19

### Added
- Initial release of IC3000 Automation Toolkit
- NTP configuration automation with REST API integration
- Support for single and multiple NTP servers (comma-separated)
- Firmware upgrade automation with file upload and installation
- Batch processing to prevent network overload
- Parallel execution using thread pools
- CSV-based device inventory management
- YAML configuration file for centralized settings
- Comprehensive error handling and retry logic
- Detailed console output with progress tracking
- CSV reporting with timestamps for audit trails
- Command-line interface with multiple options:
  - `--test` mode for safe testing on 2 devices
  - `--batch-size` for controlling parallel batches
  - `--batch-delay` for spacing out batches
  - `--workers` for controlling thread pool size
  - `--limit` for processing subset of devices
  - `--yes` for skipping confirmation prompts
- Secure authentication flow via X-IDA-AUTH-TOKEN
- SSL certificate handling for self-signed certificates
- Complete documentation:
  - README.md with comprehensive guide
  - QUICKSTART.md for quick setup
  - GITLAB_SETUP.md for repository management
- Example configuration files and templates
- .gitignore for protecting sensitive data

### Security
- Credentials stored in CSV file (excluded from git)
- Configuration file excluded from git by default
- Example files provided without sensitive data
- File permission recommendations for credential protection

### Technical Details
- REST API endpoints discovered and documented:
  - Port 8443: Authentication and token service
  - Port 8444: NTP configuration and firmware upload
- Three-step authentication process implemented:
  1. Login to web UI on port 8443
  2. Request API token from token service
  3. Use token for all API operations
- Graceful timeout handling for device reboots during upgrades
- Multi-server NTP configuration support
- Device name extraction from CSV (DeviceName or Hostname)

## [Unreleased]

### Planned Features
- Config backup before making changes
- Rollback capability for failed upgrades
- Email notifications on completion/errors
- Webhook integration for monitoring systems
- Support for additional IC3000 API endpoints
- Progress bar for large operations
- Dry-run mode to preview changes
- Scheduling support for automated runs

### Known Issues
- None currently reported

---

## Version History

- **v1.0.0** (2025-12-19): Initial release



