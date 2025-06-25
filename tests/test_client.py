"""
Test cases for HetznerClient.
"""

import pytest
import requests
from unittest.mock import patch, Mock

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from pyhetznerserver.client import HetznerClient
from pyhetznerserver.exceptions import (
    ValidationError,
    AuthenticationError,
    RateLimitError,
    HetznerAPIError
)


class TestHetznerClient:
    """Test cases for HetznerClient class."""
    
    def test_client_initialization_with_valid_token(self):
        """Test that client initializes correctly with valid token."""
        client = HetznerClient(token="valid_token")
        
        assert client.token == "valid_token"
        assert client.dry_run is False
        assert client.timeout == 30
        assert client.session is not None
        assert "Bearer valid_token" in client.session.headers["Authorization"]
        
        client.close()
    
    def test_client_initialization_with_empty_token_raises_error(self):
        """Test that empty token raises ValidationError."""
        with pytest.raises(ValidationError, match="API token is required"):
            HetznerClient(token="")
    
    def test_client_initialization_with_none_token_raises_error(self):
        """Test that None token raises ValidationError."""
        with pytest.raises(ValidationError, match="API token is required"):
            HetznerClient(token=None)
    
    def test_client_initialization_with_dry_run_mode(self):
        """Test that dry-run mode is set correctly."""
        client = HetznerClient(token="test_token", dry_run=True)
        
        assert client.dry_run is True
        client.close()
    
    def test_client_initialization_with_custom_timeout(self):
        """Test that custom timeout is set correctly."""
        client = HetznerClient(token="test_token", timeout=60)
        
        assert client.timeout == 60
        client.close()
    
    def test_dry_run_mode_returns_mock_data(self):
        """Test that dry-run mode returns mock data for all requests."""
        client = HetznerClient(token="test_token", dry_run=True)
        
        # Test GET request
        response = client._request("GET", "servers")
        assert "servers" in response
        assert response["servers"] == []
        
        # Test POST request
        response = client._request("POST", "servers", json={"name": "test"})
        assert "server" in response
        assert response["server"]["name"] == "test"
        
        client.close()
    
    @patch('requests.Session.request')
    def test_successful_api_request(self, mock_request):
        """Test successful API request handling."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"servers": []}
        mock_request.return_value = mock_response
        
        client = HetznerClient(token="test_token")
        response = client._request("GET", "servers")
        
        assert response == {"servers": []}
        mock_request.assert_called_once()
        
        client.close()
    
    @patch('requests.Session.request')
    def test_204_no_content_response(self, mock_request):
        """Test handling of 204 No Content responses."""
        mock_response = Mock()
        mock_response.status_code = 204
        mock_request.return_value = mock_response
        
        client = HetznerClient(token="test_token")
        response = client._request("DELETE", "servers/123")
        
        assert response == {}
        
        client.close()
    
    @patch('requests.Session.request')
    def test_401_authentication_error(self, mock_request):
        """Test that 401 status code raises AuthenticationError."""
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.json.return_value = {
            "error": {
                "code": "unauthorized",
                "message": "Invalid token"
            }
        }
        mock_request.return_value = mock_response
        
        client = HetznerClient(token="invalid_token")
        
        with pytest.raises(AuthenticationError, match="Invalid token"):
            client._request("GET", "servers")
        
        client.close()
    
    @patch('requests.Session.request')
    def test_429_rate_limit_error(self, mock_request):
        """Test that 429 status code raises RateLimitError."""
        mock_response = Mock()
        mock_response.status_code = 429
        mock_response.json.return_value = {
            "error": {
                "code": "rate_limit_exceeded",
                "message": "Rate limit exceeded"
            }
        }
        mock_request.return_value = mock_response
        
        client = HetznerClient(token="test_token")
        
        with pytest.raises(RateLimitError, match="Rate limit exceeded"):
            client._request("GET", "servers")
        
        client.close()
    
    @patch('requests.Session.request')
    def test_422_validation_error(self, mock_request):
        """Test that 422 status code raises ValidationError."""
        mock_response = Mock()
        mock_response.status_code = 422
        mock_response.json.return_value = {
            "error": {
                "code": "invalid_input",
                "message": "Invalid server name"
            }
        }
        mock_request.return_value = mock_response
        
        client = HetznerClient(token="test_token")
        
        with pytest.raises(ValidationError, match="Invalid server name"):
            client._request("POST", "servers", json={"name": ""})
        
        client.close()
    
    @patch('requests.Session.request')
    def test_generic_api_error(self, mock_request):
        """Test handling of generic API errors."""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {
            "error": {
                "code": "internal_error",
                "message": "Internal server error"
            }
        }
        mock_request.return_value = mock_response
        
        client = HetznerClient(token="test_token")
        
        with pytest.raises(HetznerAPIError, match="Internal server error"):
            client._request("GET", "servers")
        
        client.close()
    
    @patch('requests.Session.request')
    def test_malformed_error_response(self, mock_request):
        """Test handling of malformed error responses."""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {}  # No error field
        mock_request.return_value = mock_response
        
        client = HetznerClient(token="test_token")
        
        with pytest.raises(HetznerAPIError, match="Unknown error"):
            client._request("GET", "servers")
        
        client.close()
    
    @patch('requests.Session.request')
    def test_request_timeout_error(self, mock_request):
        """Test handling of request timeout."""
        mock_request.side_effect = requests.exceptions.Timeout()
        
        client = HetznerClient(token="test_token")
        
        with pytest.raises(HetznerAPIError, match="Request timeout"):
            client._request("GET", "servers")
        
        client.close()
    
    @patch('requests.Session.request')
    def test_connection_error(self, mock_request):
        """Test handling of connection errors."""
        mock_request.side_effect = requests.exceptions.ConnectionError()
        
        client = HetznerClient(token="test_token")
        
        with pytest.raises(HetznerAPIError, match="Connection error"):
            client._request("GET", "servers")
        
        client.close()
    
    def test_client_has_servers_manager(self):
        """Test that client has servers manager."""
        client = HetznerClient(token="test_token", dry_run=True)
        
        assert hasattr(client, 'servers')
        assert client.servers is not None
        
        client.close()
    
    def test_client_close(self):
        """Test that client close method works."""
        client = HetznerClient(token="test_token")
        session = client.session
        
        client.close()
        
        # Session should be closed but we can't easily test it
        # Just ensure no exception is raised
        assert True
    
    def test_user_agent_header(self):
        """Test that User-Agent header is set correctly."""
        client = HetznerClient(token="test_token")
        
        assert "PyHetznerServer/1.0.0" in client.session.headers["User-Agent"]
        
        client.close()
    
    def test_content_type_header(self):
        """Test that Content-Type header is set correctly."""
        client = HetznerClient(token="test_token")
        
        assert client.session.headers["Content-Type"] == "application/json"
        
        client.close()


@pytest.fixture
def client():
    """Fixture for HetznerClient in dry-run mode."""
    client = HetznerClient(token="test_token", dry_run=True)
    yield client
    client.close()


class TestClientIntegration:
    """Integration tests for HetznerClient."""
    
    def test_client_servers_list_dry_run(self, client):
        """Test that servers.list() works in dry-run mode."""
        servers = client.servers.list()
        assert isinstance(servers, list)
        assert len(servers) == 0
    
    def test_client_servers_create_dry_run(self, client):
        """Test that servers.create() works in dry-run mode."""
        server, action = client.servers.create(
            name="test-server",
            server_type="cx11",
            image="ubuntu-20.04"
        )
        
        assert server.name == "test-server"
        assert server.id == 12345
        assert action["command"] == "create_server" 