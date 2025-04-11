# GhostAssetSync

🔗 **Cross-platform device asset sync tool that pulls system & JAMF info, and syncs it with Snipe-IT using your custom logic.**

---

## 🚀 Features

- ✅ Gathers local device info: Serial, OS, Hostname, MAC, Logged-in Users
- ✅ Queries JAMF Pro API for existing record
- ✅ Matches or creates assets in Snipe-IT (based on Serial Number)
- ✅ If `asset_tag` is blank, auto-generates one from hostname or fallback to `CASID-<serial>`
- ✅ Enforces Snipe-IT as source-of-truth (syncs `asset_tag` back to JAMF if needed)
- ✅ Fully cross-platform: macOS & Windows
- ✅ Deployable via JAMF, GPO, SCCM, Intune, etc.
- ✅ Packaged as `.msi` for Windows, `.pkg` for macOS
- ✅ Microsoft Teams webhook support for sync notifications

---

## 📁 Directory Structure

```
GhostAssetSync/
├── ghostsync.py                # Main script (entrypoint)
├── settings.conf.example       # Configuration sample
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── src/
│   ├── asset_sync.py           # Sync logic
│   ├── jamf_client.py          # JAMF Pro API wrapper
│   ├── snipeit_client.py       # Snipe-IT API wrapper
│   ├── system_info.py          # Local OS info collector
│   ├── utils.py                # Helper functions

```

⚙️ Setup
1. Clone Repo
```
git clone https://github.com/YOURORG/GhostAssetSync.git
cd GhostAssetSync
```

2. Configure Credentials
```
cp settings.conf.example settings.conf
```

Edit settings.conf with:
```[DEFAULT]
snipe_url = https://yoursnipe.it/api/v1
snipe_token = YOUR_SNIPE_API_KEY
jamf_url = https://your.jamf.instance.com
jamf_user = your_jamf_api_user
jamf_password = your_jamf_api_password
site_id = 1
company_id = 1
teams_webhook_url = https://outlook.office.com/webhook/XXXXXX
```

🚦 Usage
```python ghostsync.py ```

🔐 Packaging
macOS .pkg
```
pyinstaller --onefile ghostsync.py
productbuild --component dist/ghostsync /usr/local/bin GhostAssetSync.pkg
```
Windows .msi
```
pyinstaller --onefile ghostsync.py
# Use WiX Toolset or NSIS to wrap ghostsync.exe into an MSI
```
Built binaries can be deployed silently via JAMF or GPO.

📬 Teams Webhook Notifications (Optional)

To enable Microsoft Teams integration:
1. Add a webhook URL to your settings.conf under teams_webhook_url.
2. The sync process will POST a message on:
- Asset Created
- Asset Updated
- Errors/Failures

🧼 Best Practices
- Never commit settings.conf with real credentials.
- Use settings.conf.example for version control.
- Consider using environment variables or a secret manager in production.
