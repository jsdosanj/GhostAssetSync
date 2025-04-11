import re

def extract_asset_tag_from_name(name):
    match = re.search(r'\d{4,}', name)
    return match.group(0) if match else None

def generate_asset_tag(serial, hostname):
    return extract_asset_tag_from_name(hostname) or f"CASID-{serial[-6:]}"
