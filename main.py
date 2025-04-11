import configparser
from src import info_collector, snipe_api, helpers

config = configparser.ConfigParser()
config.read('settings.conf')

info = info_collector.collect_all()
token = config['DEFAULT']['snipe_token']
url = config['DEFAULT']['snipe_url']
fields = [f.strip() for f in config['DEFAULT']['sync_fields'].split(',')]

api = snipe_api.SnipeAPI(url, token)
existing = api.search_asset_by_serial(info['serial'])

payload = {}
if 'hostname' in fields: payload['name'] = info['hostname']
if 'os_name' in fields: payload['custom_fields'] = {'Operating System': info['os_name']}
if 'os_version' in fields: payload['custom_fields']['OS Version'] = info['os_version']
if 'os_build' in fields: payload['custom_fields']['OS Build'] = info['os_build']
if 'mac_address' in fields: payload['custom_fields']['MAC Address'] = info['mac_address']
if 'logged_in_users' in fields: payload['custom_fields']['Logged In Users'] = info['logged_in_users']
if 'ad_group' in fields: payload['custom_fields']['AD Group'] = info['ad_group']

# Source-of-truth = Snipe
if existing:
    asset_id = existing['id']
    payload['asset_tag'] = existing['asset_tag']
    print("🔄 Updating existing asset in Snipe...")
    api.update_asset(asset_id, payload)
else:
    print("➕ Creating new asset...")
    payload['serial'] = info['serial']
    payload['asset_tag'] = helpers.generate_asset_tag(info['serial'], info['hostname'])
    payload['model_id'] = api.get_model_id(info['os_name']) or 1
    payload['status_id'] = 2
    payload['company_id'] = config['DEFAULT'].getint('company_id')
    payload['site_id'] = config['DEFAULT'].getint('site_id')
    api.create_asset(payload)

print("✅ Sync complete.")
