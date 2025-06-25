import json
import requests
from typing import Dict, Any, Optional

try:
    from .managers.server_manager import ServerManager
    from .exceptions import (
        HetznerAPIError,
        AuthenticationError,
        ValidationError,
        RateLimitError,
        ServerNotFoundError,
        ConflictError,
        ResourceLimitError
    )
except ImportError:
    from managers.server_manager import ServerManager
    from exceptions import (
        HetznerAPIError,
        AuthenticationError,
        ValidationError,
        RateLimitError,
        ServerNotFoundError,
        ConflictError,
        ResourceLimitError
    )

class HetznerClient:
    BASE_URL = "https://api.hetzner.cloud/v1"
    
    def __init__(self, token: str, dry_run: bool = False, timeout: int = 30):
        if not token:
            raise ValidationError("API token is required")
            
        self.token = token
        self.dry_run = dry_run
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "PyHetznerServer/1.0.0"
        })
        
        self.servers = ServerManager(self)
    
    def _request(self, method: str, endpoint: str, params: Dict = None, json: Dict = None) -> Dict[str, Any]:
        if self.dry_run:
            return self._mock_response(method, endpoint, json)
        
        url = f"{self.BASE_URL}/{endpoint}"
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                json=json,
                timeout=self.timeout
            )
            
            self._handle_response_errors(response)
            
            if response.status_code == 204:
                return {}
                
            return response.json()
            
        except requests.exceptions.Timeout:
            raise HetznerAPIError("Request timeout")
        except requests.exceptions.ConnectionError:
            raise HetznerAPIError("Connection error")
        except requests.exceptions.RequestException as e:
            raise HetznerAPIError(f"Request failed: {str(e)}")
    
    def _handle_response_errors(self, response: requests.Response):
        if response.status_code < 400:
            return
            
        try:
            error_data = response.json().get("error", {})
            error_code = error_data.get("code", "unknown")
            error_message = error_data.get("message", "Unknown error")
        except (ValueError, KeyError):
            error_code = "unknown"
            error_message = f"HTTP {response.status_code}"
        
        if response.status_code == 401:
            raise AuthenticationError(error_message, response.status_code, error_code)
        elif response.status_code == 403:
            if error_code == "rate_limit_exceeded":
                raise RateLimitError(error_message, response.status_code, error_code)
            raise HetznerAPIError(error_message, response.status_code, error_code)
        elif response.status_code == 404:
            raise ServerNotFoundError(error_message, response.status_code, error_code)
        elif response.status_code == 409:
            raise ConflictError(error_message, response.status_code, error_code)
        elif response.status_code == 422:
            raise ValidationError(error_message, response.status_code, error_code)
        elif response.status_code == 429:
            raise RateLimitError(error_message, response.status_code, error_code)
        elif error_code == "resource_limit_exceeded":
            raise ResourceLimitError(error_message, response.status_code, error_code)
        else:
            raise HetznerAPIError(error_message, response.status_code, error_code)
    
    def _mock_response(self, method: str, endpoint: str, data: Dict = None) -> Dict[str, Any]:
        if "servers" in endpoint:
            if method == "POST" and not "/" in endpoint.replace("servers", ""):
                return {
                    "server": {
                        "id": 12345,
                        "name": data.get("name", "test-server"),
                        "status": "initializing",
                        "created": "2023-01-01T00:00:00+00:00",
                        "public_net": {
                            "ipv4": {"id": 1, "ip": "192.168.1.1", "blocked": False, "dns_ptr": "test.example.com"},
                            "ipv6": {"id": 2, "ip": "2001:db8::/64", "blocked": False, "dns_ptr": []},
                            "floating_ips": [],
                            "firewalls": []
                        },
                        "private_net": [],
                        "server_type": {
                            "id": 1, "name": "cx11", "description": "CX11", "cores": 1, "memory": 2.0, "disk": 20,
                            "deprecated": False, "prices": [], "storage_type": "local", "cpu_type": "shared", "architecture": "x86"
                        },
                        "datacenter": {
                            "id": 1, "name": "fsn1-dc8", "description": "Falkenstein DC 8",
                            "location": {"id": 1, "name": "fsn1", "description": "Falkenstein", "country": "DE", "city": "Falkenstein", "latitude": 50.47612, "longitude": 12.370071, "network_zone": "eu-central"}
                        },
                        "image": {
                            "id": 1, "type": "system", "status": "available", "name": "ubuntu-20.04", "description": "Ubuntu 20.04",
                            "image_size": 2.5, "disk_size": 5, "created": "2023-01-01T00:00:00+00:00", "os_flavor": "ubuntu", "os_version": "20.04",
                            "rapid_deploy": True, "protection": {"delete": False}, "labels": {}, "architecture": "x86"
                        },
                        "iso": None,
                        "rescue_enabled": False,
                        "locked": False,
                        "backup_window": None,
                        "outgoing_traffic": 0,
                        "ingoing_traffic": 0,
                        "included_traffic": 21474836480,
                        "protection": {"delete": False, "rebuild": False},
                        "labels": {},
                        "volumes": [],
                        "load_balancers": []
                    },
                    "action": {
                        "id": 123,
                        "command": "create_server",
                        "status": "running",
                        "progress": 0,
                        "started": "2023-01-01T00:00:00+00:00",
                        "finished": None,
                        "resources": [{"id": 12345, "type": "server"}],
                        "error": None
                    },
                    "next_actions": [],
                    "root_password": "MockPassword123!" if not data.get("ssh_keys") else None
                }
            elif method == "GET" and "/" not in endpoint.replace("servers", ""):
                return {
                    "servers": [],
                    "meta": {"pagination": {"page": 1, "per_page": 25, "previous_page": None, "next_page": None, "last_page": 1, "total_entries": 0}}
                }
            elif method == "GET" and "/" in endpoint.replace("servers", ""):
                return {
                    "server": {
                        "id": 12345,
                        "name": "mock-server",
                        "status": "running",
                        "created": "2023-01-01T00:00:00+00:00",
                        "public_net": {"ipv4": {"id": 1, "ip": "192.168.1.1", "blocked": False, "dns_ptr": "test.example.com"}, "ipv6": {"id": 2, "ip": "2001:db8::/64", "blocked": False, "dns_ptr": []}, "floating_ips": [], "firewalls": []},
                        "private_net": [],
                        "server_type": {"id": 1, "name": "cx11", "description": "CX11", "cores": 1, "memory": 2.0, "disk": 20, "deprecated": False, "prices": [], "storage_type": "local", "cpu_type": "shared", "architecture": "x86"},
                        "datacenter": {"id": 1, "name": "fsn1-dc8", "description": "Falkenstein DC 8", "location": {"id": 1, "name": "fsn1", "description": "Falkenstein", "country": "DE", "city": "Falkenstein", "latitude": 50.47612, "longitude": 12.370071, "network_zone": "eu-central"}},
                        "image": {"id": 1, "type": "system", "status": "available", "name": "ubuntu-20.04", "description": "Ubuntu 20.04", "image_size": 2.5, "disk_size": 5, "created": "2023-01-01T00:00:00+00:00", "os_flavor": "ubuntu", "os_version": "20.04", "rapid_deploy": True, "protection": {"delete": False}, "labels": {}, "architecture": "x86"},
                        "iso": None,
                        "rescue_enabled": False,
                        "locked": False,
                        "backup_window": None,
                        "outgoing_traffic": 0,
                        "ingoing_traffic": 0,
                        "included_traffic": 21474836480,
                        "protection": {"delete": False, "rebuild": False},
                        "labels": {},
                        "volumes": [],
                        "load_balancers": []
                    }
                }
            elif "actions" in endpoint:
                return {
                    "action": {
                        "id": 123,
                        "command": "mock_action",
                        "status": "success",
                        "progress": 100,
                        "started": "2023-01-01T00:00:00+00:00",
                        "finished": "2023-01-01T00:01:00+00:00",
                        "resources": [{"id": 12345, "type": "server"}],
                        "error": None
                    }
                }
        
        return {"mock": True, "method": method, "endpoint": endpoint, "data": data}
    
    def close(self):
        if self.session:
            self.session.close() 