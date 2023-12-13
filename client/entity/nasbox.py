import re
import socket
import subprocess
from typing import Union

from .entity import Entity
from .entity_attrs import EntityName
from client.eclipse_config import NativeOS


class Nasbox(Entity):

    @staticmethod
    def create(*args, **kwargs) -> '_Nasbox':

        """Create Nasbox subclass based on native operating system."""

        if NativeOS.IS_UNSUPPORTED_OS:
            raise ValueError(f"Unsupported Operating System: '{NativeOS.OS}'")
        if NativeOS.IS_WINDOWS:
            return NasboxWindows(*args, **kwargs)
        if NativeOS.IS_LINUX:
            return NasboxLinux(*args, **kwargs)


class _Nasbox(Entity):

    def __init__(self):
        super().__init__()
        self.name = EntityName.NASBOX

        self._path = ""
        self._nas_name = ""
        self._location = ""
        self._ipv4_addr = ""
        self.capacity_gb_ = float("nan")

    @property
    def path(self) -> str:
        return self._nas_name

    @path.setter
    def path(self, path: str):
        """Abstract Method for setting various network paths."""
        pass

    @property
    def nas_name(self) -> str:
        return self._nas_name

    @nas_name.setter
    def nas_name(self, nas_name: str):
        self._nas_name = nas_name

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

    ETC_MTAB = '/etc/mtab'
    REGEX_NETWORK_PATH = r'^\d{1,3}(\.\d{1,3}){3}:/.*'

    def __init__(self, path: str = ""):
        super().__init__()

        self._mount_path = ""
        self._network_path = ""

        if path:
            self.path = path

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, path: str):
        """
        Set the network_path or mount_path property.

        Sets a given input path to the network_path or mount_path
        property depending on whether the argument was:
        - A linux network path: '{ipv4_address}:/{shared_folder}'
        - A mounted network path: '/mnt/shared_folder'

        Note the that method will also attempt to set the
        objects 'ipv4_addr' property by deriving it from
        the input 'path' argument.

        :param path: A linux network path or mounted network path.
        :raises ValueError:
        """

        if self.is_mounted_network_path(path=path):
            self.mount_path = path
        elif self.is_linux_network_path(path=path):
            self.network_path = path
        else:
            raise ValueError(f"Given path '{path}' is not valid.")

        # set the 'path' attribute accordingly
        mp = self.mount_path
        np = self.network_path
        self._path = mp if mp else np

    @property
    def mount_path(self):
        """Get the mounted_path property."""

        return self._mount_path

    @mount_path.setter
    def mount_path(self, mount_path: str):
        """Set the mount_path property."""

        self._mount_path = mount_path
        self.ipv4_addr = \
            self._ip_from_mount_path(mount_path)

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

        # Resolve the hostname to an IP address
        self.network_path = network_path
        network_address = match.group(1)
        self.ipv4_addr = \
            self._ip_from_network_path(network_address)

    @staticmethod
    def _ip_from_network_path(network_path: str):
        """

        :param network_path:
        :return:
        """

        try:
            ipv4_addr = socket.gethostbyname(network_path)
        except socket.error:
            ipv4_addr = ""

        return ipv4_addr

    def _get_mounts(self):
        with open(self.ETC_MTAB, 'r') as f:
            mounts = f.readlines()

        network_mounts = []
        for mount in mounts:
            if mount.startswith('//'):
                parts = mount.split()
                network_path = parts[0]
                mount_point = parts[1]
                network_mounts.append((network_path, mount_point))

        return network_mounts

    def is_linux_network_path(self, path: str) -> bool:
        """
        Determine if a given input 'path' is a linux network path.
        Specifically, the method returns True if the 'path' argument
        follows the format: '{ipv4_addr}:/{shared_folder}'.

        E.g., '127.0.0.1:/shared_folder'

        :param path: A given path.
        :return: True or False
        """

        # Pattern to match 'IP:/path'
        pattern = self.REGEX_NETWORK_PATH
        return re.match(pattern, path) is not None

    def is_mounted_network_path(self, path):
        """
        Determine if a given input 'path' is a mounted network path.
        Specifically, the method reads from '/etc/mtab', comparing
        the input 'path' argument against the system registered
        mounted network drives.

        :param path: A given path.
        :return: True or False
        """

        mounts = self._get_mounts()
        for mount in mounts:
            # Check if the given path is a mount point
            if path == mount[1] and mount[0].startswith('//'):
                return True

        return False

    @staticmethod
    def _ip_from_mount_path(mount_path: str):
        """

        :param mount_path:
        :return:
        """

        result = subprocess.run(['mount'], capture_output=True, text=True)
        network_drives = re.findall(r'//(.*?) on (.*?) type', result.stdout)

        for ip, mount_point in network_drives:
            if mount_point == mount_path:
                return ip  # Return the IP or hostname

        return None  # No match found


class NasboxWindows(_Nasbox):

    # Pattern for UNC path with IPv4: '\\192.168.1.1\share'
    REGEX_UNC_PATH = r"^\\\\(\d{1,3}\.){3}\d{1,3}\\[\w.-]+"

    # Pattern for Drive Path: 'C:\\'
    REGEX_DRIVE_PATH = r"[a-zA-Z]:\\"

    def __init__(self, path: str = ""):
        super().__init__()

        self._drive_letter = ""
        self._drive_path = ""
        self._unc_path = ""

        if path:
            self.path = path

    @property
    def path(self):
        """Get the path property."""

        return self._path

    @path.setter
    def path(self, path: str):

        """

        :param path:
        :raises ValueError:
        """

        if self.is_drive_path(path):
            self.drive_path = path
        elif self.is_unc_path(path):
            self.unc_path = path
        else:
            raise ValueError(f"Given path '{path}' is not valid.")

        # set the path accordingly
        dp = self.drive_path
        up = self.unc_path
        self._path = dp if dp else up

    @property
    def drive_letter(self) -> str:
        """Get the drive_letter property."""

        return self._drive_letter

    @drive_letter.setter
    def drive_letter(self, drive_letter: str):
        """

        :param drive_letter:
        :return:
        """

        dl = drive_letter[0]
        if dl.isalpha():
            self._drive_letter = dl
            self.drive_path = dl

    @property
    def unc_path(self):
        """Get the unc_path property."""

        return self._unc_path

    @unc_path.setter
    def unc_path(self, unc_path: str):
        """

        :param unc_path:
        :return:
        """

        self._unc_path = unc_path
        self.ipv4_addr = self.unc_path_to_ip(unc_path)

    @property
    def drive_path(self):
        """Get the drive path property."""

        return self._drive_path

    @drive_path.setter
    def drive_path(self, drive_path: str):
        """

        :param drive_path:
        :return:
        """

        if self.drive_letter != drive_path[0]:
            self.drive_letter = drive_path
        if not drive_path.endswith(r":\\"):
            drive_path += r":\\"
        # update relevant properties
        self._drive_path = drive_path
        self.unc_path = \
            self.drive_letter_to_unc_path(drive_path)

    def is_unc_path(self, unc_path: str) -> bool:
        """

        :param unc_path:
        :return:
        """

        pattern = self.REGEX_UNC_PATH

        if re.match(pattern, unc_path):
            # Further validate each octet in the IPv4 address
            octets = unc_path.split("\\")[2].split(".")
            for octet in octets:
                if not 0 <= int(octet) <= 255:
                    return False
            return True
        else:
            return False

    def is_drive_path(self, drive_path: str) -> bool:
        """Validate if the string is a correctly formatted Windows drive path."""

        return bool(re.match(self.REGEX_DRIVE_PATH, drive_path))

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
        pattern = re.compile(rf"{re.escape(drive_letter)}\s+(\S+)")
        match = pattern.search(result.stdout)

        if match:
            return match.group(1)  # This should be the network path
        else:
            return ""
