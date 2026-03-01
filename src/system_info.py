import platform
import subprocess
import socket
import uuid
import logging

logger = logging.getLogger(__name__)


def get_serial():
    try:
        if platform.system() == "Windows":
            result = subprocess.check_output(
                ["wmic", "bios", "get", "serialnumber"],
                shell=False,
                timeout=10
            ).decode().split("\n")[1].strip()
            return result if result else "UNKNOWN"
        result = subprocess.check_output(
            ["system_profiler", "SPHardwareDataType"],
            shell=False,
            timeout=10
        ).decode()
        for line in result.splitlines():
            if "Serial Number" in line:
                return line.split(":")[-1].strip()
        return "UNKNOWN"
    except Exception as e:
        logger.debug("Failed to get serial: %s", e)
        return "UNKNOWN"


def get_mac_address():
    mac = hex(uuid.getnode()).replace('0x', '').upper()
    return ':'.join(mac[i:i+2] for i in range(0, 12, 2))


def get_logged_in_users():
    try:
        if platform.system() == "Windows":
            return subprocess.check_output(
                ["query", "user"],
                shell=False,
                timeout=10
            ).decode().strip()
        return subprocess.check_output(
            ["users"],
            shell=False,
            timeout=10
        ).decode().strip()
    except Exception as e:
        logger.debug("Failed to get logged-in users: %s", e)
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
