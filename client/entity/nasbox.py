import re
import socket
import platform
import subprocess
from typing import Union, Optional

from .entity import Entity
from .entity_attrs import EntityName


LINUX_OS = "linux"
LINUX2_OS = "linux2"
WINDOWS_OS = "windows"


class Nasbox(Entity):

    def __init__(self, nas_name: Optional[str] = "", location: Optional[str] = "", ipv4_addr: Optional[str] = "", capacity_gb: Optional[float] = ""):
        super().__init__()
        self.name = EntityName.NASBOX

        self._mapped_drive = ""
        self.nas_name_ = nas_name if nas_name else ""
        self.location_ = location if location else ""
        self.ipv4_addr_ = ipv4_addr if ipv4_addr else ""
        self.capacity_gb_ = capacity_gb if capacity_gb else float("nan")

    @property
    def nas_name(self) -> str:
        return self.nas_name_

    @nas_name.setter
    def nas_name(self, nas_name: str):
        self.nas_name_ = nas_name

    @property
    def location(self) -> str:
        return self.location_

    @location.setter
    def location(self, location: str):
        self.location_ = location

    @property
    def ipv4_addr(self) -> str:
        return self.ipv4_addr_

    @ipv4_addr.setter
    def ipv4_addr(self, ipv4_addr: str):
        self.ipv4_addr_ = ipv4_addr

    @property
    def capacity_gb(self) -> float:
        return self.capacity_gb_

    @capacity_gb.setter
    def capacity_gb(self, capacity_gb: Union[float, str]):

        if isinstance(capacity_gb, str) and capacity_gb.isnumeric():
            self.capacity_gb_ = float(capacity_gb)
        elif isinstance(capacity_gb, float):
            self.capacity_gb_ = capacity_gb
        else:
            raise ValueError("Argument must of of type 'float' or 'string'")

    def set_ipv4_addr(self, nas_location: str):
        """
        Set the ipv4 address of the Nasbox Entity.

        Sets the IP address of the Nasbox entity via one of two
        possible options for the argument 'nas_location':
            - Mapped network drive (e.g. Z:\\mapped\\path)
            - IPv4 Network Address

        If an incorrectly formatted IPv4 address, or an invalid
        network drive is passed, method will raise a ValueError

        :param nas_location: ipv4 network address OR mapped network drive
        :raise ValueError:
        :return: None
        """

        native_os = platform.system().lower()

        try:  # Check if nas_location is a valid IPv4 address
            socket.inet_aton(nas_location)
            self.ipv4_addr = nas_location
        except socket.error:  # not an IPv4 address, treat as network drive
            if native_os == WINDOWS_OS:
                if not self._is_valid_windows_drive(nas_location):
                    raise ValueError(f"Invalid Windows network drive: {nas_location}")
                # IP addr from windows network path
                self._mapped_drive = nas_location
                self.ipv4_addr = self.windows_network_path_to_ip(nas_location)
            elif native_os in [LINUX_OS, LINUX2_OS]:
                # IP addr from unix network path
                self.ipv4_addr = self.unix_network_path_to_ip(nas_location)
                raise ValueError("Network drive paths are not supported on Unix")
            else:
                raise ValueError("Unsupported Operating System.")

    @staticmethod
    def _is_valid_windows_drive(drive_str: str):
        """
        Validate if the string is a correctly formatted Windows drive path.
        """
        return re.match(r"[a-zA-Z]:\\", drive_str)

    @staticmethod
    def windows_network_path_to_ip(drive_letter: str) -> Union[str, None]:
        """
        Resolve a Windows network drive letter to an IP address.

        :param drive_letter: The drive letter to resolve (e.g., 'Z:')
        :return: The IP address if resolved, None otherwise.
        """
        try:
            # Run 'net use' command to get network drive details
            result = subprocess.check_output(['net', 'use'], universal_newlines=True)
            # Search for the UNC path in the command output
            match = re.search(rf"{drive_letter}\s+([^ ]+)", result, re.IGNORECASE)
            if not match:
                return None

            # Extract the hostname from the UNC path
            unc_path = match.group(1)
            hostname = re.match(r"\\\\([^\\]+)", unc_path)
            if not hostname:
                return None

            # Resolve the hostname to an IP address
            ip_address = socket.gethostbyname(hostname.group(1))
            return ip_address

        except Exception as e:
            print(f"Error resolving network drive: {e}")
            return None

    @staticmethod
    def unix_network_path_to_ip(network_path: str):
        """
        Resolve a Unix network path to an IP address.

        :param network_path: The network path (e.g., '192.168.1.100:/shared_folder')
        :return: The IP address if resolved, None otherwise.
        """
        # Extract the hostname or IP part from the network path
        match = re.match(r"([^:/]+)", network_path)
        if not match:
            return None

        network_address = match.group(1)
        try:
            # Check if it's already an IP address
            socket.inet_aton(network_address)
            return network_address
        except socket.error:
            # Resolve the hostname to an IP address
            try:
                ip_address = socket.gethostbyname(network_address)
                return ip_address
            except socket.error:
                return None


