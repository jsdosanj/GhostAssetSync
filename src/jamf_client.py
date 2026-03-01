import logging
import requests
from requests.auth import HTTPBasicAuth

logger = logging.getLogger(__name__)


class JamfClient:
    def __init__(self, url, user, password):
        self.base_url = url.rstrip('/')
        if not self.base_url.startswith("https://") and "localhost" not in self.base_url and "127.0.0.1" not in self.base_url:
            raise ValueError(f"JAMF URL must use HTTPS: {self.base_url}")
        self.session = requests.Session()
        self.session.auth = HTTPBasicAuth(user, password)
        self.session.headers.update({"Accept": "application/json"})
        self.session.verify = True  # Explicitly enforce SSL verification

    def get_computers(self):
        r = self.session.get(f"{self.base_url}/JSSResource/computers", timeout=30)
        r.raise_for_status()
        data = r.json()
        if not isinstance(data, dict) or 'computers' not in data:
            logger.warning("Unexpected JAMF response structure for get_computers")
            return []
        return data.get('computers', [])

    def get_computer_detail(self, computer_id):
        if not isinstance(computer_id, int) or computer_id <= 0:
            raise ValueError(f"Invalid computer ID: {computer_id}")
        r = self.session.get(
            f"{self.base_url}/JSSResource/computers/id/{int(computer_id)}",
            timeout=30
        )
        r.raise_for_status()
        return r.json()
