import requests

class SnipeAPI:
    def __init__(self, base_url, token):
        self.base_url = base_url.rstrip('/')
        self.headers = {
            'Authorization': f'Bearer {token}',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def search_asset_by_serial(self, serial):
        url = f"{self.base_url}/hardware?search={serial}"
        r = requests.get(url, headers=self.headers)
        results = r.json()
        return results['rows'][0] if results['rows'] else None

    def get_model_id(self, model_name):
        url = f"{self.base_url}/models?search={model_name}"
        r = requests.get(url, headers=self.headers)
        data = r.json()
        return data['rows'][0]['id'] if data['rows'] else None

    def create_asset(self, payload):
        url = f"{self.base_url}/hardware"
        r = requests.post(url, headers=self.headers, json=payload)
        return r.json()

    def update_asset(self, asset_id, payload):
        url = f"{self.base_url}/hardware/{asset_id}"
        r = requests.put(url, headers=self.headers, json=payload)
        return r.json()
