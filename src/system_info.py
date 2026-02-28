import platform
import subprocess
import socket
import uuid

def get_serial():
    try:
        if platform.system() == "Windows":
            return subprocess.check_output("wmic bios get serialnumber", shell=True).decode().split("\n")[1].strip()
        return subprocess.check_output("system_profiler SPHardwareDataType | awk '/Serial/ {print $4}'", shell=True).decode().strip()
    except Exception:
        return "UNKNOWN"

def get_mac_address():
    mac = hex(uuid.getnode()).replace('0x', '').upper()
    return ':'.join(mac[i:i+2] for i in range(0, 12, 2))

def get_logged_in_users():
    try:
        return subprocess.check_output("query user" if platform.system() == "Windows" else "users", shell=True).decode().strip()
    except Exception:
        return "UNKNOWN"

def collect_system_info():
    return {
        "hostname": socket.gethostname(),
        "serial": get_serial(),
        "mac_address": get_mac_address(),
        "os_name": platform.system(),
        "os_version": platform.version(),
        "os_build": platform.release(),
        "logged_in_users": get_logged_in_users()
    }
