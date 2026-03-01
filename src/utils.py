import re


def extract_asset_tag_from_name(name):
    if not isinstance(name, str) or not name:
        return None
    match = re.search(r'\d{4,}', name)
    return match.group(0) if match else None


def generate_asset_tag(serial, hostname):
    if not isinstance(serial, str) or len(serial) < 6:
        serial = "000000"
    if not isinstance(hostname, str):
        hostname = ""
    return extract_asset_tag_from_name(hostname) or f"CASID-{serial[-6:]}"
