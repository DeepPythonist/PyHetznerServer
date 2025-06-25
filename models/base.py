from typing import Dict, Any, Optional
from datetime import datetime

class BaseObject:
    def __init__(self, data: Dict[str, Any], client=None):
        self._client = client
        self._raw_data = data
        self._parse_data(data)
    
    def _parse_data(self, data: Dict[str, Any]):
        for key, value in data.items():
            if isinstance(value, str) and self._is_datetime(value):
                value = self._parse_datetime(value)
            setattr(self, key, value)
    
    def _is_datetime(self, value: str) -> bool:
        return value.endswith('+00:00') or value.endswith('Z')
    
    def _parse_datetime(self, value: str) -> datetime:
        if value.endswith('Z'):
            value = value[:-1] + '+00:00'
        return datetime.fromisoformat(value)
    
    def to_dict(self) -> Dict[str, Any]:
        return self._raw_data
    
    def __repr__(self) -> str:
        if hasattr(self, 'id') and hasattr(self, 'name'):
            return f"<{self.__class__.__name__}(id={self.id}, name='{self.name}')>"
        elif hasattr(self, 'id'):
            return f"<{self.__class__.__name__}(id={self.id})>"
        else:
            return f"<{self.__class__.__name__}()>" 