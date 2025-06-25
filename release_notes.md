🎉 PyHetznerServer v1.0.0 Release Notes

## 🚀 First Stable Release

This is the first stable release of PyHetznerServer, a modern, type-safe Python library for Hetzner Cloud Server management.

### ✨ Key Features

- **Complete Server Lifecycle Management** - Create, manage, and delete cloud servers
- **All Server Actions** - Power management, backups, rescue mode, ISO handling, and more  
- **Type Safety** - Full type hints throughout the codebase
- **Dry-Run Mode** - Test your code without making real API calls
- **Comprehensive Error Handling** - Detailed exception hierarchy
- **Automatic Model Parsing** - JSON responses automatically converted to Python objects
- **Rate Limiting Aware** - Built-in handling of API rate limits
- **Modern Python** - Supports Python 3.7+

### �� Installation

```bash
pip install pyhetznerserver
```

### 🛠️ Quick Start

```python
from pyhetznerserver import HetznerClient

# Initialize client
client = HetznerClient(token="your_api_token_here")

# Create a server
server, action = client.servers.create(
    name="my-server",
    server_type="cx11",
    image="ubuntu-20.04",
    location="fsn1"
)

# Manage server
server.power_off()
server.power_on() 
server.reboot()

client.close()
```

### 📋 Supported Operations

- ✅ Server CRUD operations
- ✅ Power management (on, off, reboot, reset, shutdown)
- ✅ Image creation and server rebuilding
- ✅ Backup enable/disable with scheduling
- ✅ Rescue mode enable/disable
- ✅ ISO mounting and unmounting
- ✅ Server type changes with disk upgrades
- ✅ Protection settings (delete, rebuild protection)
- ✅ Network attachment/detachment
- ✅ DNS PTR record management
- ✅ Password reset functionality
- ✅ Server action monitoring

### 🧪 Technical Details

- **Python Support**: 3.7+
- **Type Hints**: Complete type coverage
- **Testing**: 24 passing tests
- **CI/CD**: GitHub Actions workflow
- **Documentation**: Comprehensive README and examples
- **License**: MIT

### 🙏 Acknowledgments

Built for the Python and Hetzner Cloud community with ❤️

---

**Happy Cloud Computingcheck-build* ☁️
