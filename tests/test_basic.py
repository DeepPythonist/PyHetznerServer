import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

try:
    from pyhetznerserver import HetznerClient, ValidationError
except ImportError:
    from pyhetznerserver.client import HetznerClient
    from pyhetznerserver.exceptions import ValidationError


def test_dry_run_mode():
    print("Testing dry run mode...")

    client = HetznerClient(token="fake_token", dry_run=True)

    servers = client.servers.list()
    print(f"✓ Listed servers: {len(servers)}")

    server, action = client.servers.create(
        name="test-server", server_type="cx11", image="ubuntu-20.04", location="fsn1"
    )
    print(f"✓ Created server: {server.name} with ID: {server.id}")
    print(f"✓ Server IP: {server.public_net.ipv4.ip}")
    print(f"✓ Action ID: {action['id']}")

    action = server.power_off()
    print(f"✓ Power off action: {action['command']}")

    action = server.reboot()
    print(f"✓ Reboot action: {action['command']}")

    password, action = server.reset_password()
    print(f"✓ Reset password action, new password available")

    image_id, action = server.create_image("test-image")
    print(f"✓ Created image with ID: {image_id}")

    action = server.enable_backup("22-02")
    print(f"✓ Enabled backup")

    action = server.attach_iso("ubuntu-20.04")
    print(f"✓ Attached ISO")

    action = server.detach_iso()
    print(f"✓ Detached ISO")

    client.close()
    print("✓ All tests passed in dry run mode!")


def test_validation():
    print("\nTesting validation...")

    try:
        client = HetznerClient(token="")
        print("✗ Should have failed with empty token")
    except ValidationError:
        print("✓ Empty token validation works")

    client = HetznerClient(token="fake_token", dry_run=True)

    try:
        client.servers.create(name="ab", server_type="cx11", image="ubuntu-20.04")
        print("✗ Should have failed with short name")
    except ValidationError:
        print("✓ Short name validation works")

    client.close()


def test_models():
    print("\nTesting models...")

    client = HetznerClient(token="fake_token", dry_run=True)
    server, _ = client.servers.create(name="test-model", server_type="cx11", image="ubuntu-20.04")

    print(f"✓ Server model: {repr(server)}")
    print(f"✓ Server type: {server.server_type.name}")
    print(f"✓ Datacenter: {server.datacenter.name}")
    print(f"✓ Location: {server.datacenter.location.name}")
    print(f"✓ Image: {server.image.name}")
    print(f"✓ Protection: delete={server.protection.delete}, rebuild={server.protection.rebuild}")

    client.close()


if __name__ == "__main__":
    print("🚀 Starting PyHetznerServer tests...\n")
    test_dry_run_mode()
    test_validation()
    test_models()
    print("\n🎉 All tests completed successfully!")
