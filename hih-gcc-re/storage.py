from typing import Dict, Any, Optional
from schemas import DealArtifacts
import fastapi
import requests
from bs4 import BeautifulSoup
class Store:
    _mem: Dict[str, DealArtifacts] = {}

    def exists(self, deal_id: str) -> bool:
        return deal_id in self._mem

    def init_deal(self, deal_id: str):
        self._mem[deal_id] = DealArtifacts()

    def update_status(self, deal_id: str, state: str):
        self._mem[deal_id].state = state

    def save_artifact(self, deal_id: str, name: str, value: Any):
        self._mem[deal_id].artifacts[name] = value

    def get_status(self, deal_id: str) -> Optional[dict]:
        if deal_id not in self._mem:
            return None
        d = self._mem[deal_id]
        return {"deal_id": deal_id, "state": d.state, "artifacts": d.artifacts}
