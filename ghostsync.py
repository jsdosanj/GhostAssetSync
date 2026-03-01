#!/usr/bin/env python3
"""GhostAssetSync — Cross-platform device asset sync tool."""

import configparser
import logging
import os
import stat
import sys
from urllib.parse import urlparse

from src.system_info import collect_system_info
from src.jamf_client import JamfClient
from src.snipeit_client import SnipeClient
from src.asset_sync import sync_to_snipe

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
)
logger = logging.getLogger(__name__)


def _validate_url(url, name):
    parsed = urlparse(url)
    if parsed.scheme == "https":
        return
    if parsed.scheme in ("http", "") and parsed.hostname in ("localhost", "127.0.0.1", "::1"):
        return
    logger.error("[SECURITY] %s must use HTTPS: %s", name, url)
    sys.exit(1)


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, "settings.conf")

    if not os.path.isfile(config_path):
        logger.error("Config file not found: %s", config_path)
        logger.error("Copy settings.conf.example to settings.conf and fill in your credentials.")
        sys.exit(1)

    if os.name != 'nt':
        file_stat = os.stat(config_path)
        if file_stat.st_mode & stat.S_IROTH:
            logger.error("[SECURITY] settings.conf is world-readable. Run: chmod 600 settings.conf")
            sys.exit(1)
        if file_stat.st_mode & stat.S_IRGRP:
            logger.warning("[SECURITY] settings.conf is group-readable. Consider: chmod 600 settings.conf")

    config = configparser.ConfigParser()
    config.read(config_path)

    try:
        c = config["DEFAULT"]
        jamf_url = os.environ.get("GHOST_JAMF_URL") or c["jamf_url"]
        jamf_user = os.environ.get("GHOST_JAMF_USER") or c["jamf_user"]
        jamf_password = os.environ.get("GHOST_JAMF_PASSWORD") or c["jamf_password"]
        snipe_url = os.environ.get("GHOST_SNIPE_URL") or c["snipe_url"]
        snipe_token = os.environ.get("GHOST_SNIPE_TOKEN") or c["snipe_token"]
        site_id = int(c["site_id"])
        company_id = int(c["company_id"])
        webhook_url = os.environ.get("TEAMS_WEBHOOK_URL") or c.get("teams_webhook_url", "")
    except KeyError as e:
        logger.error("Missing required config key: %s", e)
        logger.error("Check your settings.conf against settings.conf.example.")
        sys.exit(1)
    except ValueError as e:
        logger.error("Invalid config value (site_id/company_id must be integers): %s", e)
        sys.exit(1)

    if site_id <= 0 or company_id <= 0:
        logger.error("site_id and company_id must be positive integers.")
        sys.exit(1)

    _validate_url(jamf_url, "jamf_url")
    _validate_url(snipe_url, "snipe_url")
    if webhook_url:
        _validate_url(webhook_url, "teams_webhook_url")

    jamf = JamfClient(jamf_url, jamf_user, jamf_password)
    snipe = SnipeClient(snipe_url, snipe_token)

    logger.info("Collecting local system info...")
    sys_info = collect_system_info()
    serial = sys_info['serial']
    logger.info("  Hostname: %s", sys_info['hostname'])
    logger.info("  Serial:   ****%s", serial[-4:] if len(serial) >= 4 else serial)
    logger.debug("  Serial (full): %s", serial)

    logger.info("Querying JAMF Pro for device record...")
    try:
        jamf_assets = jamf.get_computers()
        jamf_asset = next(
            (j for j in jamf_assets if j.get("serial_number") == sys_info["serial"]),
            {},
        )
    except Exception as e:
        logger.warning("Failed to query JAMF: %s", e)
        jamf_asset = {}

    logger.info("Syncing to Snipe-IT...")
    sync_to_snipe(sys_info, jamf_asset, snipe, site_id, company_id, webhook_url)

    logger.info("GhostAssetSync complete.")


if __name__ == "__main__":
    main()
