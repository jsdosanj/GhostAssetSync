import configparser
from src.system_info import collect_system_info
from src.jamf_client import JamfClient
from src.snipeit_client import SnipeClient
from src.asset_sync import sync_to_snipe

config = configparser.ConfigParser()
config.read("settings.conf")
c = config["DEFAULT"]

# Init clients
jamf = JamfClient(c['jamf_url'], c['jamf_user'], c['jamf_password'])
snipe = SnipeClient(c['snipe_url'], c['snipe_token'])

# Step 1: Local system info
sys_info = collect_system_info()

# Step 2: Pull JAMF info by serial
jamf_assets = jamf.get_computers()
jamf_asset = next((j for j in jamf_assets if j.get('serial_number') == sys_info['serial']), {})

# Step 3: Sync to Snipe
sync_to_snipe(sys_info, jamf_asset, snipe, int(c["site_id"]), int(c["company_id"]))

print("✅ GhostAssetSync Fusion complete.")
