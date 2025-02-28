# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.2] - 2025-02-28

### Added
- Post-installation welcome message with quick start guide
- Automatic display of helpful commands when package is first imported
- Improved onboarding experience for new users
- Demo mode that works without API keys (`--demo` flag)
- Mock test functionality for demonstrations and training

### Changed
- Updated setup.py with custom installation command 
- Enhanced package import process to guide new users
- Improved test result display with color-coded panels
- Better error messages with troubleshooting advice

## [1.0.0] - 2023-10-29

### Added
- Case Management System
  - Tracking of multiple tests
  - Organization of tests by client/use case
  - Structured directory for test results
  - Both human-readable and machine-readable result files
- Enhanced CLI Wizard
  - Interactive testing interface
  - Improved image testing
  - API key configuration
  - Advanced diagnostic capabilities

### Changed
- Simplified default user experience
- Made case management optional for regular users
- Provided advanced case management for power users via CLI flags
- Updated documentation with comprehensive installation and usage guides
- Improved error handling and validation

### Fixed
- Various bug fixes and stability improvements
- Enhanced error messages
- Cross-platform compatibility improvements

## [0.1.0] - 2023-10-15

### Added
- Initial release
- Basic API connectivity tests
- Simple image upload functionality
- DNS and network diagnostics
- Basic CLI interface
