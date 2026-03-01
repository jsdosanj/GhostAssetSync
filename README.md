# GhostAssetSync

**Cross-platform device asset sync tool that pulls system & JAMF info, and syncs it with Snipe-IT using your custom logic.**

---

## Features

- Gathers local device info: Serial, OS, Hostname, MAC, Logged-in Users
- Queries JAMF Pro API for existing record
- Matches or creates assets in Snipe-IT (based on Serial Number)
- If `asset_tag` is blank, auto-generates one from hostname or fallback to `CASID-<serial>`
- Enforces Snipe-IT as source-of-truth (syncs `asset_tag` back to JAMF if needed)
- Fully cross-platform: macOS & Windows
- Deployable via JAMF, GPO, SCCM, Intune, etc.
- Packaged as `.exe` for Windows, binary for macOS
- Microsoft Teams webhook support for sync notifications

---

## Prerequisites

- Python 3.9 or higher
- Network access to JAMF Pro and Snipe-IT APIs

---

## Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/jsdosanj/GhostAssetSync.git
cd GhostAssetSync

# 2. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Copy and configure settings
cp settings.conf.example settings.conf

# 5. Edit settings.conf with your credentials
# (see Configuration section below)

# 6. Run
python ghostsync.py
```

---

## Configuration

Copy `settings.conf.example` to `settings.conf` and fill in your values:

```ini
[DEFAULT]
snipe_url = https://yoursnipe.it/api/v1
snipe_token = YOUR_SNIPE_API_KEY
jamf_url = https://your.jamf.instance.com
jamf_user = your_jamf_api_user
jamf_password = your_jamf_api_password
site_id = 1
company_id = 1
teams_webhook_url = https://outlook.office.com/webhook/XXXXXX
```

| Key | Required | Description |
|-----|----------|-------------|
| `snipe_url` | Yes | Snipe-IT API base URL |
| `snipe_token` | Yes | Snipe-IT API bearer token |
| `jamf_url` | Yes | JAMF Pro server URL |
| `jamf_user` | Yes | JAMF Pro API username |
| `jamf_password` | Yes | JAMF Pro API password |
| `site_id` | Yes | Snipe-IT site ID |
| `company_id` | Yes | Snipe-IT company ID |
| `teams_webhook_url` | No | Microsoft Teams incoming webhook URL |

---

## How It Works

1. **Collect system info** — hostname, serial number, MAC address, OS details, logged-in users
2. **Query JAMF Pro** — look up the device record by serial number
3. **Search Snipe-IT** — check if an asset with that serial already exists
4. **Create or update asset** — create a new asset or update the existing one with current data
5. **Send Teams notification** — post a success or failure card to the configured webhook

---

## Directory Structure

```
GhostAssetSync/
├── ghostsync.py                # Main script (entrypoint)
├── settings.conf.example       # Configuration sample
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── .github/
│   └── workflows/
│       └── build.yml           # CI/CD workflow
└── src/
    ├── __init__.py             # Package marker
    ├── asset_sync.py           # Sync logic
    ├── jamf_client.py          # JAMF Pro API wrapper
    ├── snipeit_client.py       # Snipe-IT API wrapper
    ├── system_info.py          # Local OS info collector
    └── utils.py                # Helper functions
```

---

## Packaging & Deployment

### macOS

```bash
pip install pyinstaller
pyinstaller --onefile ghostsync.py
# Binary is at dist/ghostsync
```

### Windows

```powershell
pip install pyinstaller
pyinstaller --onefile ghostsync.py
# Executable is at dist\ghostsync.exe
```

Built binaries can be deployed silently via JAMF or GPO.

---

## Microsoft Teams Notifications

To enable Microsoft Teams integration:

1. Create an incoming webhook in your Teams channel.
2. Add the webhook URL to `settings.conf` under `teams_webhook_url`.

The sync process will POST a notification card on:

- Asset Created
- Asset Updated
- Errors / Failures

---

## Environment Variables

All secrets can be supplied via environment variables (these take precedence over `settings.conf`):

| Variable | Description |
|----------|-------------|
| `GHOST_JAMF_URL` | Overrides `jamf_url` from `settings.conf` |
| `GHOST_JAMF_USER` | Overrides `jamf_user` from `settings.conf` |
| `GHOST_JAMF_PASSWORD` | Overrides `jamf_password` from `settings.conf` |
| `GHOST_SNIPE_URL` | Overrides `snipe_url` from `settings.conf` |
| `GHOST_SNIPE_TOKEN` | Overrides `snipe_token` from `settings.conf` |
| `TEAMS_WEBHOOK_URL` | Overrides `teams_webhook_url` from `settings.conf` |

---

## Troubleshooting

**Missing config file**
```
[ERROR] Config file not found: /path/to/settings.conf
```
Run `cp settings.conf.example settings.conf` and fill in your credentials.

**Import errors (`ModuleNotFoundError`)**
Ensure you are running from the repository root and that `src/__init__.py` exists.

**API authentication failures**
Double-check `jamf_user`, `jamf_password`, and `snipe_token` in `settings.conf`. Verify network access to both APIs.

---

## Security

- **Config file permissions**: On Unix, `settings.conf` must not be world-readable. Run `chmod 600 settings.conf` after creation. GhostAssetSync will refuse to start if the file is world-readable, and warns if it is group-readable.
- **Environment variables**: In production, supply all secrets via environment variables (`GHOST_JAMF_URL`, `GHOST_JAMF_USER`, `GHOST_JAMF_PASSWORD`, `GHOST_SNIPE_URL`, `GHOST_SNIPE_TOKEN`, `TEAMS_WEBHOOK_URL`) instead of storing them in `settings.conf`.
- **HTTPS enforcement**: All API URLs (Snipe-IT, JAMF Pro, Teams webhook) must use HTTPS. The tool will refuse to start or skip notifications if HTTP is used (localhost/127.0.0.1 are exempt for local development).
- **Serial number masking**: Serial numbers are masked in log output and Teams notifications (only the last 4 characters are shown). Full serial is available at DEBUG log level only.
- **No stack trace leakage**: Error details are logged locally only. Teams failure notifications send a generic message without exposing internal error details.
- **Reporting vulnerabilities**: Please open a GitHub issue marked `[SECURITY]` or contact the repository owner directly. Do not disclose security vulnerabilities publicly until a fix is available.
- Never commit `settings.conf` with real credentials — it is listed in `.gitignore`.
- Use `settings.conf.example` for version control.

---

## Contributing

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/my-change`).
3. Commit your changes with a clear message.
4. Open a pull request against `main`.

---

## License

This project is licensed under the MIT License.

