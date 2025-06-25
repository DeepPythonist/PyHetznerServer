"""
PyHetznerServer - A modern, type-safe Python library for Hetzner Cloud Server management.

This library provides a comprehensive interface to manage Hetzner Cloud servers,
including creation, deletion, power management, backups, and more.

Example:
    >>> from pyhetznerserver import HetznerClient
    >>> client = HetznerClient(token="your_api_token")
    >>> servers = client.servers.list()
    >>> print(f"Found {len(servers)} servers")
"""

from .client import HetznerClient
from .exceptions import (
    HetznerAPIError,
    AuthenticationError,
    ValidationError,
    ServerNotFoundError,
    RateLimitError,
    ConflictError,
    ResourceLimitError,
    ActionFailedError
)
from .models.server import Server
from .models.nested import (
    ServerType,
    Datacenter,
    Location,
    Image,
    ISO,
    Protection,
    PublicNet,
    PrivateNet,
    IPv4,
    IPv6
)

__version__ = "1.2.0"
__author__ = "Mohammad Rasol Esfandiari"
__email__ = "mrasolesfandiari@gmail.com"
__license__ = "MIT"
__url__ = "https://github.com/DeepPythonist/PyHetznerServer"

__all__ = [
    # Main client
    "HetznerClient",
    
    # Exceptions
    "HetznerAPIError",
    "AuthenticationError", 
    "ValidationError",
    "ServerNotFoundError",
    "RateLimitError",
    "ConflictError",
    "ResourceLimitError",
    "ActionFailedError",
    
    # Models
    "Server",
    "ServerType",
    "Datacenter",
    "Location",
    "Image", 
    "ISO",
    "Protection",
    "PublicNet",
    "PrivateNet",
    "IPv4",
    "IPv6",
] 