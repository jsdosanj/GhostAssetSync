# GhostAssetSync


Looking to build a cross-platform CLI app (Mac + Windows) that:
1. Collects device metadata (Device Name, OS, Serial, MAC, Users, AD Group/OU, etc.).
2. Checks if the serial exists in Snipe-IT.
3. Syncs or creates an asset using Snipe-IT’s API, matching models by name.
4. Treats Snipe-IT as source-of-truth for asset tags.
5. Follows logic for fallback asset tag generation (4+ digit name, else CASID-<number>).
6. Configurable via settings.conf (API keys, endpoints, fields, etc.).
7. Deployable via JAMF (Mac) and GPO/SCCM (Windows) – low-dependency or self-contained.

 This will use Python 3 for cross-platform compatibility with:
 1. 🪟 Windows: GPO-friendly with py2exe or pyinstaller.
 2. 🍎 Mac: JAMF-friendly via a compiled CLI or script.

 📦 Dependencies:
 1. requests: for HTTP with Snipe-IT API
 2. plistlib / subprocess / platform: for system info
 3. configparser: for .conf config parsing
 4. pyobjc (optional Mac-specific)

🧊 Packaging (Build for Deployment)
1. Windows (GPO-ready): pyinstaller --onefile main.py
2. macOS (JAMF-ready): py2app / create PKG from Python script

All you need:
1. Drop config + script on target devices.
2. Schedule with JAMF / GPO / cron / scheduled task.
