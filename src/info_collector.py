import platform
import subprocess
import re
import json
import socket
import uuid
import os

def get_serial():
    if platform.system() == "Windows":
        return subprocess.check_output("wmic bios get serialnumber", shell=True).decode().split("\n")[1].strip()
    else:
        return subprocess.check_output("system_profiler SPHardwareDataType | awk '/Serial/ {print $4}'", shell=True).decode().strip()

def get_hostname():
    return socket.gethostname()

def get_os_info():
    system = platform.system()
    version = platform.version()
    release = platform.release()
    return system, release, version

def get_mac_address():
    mac = hex(uuid.getnode()).replace('0x', '').upper()
    return ':'.join(mac[i:i+2] for i in range(0, 12, 2))

def get_logged_in_users():
    if platform.system() == "Windows":
        return subprocess.check_output("query user", shell=True).decode().strip()
    else:
        return subprocess.check_output("users", shell=True).decode().strip()

def get_ad_info():
    if platform.system() == "Windows":
        try:
            return subprocess.check_output('dsquery computer -name %COMPUTERNAME%', shell=True).decode().strip()
        except:
            return "N/A"
    else:
        return "N/A"  # Could use directory services APIs for deep AD info

def collect_all():
    system, os_build, os_version = get_os_info()
    return {
        "hostname": get_hostname(),
        "os_name": system,
        "os_version": os_version,
        "os_build": os_build,
        "mac_address": get_mac_address(),
        "serial": get_serial(),
        "logged_in_users": get_logged_in_users(),
        "ad_group": get_ad_info(),
    }
