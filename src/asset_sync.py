import os
import re
import logging
import requests
from src.utils import generate_asset_tag

logger = logging.getLogger(__name__)

MAX_TEAMS_MSG_LEN = 2000


def _sanitize(value, max_len=255):
    """Remove control characters and truncate."""
    if not isinstance(value, str):
        value = str(value)
    cleaned = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', value)
    return cleaned[:max_len]


def post_to_teams(webhook_url, title, message, color="00FF00"):
    if not webhook_url:
        return
    if not webhook_url.startswith("https://"):
        logger.warning("Teams webhook URL must use HTTPS — skipping notification")
        return
    payload = {
        "@type": "MessageCard",
        "@context": "https://schema.org/extensions",
        "summary": _sanitize(title, 200),
        "themeColor": color,
        "title": _sanitize(title, 200),
        "text": _sanitize(message, MAX_TEAMS_MSG_LEN)
    }
    try:
        r = requests.post(webhook_url, json=payload, timeout=15)
        r.raise_for_status()
    except Exception as e:
        logger.error("Teams webhook POST failed: %s", e)


def sync_to_snipe(system_info, jamf_asset, snipe_client, site_id, company_id, webhook_url=""):
    serial = _sanitize(system_info.get('serial', 'UNKNOWN'))
    hostname = _sanitize(system_info.get('hostname', 'UNKNOWN'))
    webhook_url = os.getenv("TEAMS_WEBHOOK_URL", "") or webhook_url

    try:
        asset = snipe_client.find_asset_by_serial(serial)

        custom_fields = {
            "Operating System": _sanitize(system_info.get('os_name', '')),
            "OS Version": _sanitize(system_info.get('os_version', '')),
            "OS Build": _sanitize(system_info.get('os_build', '')),
            "MAC Address": _sanitize(system_info.get('mac_address', '')),
            "Logged In Users": _sanitize(system_info.get('logged_in_users', '')),
        }

        if asset:
            if not isinstance(asset, dict) or "id" not in asset or "asset_tag" not in asset:
                raise ValueError("Snipe-IT returned an asset with missing 'id' or 'asset_tag' fields")

            logger.info("Updating existing asset [****%s] in Snipe-IT", serial[-4:])
            payload = {
                "name": hostname,
                "custom_fields": custom_fields,
                "asset_tag": asset["asset_tag"]
            }
            snipe_client.update_asset(asset["id"], payload)

            post_to_teams(
                webhook_url,
                f"Asset Updated: {hostname}",
                f"Updated asset with serial: `****{serial[-4:]}` and tag: `{_sanitize(asset['asset_tag'])}`"
            )
        else:
            logger.info("Creating new asset [****%s] in Snipe-IT", serial[-4:])
            asset_tag = generate_asset_tag(serial, hostname)
            model_id = snipe_client.find_or_create_model(system_info.get('os_name', 'Unknown'))

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
                f"Created new asset with serial: `****{serial[-4:]}` and tag: `{asset_tag}`"
            )
    except Exception as e:
        logger.error("Asset sync failed for [****%s]: %s", serial[-4:], e)
        # Send generic message to Teams — do NOT leak stack traces
        post_to_teams(
            webhook_url,
            "Asset Sync Failed",
            f"Sync failed for host `{hostname}`. Check local logs for details.",
            color="FF0000"
        )
