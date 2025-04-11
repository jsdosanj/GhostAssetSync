import requests
from requests.auth import HTTPBasicAuth

class JamfClient:
    def __init__(self, url, user, password):
        self.base_url = url.rstrip('/')
        self.auth = HTTPBasicAuth(user, password)

    def get_computers(self):
        r = requests.get(f"{self.base_url}/JSSResource/computers", auth=self.auth, headers={"Accept": "application/json"})
        r.raise_for_status()
        return r.json().get('computers', [])

    def get_computer_detail(self, id):
        r = requests.get(f"{self.base_url}/JSSResource/computers/id/{id}", auth=self.auth, headers={"Accept": "application/json"})
        r.raise_for_status()
        return r.json()
