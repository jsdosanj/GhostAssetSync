import os
import requests
from src.utils import generate_asset_tag

def post_to_teams(webhook_url, title, message, color="00FF00"):
    if not webhook_url:
        return  # silently skip if not configured
    payload = {
        "@type": "MessageCard",
        "@context": "https://schema.org/extensions",
        "summary": title,
        "themeColor": color,
        "title": title,
        "text": message
    }
    try:
        r = requests.post(webhook_url, json=payload, timeout=15)
        r.raise_for_status()
    except Exception as e:
        print(f"[Teams Alert Error] {e}")

def sync_to_snipe(system_info, jamf_asset, snipe_client, site_id, company_id, webhook_url=""):
    serial = system_info['serial']
    hostname = system_info['hostname']
    # Allow env var to override
    webhook_url = os.getenv("TEAMS_WEBHOOK_URL", "") or webhook_url

    try:
        asset = snipe_client.find_asset_by_serial(serial)

        custom_fields = {
            "Operating System": system_info['os_name'],
            "OS Version": system_info['os_version'],
            "OS Build": system_info['os_build'],
            "MAC Address": system_info['mac_address'],
            "Logged In Users": system_info['logged_in_users'],
        }

        if asset:
            print(f"Updating existing asset [{serial}] in Snipe")
            payload = {
                "name": hostname,
                "custom_fields": custom_fields,
                "asset_tag": asset["asset_tag"]
            }
            snipe_client.update_asset(asset["id"], payload)

            post_to_teams(
                webhook_url,
                f"Asset Updated: {hostname}",
                f"Updated asset with serial: `{serial}` and tag: `{asset['asset_tag']}`"
            )
        else:
            print(f"Creating new asset [{serial}] in Snipe")
            asset_tag = generate_asset_tag(serial, hostname)
            model_id = snipe_client.find_or_create_model(system_info['os_name'])

            payload = {
                "name": hostname,
                "serial": serial,
                "asset_tag": asset_tag,
                "model_id": model_id,
                "status_id": 2,
                "company_id": company_id,
                "site_id": site_id,
                "custom_fields": custom_fields
            }

            snipe_client.create_asset(payload)

            post_to_teams(
                webhook_url,
                f"Asset Created: {hostname}",
                f" Created new asset with serial: `{serial}` and tag: `{asset_tag}`"
            )
    except Exception as e:
        error_msg = f" Asset Sync Failed for `{hostname}` ({serial})\n```\n{str(e)}\n```"
        print(error_msg)
        post_to_teams(webhook_url, "Asset Sync Failed ", error_msg, color="FF0000")
