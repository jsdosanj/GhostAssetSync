import logging
import requests
from urllib.parse import quote

logger = logging.getLogger(__name__)


class SnipeClient:
    def __init__(self, base_url, token):
        self.base_url = base_url.rstrip('/')
        if not self.base_url.startswith("https://") and "localhost" not in self.base_url and "127.0.0.1" not in self.base_url:
            raise ValueError(f"Snipe-IT URL must use HTTPS: {self.base_url}")
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        })
        self.session.verify = True

    def find_asset_by_serial(self, serial):
        safe_serial = quote(str(serial), safe='')
        r = self.session.get(f"{self.base_url}/hardware?search={safe_serial}", timeout=30)
        r.raise_for_status()
        data = r.json()
        if not isinstance(data, dict) or 'rows' not in data:
            logger.warning("Unexpected Snipe-IT response for find_asset_by_serial")
            return None
        rows = data.get('rows', [])
        return rows[0] if rows else None

    def find_or_create_model(self, os_name):
        safe_name = quote(str(os_name), safe='')
        r = self.session.get(f"{self.base_url}/models?search={safe_name}", timeout=30)
        r.raise_for_status()
        data = r.json()
        if not isinstance(data, dict) or 'rows' not in data:
            logger.warning("Unexpected Snipe-IT response for find_or_create_model")
            return 1
        models = data.get('rows', [])
        if models and isinstance(models[0], dict) and 'id' in models[0]:
            return models[0]['id']
        return 1

    def create_asset(self, payload):
        r = self.session.post(f"{self.base_url}/hardware", json=payload, timeout=30)
        r.raise_for_status()
        return r.json()

    def update_asset(self, asset_id, payload):
        if not isinstance(asset_id, int) or asset_id <= 0:
            raise ValueError(f"Invalid asset ID: {asset_id}")
        r = self.session.put(f"{self.base_url}/hardware/{int(asset_id)}", json=payload, timeout=30)
        r.raise_for_status()
        return r.json()
