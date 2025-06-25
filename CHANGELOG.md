# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Planned: Volume management support
- Planned: Network management support
- Planned: Load balancer integration
- Planned: Firewall management
- Planned: Floating IP management

## [1.2.0] - 2025-06-26

### 🚀 Professional PyPI Release
- Successfully published to PyPI as `pyhetznerserver`
- Package available for installation via `pip install pyhetznerserver`
- Complete professional package structure with standard Python layout
- All quality checks passed (twine check, pytest, imports)
- Professional documentation and metadata
- Ready for production use

### 🔧 Technical Improvements
- Optimized package build process
- Verified compatibility across Python 3.7-3.12
- Clean imports and proper module exports
- Professional setuptools configuration

## [1.0.0] - 2024-06-26

### Added
- Initial release of PyHetznerServer
- Complete Hetzner Cloud Server API coverage
- Server lifecycle management (create, delete, update)
- Power management operations (power on/off, reboot, reset, shutdown)
- Image and snapshot management
- Backup system integration
- Rescue mode support
- ISO attachment/detachment
- Network operations (attach/detach from networks)
- DNS PTR record management
- Server protection settings
- Type-safe Python models with full type hints
- Comprehensive error handling with custom exceptions
- Dry-run mode for testing without API calls
- Automatic JSON to Python object conversion
- Rate limiting awareness
- Pagination support
- Label-based filtering
- Server action history and status tracking

### Features
- **HetznerClient**: Main client class with authentication and request handling
- **Server**: Complete server model with all properties and actions
- **ServerManager**: Manager class for server operations
- **BaseObject**: Base class for all API objects with automatic parsing
- **Exception Hierarchy**: Detailed exceptions for different error types
- **Mock Support**: Built-in dry-run mode for testing

### Supported Operations
- Server CRUD operations
- Power management (on, off, reboot, reset, shutdown)
- Image creation and server rebuilding
- Backup enable/disable with scheduling
- Rescue mode enable/disable
- ISO mounting and unmounting
- Server type changes with disk upgrades
- Protection settings (delete, rebuild protection)
- Network attachment/detachment
- DNS PTR record management
- Password reset functionality
- Server action monitoring

### Technical Details
- Python 3.7+ support
- Type hints throughout the codebase
- Requests library for HTTP operations
- Automatic datetime parsing
- Nested object models for complex data structures
- Comprehensive test coverage with dry-run mode

### Documentation
- Complete README with examples
- API coverage documentation
- Error handling guide
- Contributing guidelines
- License information

---

## Release Notes

### v1.0.0 - First Stable Release

This is the first stable release of PyHetznerServer, providing complete coverage of the Hetzner Cloud Server API. The library is designed to be:

- **Developer-friendly**: Intuitive API design with comprehensive documentation
- **Type-safe**: Full type hints for better IDE support and fewer runtime errors
- **Reliable**: Comprehensive error handling and rate limiting awareness
- **Testable**: Built-in dry-run mode for testing without actual API calls
- **Maintainable**: Clean architecture with separate concerns for client, models, and managers

The library has been thoroughly tested and is ready for production use in server management applications, infrastructure automation, and cloud resource management tools.

## [1.1.0] - 2025-06-26

### 🏗️ Major Restructuring
- **BREAKING CHANGE**: Restructured to standard Python package layout
- Moved all source code to `pyhetznerserver/` package directory
- Moved tests to separate `tests/` directory
- Updated all imports and package configuration
- Fixed `__init__.py` with proper exports for clean imports
- Updated `pyproject.toml` for new package structure
- Updated `Makefile` commands for new layout

### ✅ Quality Improvements
- All 24 tests pass with new structure
- Follows Python packaging best practices
- Ready for professional PyPI distribution
- Improved modularity and separation of concerns
- Clean import statements: `from pyhetznerserver import HetznerClient`

### 📦 Package Standards
- PEP-compliant package structure
- Proper setuptools configuration
- Professional directory organization
- Clear separation between source code and tests

## [1.0.3] - 2025-06-26

### �� CI/CD Improvements 