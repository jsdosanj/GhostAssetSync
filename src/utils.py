import re


def extract_asset_tag_from_name(name):
    if not isinstance(name, str) or not name:
        return None
    match = re.search(r'\d{4,}', name)
    return match.group(0) if match else None


def generate_asset_tag(serial, hostname):
    if not isinstance(hostname, str):
        hostname = ""

    hostname_tag = extract_asset_tag_from_name(hostname)
    if hostname_tag:
        return hostname_tag

    if not isinstance(serial, str):
        serial = str(serial) if serial is not None else ""

    # Use the last 6 characters of the serial, zero-padding if it is shorter than 6
    normalized_serial = serial[-6:].zfill(6) if serial else "000000"
    return f"CASID-{normalized_serial}"
