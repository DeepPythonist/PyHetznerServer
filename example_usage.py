try:
    from pyhetznerserver import HetznerClient, ServerNotFoundError, ValidationError
except ImportError:
    from __init__ import HetznerClient
    from exceptions import ServerNotFoundError, ValidationError

def main():
    client = HetznerClient(token="your_api_token_here", dry_run=True)
    
    try:
        servers = client.servers.list()
        print(f"Found {len(servers)} servers")
        
        for server in servers:
            print(f"Server: {server.name} (ID: {server.id}) - Status: {server.status}")
        
        server, action = client.servers.create(
            name="my-test-server",
            server_type="cx11", 
            image="ubuntu-20.04",
            location="fsn1",
            ssh_keys=["my-ssh-key"],
            labels={"env": "test", "purpose": "development"}
        )
        
        print(f"Created server: {server.name} with ID: {server.id}")
        print(f"Server IP: {server.public_net.ipv4.ip}")
        print(f"Action ID: {action['id']}")
        
        server.power_off()
        print("Server powered off")
        
        server.power_on()
        print("Server powered on")
        
        password, action = server.reset_password()
        print(f"New root password: {password}")
        
        server.enable_backup("22-02")
        print("Backup enabled")
        
        try:
            non_existent = client.servers.get(99999)
        except ServerNotFoundError:
            print("Server 99999 not found")
        
    except ValidationError as e:
        print(f"Validation error: {e}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    main() 