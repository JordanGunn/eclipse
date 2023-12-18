import os
import sys
import ctypes
import psutil
from stat import FILE_ATTRIBUTE_HIDDEN


# ====================================
# MISC CONSTANTS
# ====================================
CONVERT_GB = 1024.0 ** 3
ECLIPSE_TEMP_DIR = ".eclipse_temp"
# ------------------------------------


# ====================================
# NETWORK CONSTANTS
# ====================================

class _Port:
    """Commonly used port numbers."""
    class PRIVATE:
        """
        Range of private ports generally not assigned to any standard service.

        NOTE: A good choice if we wish to avoid conflicts entirely.
        """

        P_49152 = 49152
        P_65535 = 65535

    class FORBIDDEN:
        """Forbidden port numbers."""
        class WellKnown:
            """Well-known ports (Reserved for standard services)"""

            P_0000 = 0
            P_1023 = 1023

    P_8000 = 8000
    P_8080 = 8080

    DEFAULT = P_8000


class _Host:

    """Commonly used hostnames and IP addresses."""

    LOCALHOST = "localhost"
    LOOPBACK_ADDR = "127.0.0.1"
    NET_INTERFACE_ALL = "0.0.0.0"

    DEFAULT = LOOPBACK_ADDR


class NetworkConfig:
    """
    Enum class encapsulating constants for Hostnames, IPs and, Port Numbers.

    Accessing a port number:
    >>> NetworkConfig.PORT.DEFAULT
    >>> NetworkConfig.PORT.P_8000

    Accessing a hostname or IP:
    >>> NetworkConfig.HOST.DEFAULT
    >>> NetworkConfig.HOST.LOCALHOST
    """

    PORT = _Port
    HOST = _Host

# ------------------------------------


# ====================================
# SYSTEM CONSTANTS
# ====================================
class SupportedOS:
    """Supported operating systems."""

    LINUX = "linux"
    LINUX2 = "linux2"
    WINDOWS = "windows"
    WIN32 = 'win32'
    LIST = [LINUX, LINUX2, WINDOWS]


class NativeOS:
    OS = sys.platform.lower()
    IS_UNSUPPORTED_OS = (OS not in SupportedOS.LIST)
    IS_WINDOWS = (OS == SupportedOS.WINDOWS or SupportedOS.WIN32) 
    IS_LINUX = (OS == SupportedOS.LINUX) or (sys.platform == SupportedOS.LINUX2)
    SHELL_EXEC = "/usr/bin/zsh" if IS_LINUX else None
# ------------------------------------


# ====================================
# APP DATA CONSTANTS
# ====================================
APP_DATA_DIR = "." + os.path.sep + "data"
GEOBC_LOGO_DATA = "geobc_logo.b64"
# Base64 encoding of the icon for the Province of BC
os.chdir(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)
with open(APP_DATA_DIR + os.path.sep + GEOBC_LOGO_DATA, "r") as logo:
    try:
        BC_LOGO_B64 = logo.read()
    except (FileNotFoundError, NotADirectoryError):
        BC_LOGO_B64 = ""
# ------------------------------------


def temp_hidden_dir(parent_dir):
    """
    Defines path to temporary, hidden directory.
    Creates the directory if it doesn't exist.

    Args:
        parent_dir (str):
            - Path to parent directory of the temp directory.

    Returns:
        (str):
            - Path to the hidden temp directory.
    """

    temp_dir = os.path.join(parent_dir, ECLIPSE_TEMP_DIR)
    if not os.path.isdir(temp_dir):
        os.mkdir(temp_dir)
        ctypes.windll.kernel32.SetFileAttributesW(temp_dir, FILE_ATTRIBUTE_HIDDEN)
    return temp_dir


def total_ram():

    """
    Check the amount of RAM on the machine.

    Used to dynamically adjust the amount of cores being used during
    processing to deal with RAM overflow when processing many large
    files concurrently.
    """

    if IS_LINUX:
        total_bytes = os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES')
    else:
        total_bytes = int(psutil.virtual_memory().total)

    gigabytes = total_bytes / CONVERT_GB
    return gigabytes
