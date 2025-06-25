# PyHetznerServer

[![PyPI version](https://badge.fury.io/py/pyhetznerserver.svg)](https://badge.fury.io/py/pyhetznerserver)
[![Python Support](https://img.shields.io/pypi/pyversions/pyhetznerserver.svg)](https://pypi.org/project/pyhetznerserver/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Downloads](https://pepy.tech/badge/pyhetznerserver)](https://pepy.tech/project/pyhetznerserver)

A modern, type-safe Python library for **Hetzner Cloud Server** management with comprehensive API coverage.

## 🚀 Features

- **Complete Server Lifecycle Management** - Create, manage, and delete cloud servers
- **All Server Actions** - Power management, backups, rescue mode, ISO handling, and more
- **Type Safety** - Full type hints throughout the codebase
- **Dry-Run Mode** - Test your code without making real API calls
- **Comprehensive Error Handling** - Detailed exception hierarchy
- **Automatic Model Parsing** - JSON responses automatically converted to Python objects
- **Rate Limiting Aware** - Built-in handling of API rate limits
- **Modern Python** - Supports Python 3.8+

## 📦 Installation

```bash
pip install pyhetznerserver
```

## 🔑 Authentication

First, create an API token in the [Hetzner Cloud Console](https://console.hetzner.cloud/):

1. Go to your project
2. Navigate to **Security** → **API Tokens**
3. Generate a new token with appropriate permissions

## 🛠️ Quick Start

```python
from pyhetznerserver import HetznerClient

# Initialize client
client = HetznerClient(token="your_api_token_here")

# List all servers
servers = client.servers.list()
print(f"Found {len(servers)} servers")

# Create a new server
server, action = client.servers.create(
    name="my-web-server",
    server_type="cx11",
    image="ubuntu-20.04",
    location="fsn1",
    ssh_keys=["your-ssh-key-name"],
    labels={"env": "production", "app": "web"}
)

print(f"Server created: {server.name} ({server.public_net.ipv4.ip})")

# Server management
server.power_off()      # Power off server
server.power_on()       # Power on server  
server.reboot()         # Reboot server
server.reset()          # Hard reset

# Advanced operations
server.enable_backup("22-02")                    # Enable daily backups
server.create_image("my-snapshot")               # Create server image
server.enable_rescue()                           # Enable rescue mode
server.attach_iso("ubuntu-20.04")               # Mount ISO
server.change_type("cx21", upgrade_disk=True)   # Upgrade server

# Cleanup
client.close()
```

## 📋 Server Operations

### Power Management
```python
server.power_on()        # Start server
server.power_off()       # Stop server  
server.reboot()          # Restart server
server.reset()           # Force restart
server.shutdown()        # Graceful shutdown
```

### Backup & Recovery
```python
server.enable_backup("22-02")         # Enable backups at 22:00-02:00 UTC
server.disable_backup()               # Disable backups
server.create_image("snapshot-name")  # Create snapshot
server.rebuild("ubuntu-22.04")        # Rebuild from image
```

### Rescue & Maintenance
```python
password, action = server.enable_rescue("linux64", ssh_keys=["key1"])
server.disable_rescue()
server.attach_iso("ubuntu-20.04")
server.detach_iso()
```

### Network Management
```python
server.attach_to_network(network_id, ip="10.0.0.100")
server.detach_from_network(network_id)
server.change_dns_ptr("1.2.3.4", "server.example.com")
```

### Security
```python
password, action = server.reset_password()
server.change_protection(delete=True, rebuild=False)
```

## 🔍 Server Information

Access comprehensive server information through nested objects:

```python
server = client.servers.get(server_id)

# Basic info
print(f"Server: {server.name} (ID: {server.id})")
print(f"Status: {server.status}")
print(f"Created: {server.created}")

# Network information
print(f"IPv4: {server.public_net.ipv4.ip}")
print(f"IPv6: {server.public_net.ipv6.ip}")

# Hardware details
print(f"Type: {server.server_type.name}")
print(f"CPU Cores: {server.server_type.cores}")
print(f"RAM: {server.server_type.memory} GB")
print(f"Disk: {server.server_type.disk} GB")

# Location
print(f"Datacenter: {server.datacenter.name}")
print(f"Location: {server.datacenter.location.city}, {server.datacenter.location.country}")

# Operating System
print(f"OS: {server.image.name} ({server.image.os_flavor})")
```

## 🧪 Testing & Development

Enable dry-run mode for testing without making real API calls:

```python
client = HetznerClient(token="fake_token", dry_run=True)

# All operations return mock data
servers = client.servers.list()  # Returns empty list
server, action = client.servers.create(name="test", server_type="cx11", image="ubuntu-20.04")
print(f"Mock server created: {server.name}")  # Uses fake data
```

## 🚨 Error Handling

The library provides detailed exception hierarchy:

```python
from pyhetznerserver import (
    HetznerAPIError,
    AuthenticationError, 
    ValidationError,
    ServerNotFoundError,
    RateLimitError
)

try:
    server = client.servers.get(999999)
except ServerNotFoundError:
    print("Server not found")
except AuthenticationError:
    print("Invalid API token")
except RateLimitError:
    print("API rate limit exceeded")
except ValidationError as e:
    print(f"Invalid input: {e}")
except HetznerAPIError as e:
    print(f"API error: {e}")
```

## 📊 Filtering & Pagination

```python
# Filter servers
servers = client.servers.list(
    status="running",
    label_selector="env=production",
    sort="name:asc"
)

# Pagination
servers = client.servers.list(page=2, per_page=10)
```

## 🏷️ Labels & Metadata

```python
# Create server with labels
server, action = client.servers.create(
    name="web-server",
    server_type="cx11", 
    image="ubuntu-20.04",
    labels={
        "environment": "production",
        "team": "backend",
        "cost-center": "engineering"
    }
)

# Filter by labels
prod_servers = client.servers.list(label_selector="environment=production")
```

## 🔧 Advanced Configuration

```python
client = HetznerClient(
    token="your_token",
    dry_run=False,           # Enable for testing
    timeout=30               # Request timeout in seconds
)
```

## 📚 API Coverage

This library covers all Hetzner Cloud Server API endpoints:

- ✅ **Server Management** - CRUD operations
- ✅ **Power Actions** - Start, stop, reboot, reset
- ✅ **Image Management** - Create snapshots, rebuild
- ✅ **Backup System** - Enable/disable, scheduling
- ✅ **Rescue Mode** - Recovery operations
- ✅ **ISO Handling** - Mount/unmount ISO images
- ✅ **Network Operations** - Attach/detach networks
- ✅ **DNS Management** - PTR record management
- ✅ **Security** - Password reset, protection settings
- ✅ **Server Types** - Hardware configuration changes
- ✅ **Actions** - Retrieve operation status and history

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Hetzner Cloud](https://www.hetzner.com/cloud) for providing excellent cloud infrastructure
- The Python community for amazing tools and libraries

## 📞 Support

- 📖 **Documentation**: [GitHub Repository](https://github.com/DeepPythonist/PyHetznerServer)
- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/DeepPythonist/PyHetznerServer/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/DeepPythonist/PyHetznerServer/discussions)

## 🔗 Related Projects

- [hcloud-python](https://github.com/hetznercloud/hcloud-python) - Official Hetzner Cloud Python library
- [terraform-provider-hcloud](https://github.com/hetznercloud/terraform-provider-hcloud) - Terraform provider

---

Made with ❤️ for the Python and Hetzner Cloud community 