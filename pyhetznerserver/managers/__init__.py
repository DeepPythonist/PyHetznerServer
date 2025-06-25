try:
    from .server_manager import ServerManager
except ImportError:
    from server_manager import ServerManager

__all__ = ["ServerManager"]
