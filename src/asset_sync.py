from src.utils import generate_asset_tag

def sync_to_snipe(system_info, jamf_asset, snipe_client, site_id, company_id):
    serial = system_info['serial']
    hostname = system_info['hostname']
    asset = snipe_client.find_asset_by_serial(serial)

    custom_fields = {
        "Operating System": system_info['os_name'],
        "OS Version": system_info['os_version'],
        "OS Build": system_info['os_build'],
        "MAC Address": system_info['mac_address'],
        "Logged In Users": system_info['logged_in_users'],
    }

    if asset:
        print(f"🔄 Updating existing asset [{serial}] in Snipe")
        payload = {
            "name": hostname,
            "custom_fields": custom_fields,
            "asset_tag": asset["asset_tag"]
        }
        snipe_client.update_asset(asset["id"], payload)
    else:
        print(f"➕ Creating new asset [{serial}] in Snipe")
        asset_tag = generate_asset_tag(serial, hostname)
        payload = {
            "name": hostname,
            "serial": serial,
            "asset_tag": asset_tag,
            "model_id": snipe_client.find_or_create_model(system_info['os_name']),
            "status_id": 2,
            "company_id": company_id,
            "site_id": site_id,
            "custom_fields": custom_fields
        }
        snipe_client.create_asset(payload)
