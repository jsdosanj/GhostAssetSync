import requests

class SnipeClient:
    def __init__(self, base_url, token):
        self.base_url = base_url.rstrip('/')
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    def find_asset_by_serial(self, serial):
        r = requests.get(f"{self.base_url}/hardware?search={serial}", headers=self.headers)
        r.raise_for_status()
        data = r.json()
        return data['rows'][0] if data['rows'] else None

    def find_or_create_model(self, os_name):
        r = requests.get(f"{self.base_url}/models?search={os_name}", headers=self.headers)
        r.raise_for_status()
        models = r.json()['rows']
        if models:
            return models[0]['id']
        return 1  # fallback model ID

    def create_asset(self, payload):
        r = requests.post(f"{self.base_url}/hardware", headers=self.headers, json=payload)
        r.raise_for_status()
        return r.json()

    def update_asset(self, asset_id, payload):
        r = requests.put(f"{self.base_url}/hardware/{asset_id}", headers=self.headers, json=payload)
        r.raise_for_status()
        return r.json()
