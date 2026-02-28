#!/usr/bin/env python3
"""GhostAssetSync — Cross-platform device asset sync tool."""

import configparser
import os
import sys

from src.system_info import collect_system_info
from src.jamf_client import JamfClient
from src.snipeit_client import SnipeClient
from src.asset_sync import sync_to_snipe


def main():
    # Resolve config relative to this script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, "settings.conf")

    if not os.path.isfile(config_path):
        print(f"[ERROR] Config file not found: {config_path}")
        print("Copy settings.conf.example to settings.conf and fill in your credentials.")
        sys.exit(1)

    config = configparser.ConfigParser()
    config.read(config_path)

    try:
        c = config["DEFAULT"]
        jamf_url = c["jamf_url"]
        jamf_user = c["jamf_user"]
        jamf_password = c["jamf_password"]
        snipe_url = c["snipe_url"]
        snipe_token = c["snipe_token"]
        site_id = int(c["site_id"])
        company_id = int(c["company_id"])
        webhook_url = c.get("teams_webhook_url", "")
    except KeyError as e:
        print(f"[ERROR] Missing required config key: {e}")
        print("Check your settings.conf against settings.conf.example.")
        sys.exit(1)

    # Init clients
    jamf = JamfClient(jamf_url, jamf_user, jamf_password)
    snipe = SnipeClient(snipe_url, snipe_token)

    # Step 1: Collect local system info
    print("[*] Collecting local system info...")
    sys_info = collect_system_info()
    print(f"    Hostname: {sys_info['hostname']}")
    print(f"    Serial:   {sys_info['serial']}")

    # Step 2: Pull JAMF info by serial
    print("[*] Querying JAMF Pro for device record...")
    try:
        jamf_assets = jamf.get_computers()
        jamf_asset = next(
            (j for j in jamf_assets if j.get("serial_number") == sys_info["serial"]),
            {},
        )
    except Exception as e:
        print(f"[WARN] Failed to query JAMF: {e}")
        jamf_asset = {}

    # Step 3: Sync to Snipe-IT
    print("[*] Syncing to Snipe-IT...")
    sync_to_snipe(sys_info, jamf_asset, snipe, site_id, company_id, webhook_url)

    print("[✓] GhostAssetSync complete.")


if __name__ == "__main__":
    main()
