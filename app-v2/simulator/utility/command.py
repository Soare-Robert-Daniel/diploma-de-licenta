from typing import Optional, Dict, Any


class Command:
    def __init__(self, command_type: str, payload: Optional[Dict[str, Any]] = None):
        self.type = command_type
        self.payload = payload

    def set_payload(self, payload: Optional[Dict[str, Any]]):
        if payload is not None:
            self.payload = payload
