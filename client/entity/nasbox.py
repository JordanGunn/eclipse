import re
import socket
import subprocess
from typing import Union

from .entity import Entity
from .entity_attrs import EntityName
from client.eclipse_config import NativeOS


class Nasbox(Entity):

    @staticmethod
    def create(path: str) -> '_Nasbox':

        """Create Nasbox subclass based on native operating system."""

        if NativeOS.IS_UNSUPPORTED_OS:
            raise ValueError(f"Unsupported Operating System: '{NativeOS.OS}'")
        if NativeOS.IS_WINDOWS:
            return NasboxWindows(drive_letter=path)
        if NativeOS.IS_LINUX:
            return NasboxLinux(network_path=path)


class _Nasbox(Entity):

    def __init__(self, network_path: str = ""):
        super().__init__()
        self.name = EntityName.NASBOX

        self._network_path = ""
        self._nas_name = ""
        self._location = ""
        self._ipv4_addr = ""
        self.capacity_gb_ = float("nan")

        if network_path:
            self.network_path = network_path

    @property
    def nas_name(self) -> str:
        return self._nas_name

    @nas_name.setter
    def nas_name(self, nas_name: str):
        self._nas_name = nas_name

    @property
    def network_path(self) -> str:
        return self._nas_name

    @network_path.setter
    def network_path(self, network_path: str):
        """Abstract Method"""
        pass

    @property
    def location(self) -> str:
        return self._location

    @location.setter
    def location(self, location: str):
        self._location = location

    @property
    def ipv4_addr(self) -> str:
        return self._ipv4_addr

    @ipv4_addr.setter
    def ipv4_addr(self, ipv4_addr: str):
        try:  # Check if nas_location is a valid IPv4 address
            socket.inet_aton(ipv4_addr)
            self._ipv4_addr = ipv4_addr
        except socket.error:  # not an IPv4 address, treat as network drive
            self._ipv4_addr = ""

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


class NasboxLinux(_Nasbox):

    def __init__(self, network_path: str = ""):
        super().__init__()

        if self.network_path:
            self.network_path = network_path

    @property
    def network_path(self) -> str:
        return self._network_path

    @network_path.setter
    def network_path(self, network_path: str):
        """
        Resolve a Unix network path to an IP address.

        :param network_path: The network path (e.g., '192.168.1.100:/shared_folder')
        :return: The IP address if resolved, None otherwise.
        """
        # Extract the hostname or IP part from the network path
        match = re.match(r"([^:/]+)", network_path)
        if not match:
            raise ValueError(f"Invalid network path: {network_path}")

        # Resolve the hostname to an IP address
        self.network_path = network_path
        network_address = match.group(1)
        try:
            ip_address = socket.gethostbyname(network_address)
            self._ipv4_addr = ip_address
        except socket.error:
            raise ConnectionError(f"Failed to derive IPv4 Address: {socket.error}")


class NasboxWindows(_Nasbox):

    def __init__(self, drive_letter: str = ""):
        super().__init__()

        self._drive_letter = ""
        if drive_letter:
            self.drive_letter = drive_letter
            self.network_path = self.drive_letter_to_unc_path(self.drive_letter)
            self._ipv4_addr = self.unc_path_to_ip(self.network_path)

    @property
    def network_path(self):
        return self._network_path

    @network_path.setter
    def network_path(self, unc_path: str):
        if self.is_unc_path(unc_path):
            self._network_path = unc_path
            self._ipv4_addr = self.unc_path_to_ip(unc_path)
        else:
            raise ValueError(f"Invalid UNC path: '{unc_path}'")

    @property
    def drive_letter(self):
        return self._drive_letter

    @drive_letter.setter
    def drive_letter(self, drive_letter: str):
        self._drive_letter = drive_letter.upper()
        if not drive_letter.endswith(":"):
            drive_letter += ":"

        # update relevant properties
        unc_path = self.drive_letter_to_unc_path(drive_letter)
        self.network_path = unc_path

    @property
    def ipv4_addr(self) -> str:
        """ """
        return self._ipv4_addr

    @staticmethod
    def is_unc_path(unc_path: str) -> bool:
        """

        :param unc_path:
        :return:
        """

        # Pattern for UNC path with IPv4: \\192.168.1.1\share
        pattern = r"^\\\\(\d{1,3}\.){3}\d{1,3}\\[\w.-]+"

        if re.match(pattern, unc_path):
            # Further validate each octet in the IPv4 address
            octets = unc_path.split("\\")[2].split(".")
            for octet in octets:
                if not 0 <= int(octet) <= 255:
                    return False
            return True
        else:
            return False

    @staticmethod
    def _is_drive_path(drive_path: str) -> bool:
        """
        Validate if the string is a correctly formatted Windows drive path.
        """

        return bool(re.match(r"[a-zA-Z]:\\", drive_path))

    @staticmethod
    def unc_path_to_ip(unc_path: str = "") -> Union[str, None]:
        """
        Resolve a Windows network drive letter to an IP address.

        :param unc_path: The drive letter to resolve (e.g., 'Z:')
        :return: The IP address if resolved, None otherwise.
        """

        try:
            # Run 'net use' command to get network drive details
            result = subprocess.check_output(['net', 'use'], universal_newlines=True)
            # Search for the UNC path in the command output
            match = re.search(rf"{unc_path}\s+([^ ]+)", result, re.IGNORECASE)
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
    def drive_letter_to_unc_path(drive_letter: str) -> str:
        """

        :param drive_letter:
        :return:
        """

        # Running 'net use' command and capturing its output
        result = subprocess.run(["net", "use"], capture_output=True, text=True)

        # Parsing the output to find the network path
        pattern = re.compile(rf"{re.escape(drive_letter)}\s+([^\s]+)")
        match = pattern.search(result.stdout)

        if match:
            return match.group(1)  # This should be the network path
        else:
            return ""






