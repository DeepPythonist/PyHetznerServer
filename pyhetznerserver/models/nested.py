from typing import Dict, Any, List, Optional

try:
    from .base import BaseObject
except ImportError:
    from base import BaseObject

class ServerType(BaseObject):
    id: int
    name: str
    description: str
    cores: int
    memory: float
    disk: int
    deprecated: bool
    prices: List[Dict]
    storage_type: str
    cpu_type: str
    architecture: str
    deprecation: Optional[Dict]

class Location(BaseObject):
    id: int
    name: str
    description: str
    country: str
    city: str
    latitude: float
    longitude: float
    network_zone: str

class Datacenter(BaseObject):
    id: int
    name: str
    description: str
    location: Location
    server_types: Dict
    
    def _parse_data(self, data: Dict[str, Any]):
        super()._parse_data(data)
        if hasattr(self, 'location') and isinstance(self.location, dict):
            self.location = Location(self.location, self._client)

class Image(BaseObject):
    id: int
    type: str
    status: str
    name: str
    description: Optional[str]
    image_size: Optional[float]
    disk_size: int
    created: str
    created_from: Optional[Dict]
    bound_to: Optional[int]
    os_flavor: Optional[str]
    os_version: Optional[str]
    rapid_deploy: bool
    protection: Dict
    deprecated: Optional[str]
    deleted: Optional[str]
    labels: Dict
    architecture: str

class IPv4(BaseObject):
    id: int
    ip: str
    blocked: bool
    dns_ptr: str

class IPv6(BaseObject):
    id: int
    ip: str
    blocked: bool
    dns_ptr: List[Dict]

class PublicNet(BaseObject):
    ipv4: IPv4
    ipv6: IPv6
    floating_ips: List[int]
    firewalls: List[Dict]
    
    def _parse_data(self, data: Dict[str, Any]):
        super()._parse_data(data)
        if hasattr(self, 'ipv4') and isinstance(self.ipv4, dict):
            self.ipv4 = IPv4(self.ipv4, self._client)
        if hasattr(self, 'ipv6') and isinstance(self.ipv6, dict):
            self.ipv6 = IPv6(self.ipv6, self._client)

class PrivateNet(BaseObject):
    network: int
    ip: str
    alias_ips: List[str]
    mac_address: str

class ISO(BaseObject):
    id: int
    name: str
    description: Optional[str]
    type: str
    deprecated: Optional[str]

class Protection(BaseObject):
    delete: bool
    rebuild: bool 