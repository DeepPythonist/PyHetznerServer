from typing import Dict, Any, List, Optional

try:
    from .base import BaseObject
    from .nested import ServerType, Datacenter, Image, PublicNet, PrivateNet, ISO, Protection
except ImportError:
    from base import BaseObject
    from nested import ServerType, Datacenter, Image, PublicNet, PrivateNet, ISO, Protection

class Server(BaseObject):
    id: int
    name: str
    status: str
    created: str
    public_net: PublicNet
    private_net: List[PrivateNet]
    server_type: ServerType
    datacenter: Datacenter
    image: Image
    iso: Optional[ISO]
    rescue_enabled: bool
    locked: bool
    backup_window: Optional[str]
    outgoing_traffic: Optional[int]
    ingoing_traffic: Optional[int]
    included_traffic: Optional[int]
    protection: Protection
    labels: Dict[str, str]
    volumes: List[int]
    load_balancers: List[int]
    
    def _parse_data(self, data: Dict[str, Any]):
        super()._parse_data(data)
        
        if hasattr(self, 'public_net') and isinstance(self.public_net, dict):
            self.public_net = PublicNet(self.public_net, self._client)
            
        if hasattr(self, 'private_net') and isinstance(self.private_net, list):
            self.private_net = [PrivateNet(net, self._client) for net in self.private_net]
            
        if hasattr(self, 'server_type') and isinstance(self.server_type, dict):
            self.server_type = ServerType(self.server_type, self._client)
            
        if hasattr(self, 'datacenter') and isinstance(self.datacenter, dict):
            self.datacenter = Datacenter(self.datacenter, self._client)
            
        if hasattr(self, 'image') and isinstance(self.image, dict):
            self.image = Image(self.image, self._client)
            
        if hasattr(self, 'iso') and isinstance(self.iso, dict):
            self.iso = ISO(self.iso, self._client)
            
        if hasattr(self, 'protection') and isinstance(self.protection, dict):
            self.protection = Protection(self.protection, self._client)
    
    def power_on(self):
        return self._client.servers.power_on(self.id)
    
    def power_off(self):
        return self._client.servers.power_off(self.id)
    
    def reboot(self):
        return self._client.servers.reboot(self.id)
    
    def reset(self):
        return self._client.servers.reset(self.id)
    
    def shutdown(self):
        return self._client.servers.shutdown(self.id)
    
    def rebuild(self, image: str):
        return self._client.servers.rebuild(self.id, image)
    
    def create_image(self, name: str, image_type: str = "snapshot"):
        return self._client.servers.create_image(self.id, name, image_type)
    
    def enable_rescue(self, rescue_type: str = "linux64", ssh_keys: List[str] = None):
        return self._client.servers.enable_rescue(self.id, rescue_type, ssh_keys)
    
    def disable_rescue(self):
        return self._client.servers.disable_rescue(self.id)
    
    def enable_backup(self, backup_window: str):
        return self._client.servers.enable_backup(self.id, backup_window)
    
    def disable_backup(self):
        return self._client.servers.disable_backup(self.id)
    
    def attach_iso(self, iso: str):
        return self._client.servers.attach_iso(self.id, iso)
    
    def detach_iso(self):
        return self._client.servers.detach_iso(self.id)
    
    def change_type(self, server_type: str, upgrade_disk: bool = False):
        return self._client.servers.change_type(self.id, server_type, upgrade_disk)
    
    def change_protection(self, delete: bool = None, rebuild: bool = None):
        return self._client.servers.change_protection(self.id, delete, rebuild)
    
    def attach_to_network(self, network: int, ip: str = None, alias_ips: List[str] = None):
        return self._client.servers.attach_to_network(self.id, network, ip, alias_ips)
    
    def detach_from_network(self, network: int):
        return self._client.servers.detach_from_network(self.id, network)
    
    def change_dns_ptr(self, ip: str, dns_ptr: str):
        return self._client.servers.change_dns_ptr(self.id, ip, dns_ptr)
    
    def reset_password(self):
        return self._client.servers.reset_password(self.id)
    
    def delete(self):
        return self._client.servers.delete(self.id)
    
    def refresh(self):
        server_data = self._client.servers.get(self.id)
        self._parse_data(server_data._raw_data)
        return self 