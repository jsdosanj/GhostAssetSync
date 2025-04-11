import re

def extract_asset_tag_from_name(hostname):
    match = re.search(r'\d{4,}', hostname)
    if match:
        return match.group(0)
    return None

def generate_asset_tag(serial, hostname):
    tag = extract_asset_tag_from_name(hostname)
    return tag if tag else f"CASID-{serial[-6:]}"
