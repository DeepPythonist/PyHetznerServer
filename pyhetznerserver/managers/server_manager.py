import json
from typing import Any, Dict, List, Optional, Tuple, Union

try:
    from ..exceptions import (
        ActionFailedError,
        HetznerAPIError,
        ServerNotFoundError,
        ValidationError,
    )
    from ..models.server import Server
except ImportError:
    import os
    import sys

    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    from exceptions import ActionFailedError, HetznerAPIError, ServerNotFoundError, ValidationError
    from models.server import Server


class ServerManager:
    def __init__(self, client):
        self._client = client
        self._base_url = "servers"

    def list(
        self,
        name: str = None,
        label_selector: str = None,
        sort: str = None,
        status: str = None,
        page: int = 1,
        per_page: int = 25,
    ) -> List[Server]:

        params = {"page": page, "per_page": per_page}
        if name:
            params["name"] = name
        if label_selector:
            params["label_selector"] = label_selector
        if sort:
            params["sort"] = sort
        if status:
            params["status"] = status

        response = self._client._request("GET", self._base_url, params=params)
        return [Server(server_data, self._client) for server_data in response["servers"]]

    def get(self, server_id: int) -> Server:
        try:
            response = self._client._request("GET", f"{self._base_url}/{server_id}")
            return Server(response["server"], self._client)
        except HetznerAPIError as e:
            if e.status_code == 404:
                raise ServerNotFoundError(f"Server {server_id} not found")
            raise

    def create(
        self,
        name: str,
        server_type: str,
        image: str,
        location: str = None,
        datacenter: str = None,
        start_after_create: bool = True,
        ssh_keys: List[str] = None,
        volumes: List[int] = None,
        networks: List[int] = None,
        firewalls: List[Dict] = None,
        user_data: str = None,
        labels: Dict[str, str] = None,
        automount: bool = False,
        placement_group: int = None,
        public_net: Dict = None,
    ) -> Tuple[Server, Dict]:

        if not name or len(name) < 3 or len(name) > 63:
            raise ValidationError("Server name must be 3-63 characters long")

        data = {
            "name": name,
            "server_type": server_type,
            "image": image,
            "start_after_create": start_after_create,
            "automount": automount,
        }

        if location:
            data["location"] = location
        if datacenter:
            data["datacenter"] = datacenter
        if ssh_keys:
            data["ssh_keys"] = ssh_keys
        if volumes:
            data["volumes"] = volumes
        if networks:
            data["networks"] = networks
        if firewalls:
            data["firewalls"] = firewalls
        if user_data:
            data["user_data"] = user_data
        if labels:
            data["labels"] = labels
        if placement_group:
            data["placement_group"] = placement_group
        if public_net:
            data["public_net"] = public_net

        response = self._client._request("POST", self._base_url, json=data)
        server = Server(response["server"], self._client)
        return server, response["action"]

    def delete(self, server_id: int) -> Dict:
        response = self._client._request("DELETE", f"{self._base_url}/{server_id}")
        return response.get("action", {})

    def power_on(self, server_id: int) -> Dict:
        return self._action(server_id, "poweron")

    def power_off(self, server_id: int) -> Dict:
        return self._action(server_id, "poweroff")

    def reboot(self, server_id: int) -> Dict:
        return self._action(server_id, "reboot")

    def reset(self, server_id: int) -> Dict:
        return self._action(server_id, "reset")

    def shutdown(self, server_id: int) -> Dict:
        return self._action(server_id, "shutdown")

    def rebuild(self, server_id: int, image: str) -> Dict:
        data = {"image": image}
        return self._action(server_id, "rebuild", data)

    def create_image(
        self, server_id: int, name: str, image_type: str = "snapshot"
    ) -> Tuple[int, Dict]:
        data = {"description": name, "type": image_type}
        response = self._action(server_id, "create_image", data)
        return response.get("image", {}).get("id"), response

    def enable_rescue(
        self, server_id: int, rescue_type: str = "linux64", ssh_keys: List[str] = None
    ) -> Tuple[str, Dict]:
        data = {"type": rescue_type}
        if ssh_keys:
            data["ssh_keys"] = ssh_keys
        response = self._action(server_id, "enable_rescue", data)
        return response.get("root_password"), response

    def disable_rescue(self, server_id: int) -> Dict:
        return self._action(server_id, "disable_rescue")

    def enable_backup(self, server_id: int, backup_window: str) -> Dict:
        data = {"backup_window": backup_window}
        return self._action(server_id, "enable_backup", data)

    def disable_backup(self, server_id: int) -> Dict:
        return self._action(server_id, "disable_backup")

    def attach_iso(self, server_id: int, iso: str) -> Dict:
        data = {"iso": iso}
        return self._action(server_id, "attach_iso", data)

    def detach_iso(self, server_id: int) -> Dict:
        return self._action(server_id, "detach_iso")

    def change_type(self, server_id: int, server_type: str, upgrade_disk: bool = False) -> Dict:
        data = {"server_type": server_type, "upgrade_disk": upgrade_disk}
        return self._action(server_id, "change_type", data)

    def change_protection(self, server_id: int, delete: bool = None, rebuild: bool = None) -> Dict:
        data = {}
        if delete is not None:
            data["delete"] = delete
        if rebuild is not None:
            data["rebuild"] = rebuild
        return self._action(server_id, "change_protection", data)

    def attach_to_network(
        self, server_id: int, network: int, ip: str = None, alias_ips: List[str] = None
    ) -> Dict:
        data = {"network": network}
        if ip:
            data["ip"] = ip
        if alias_ips:
            data["alias_ips"] = alias_ips
        return self._action(server_id, "attach_to_network", data)

    def detach_from_network(self, server_id: int, network: int) -> Dict:
        data = {"network": network}
        return self._action(server_id, "detach_from_network", data)

    def change_dns_ptr(self, server_id: int, ip: str, dns_ptr: str) -> Dict:
        data = {"ip": ip, "dns_ptr": dns_ptr}
        return self._action(server_id, "change_dns_ptr", data)

    def reset_password(self, server_id: int) -> Tuple[str, Dict]:
        response = self._action(server_id, "reset_password")
        return response.get("root_password"), response

    def get_actions(self, server_id: int) -> List[Dict]:
        response = self._client._request("GET", f"{self._base_url}/{server_id}/actions")
        return response["actions"]

    def get_action(self, server_id: int, action_id: int) -> Dict:
        response = self._client._request("GET", f"{self._base_url}/{server_id}/actions/{action_id}")
        return response["action"]

    def _action(self, server_id: int, action_name: str, data: Dict = None) -> Dict:
        url = f"{self._base_url}/{server_id}/actions/{action_name}"
        response = self._client._request("POST", url, json=data or {})
        return response.get("action", response)
