# system imports
import os
import shutil
import socket
from glob import glob
from pathlib import Path
from urllib.parse import urljoin
from typing import Optional, Union
from tkinter.filedialog import askdirectory

# user imports
from .error import *
from .folder_map import FolderMapDefinition, FolderMapKey
try:
    from client.eclipse_config import NetworkConfig
    from client.eclipse_request import EclipseRequest
    from client.entity import Nasbox, SensorData, Drive
except ImportError:
    from eclipse_config import NetworkConfig
    from eclipse_request import EclipseRequest
    from entity import Nasbox, SensorData, Drive


class EclipseCopy:

    def __init__(
            self, src_dir: str, dst_dir: str, nas_id: Optional[Union[int, str]] = -1,
            delivery_id: Optional[Union[int, str]] = -1, folder_mapping: Optional[FolderMapDefinition] = None
    ):

        """
        Initialize an EclipseCopy object. \n
        \n
        Creates an EclipseCopy object. Note that the only mandatory constructor
        arguments are 'src' and 'dst'. This means that if any other parameters are not
        passed via the constructor, they should be set accordingly before executing
        the copy() method.

        :param src_dir: Source directory (external drive).
        :param dst_dir: Destination directory (network drive).
        :param nas_id: The id number of the NASbox being copied to.
        :param delivery_id: The id number of the delivery associated with the drive.
        :param folder_mapping: The folder mapping definition (e.g. 'from folder_map import KISIK_TO_GEOBC' )
        """

        # handle typing of nas_id
        if isinstance(nas_id, str):
            if nas_id.isnumeric():
                nas_id = int(nas_id)
            else:
                raise ValueError(f"Invalid 'nas_id': {nas_id}")

        # handle typing of delivery_id
        if isinstance(delivery_id, str):
            if delivery_id.isnumeric():
                delivery_id = int(delivery_id)
            else:
                raise ValueError(f"Invalid 'delivery_id': {delivery_id}")

        # string attributes
        self._src_dir = ""
        self._dst_dir = ""
        self._copy_dst = ""
        self._ipv4_addr = ""
        self._drive_letter = ""
        self._network_path = ""

        # int attributes
        self._port = -1
        self._nas_id = -1
        self._delivery_id = -1

        # list attributes
        self._files = []
        self._records = []

        # Entity attributes
        self._drive = None
        self._nasbox = None

        # dict attributes
        self._folder_mapping = folder_mapping

        # Call property setters for actual values passed
        self.src_dir = src_dir
        self.dst_dir = dst_dir
        if nas_id > 0:
            self.nas_id = nas_id
        if delivery_id > 0:
            self.delivery_id = delivery_id

    @property
    def src_dir(self) -> str:

        """Getter for the EclipseCopy src property (copy source)."""

        return self._src_dir

    @src_dir.setter
    def src_dir(self, src: str):

        """
        Setter for the EclipseCopy src property

        :param src: A valid drive path.
        :raises ValueError:
        """

        if not os.path.exists(src):
            raise ValueError(f"Path {src} does not exist.")

        else:  # set the src and update related properties.
            self._src_dir = src
            self._drive = Drive()
            self._drive.set_drive_info(src)
            self._gather_files()

    @property
    def ipv4_addr(self) -> str:

        """Getter for EclipseCopy ip property."""

        return self._ipv4_addr

    @ipv4_addr.setter
    def ipv4_addr(self, ipv4_addr: str):

        if self.is_ipv4_address(ipv4_addr):
            self._ipv4_addr = ipv4_addr
            self._network_path = self._network_path_(self.port, self.ipv4_addr)
        else:
            raise ValueError(f"Invalid IPv4 Address: '{ipv4_addr}'")

    @property
    def dst_dir(self) -> str:

        """Getter for the EclipseCopy dst property (copy destination)."""

        return self._dst_dir

    @dst_dir.setter
    def dst_dir(self, dst: str):

        """
        Setter for the EclipseCopy dst property (Copy Destination).

        :param dst: Copy Destination (IPv4 address or valid network path.)
        :raises ValueError:
        """

        if self.is_valid_path(dst):
            self._dst_dir = dst
            self._copy_dst = urljoin(
                self._network_path, self._dst_dir
            )

    @property
    def drive_letter(self) -> str:

        """Getter for the EclipseCopy dst property (copy destination)."""

        return self._drive_letter

    @drive_letter.setter
    def drive_letter(self, drive_letter: str):

        """
        Setter for the EclipseCopy dst property (Copy Destination).

        :param drive_letter: Mapped windows network drive.
        :raises ValueError:
        """

        self._drive_letter = drive_letter.upper()
        if not drive_letter.endswith(':'):
            drive_letter += ':'

        if not self.nasbox:
            self.nasbox = Nasbox()

        ipv4_addr = self.nasbox.windows_network_path_to_ip(drive_letter)
        self.ipv4_addr = self.nasbox.ipv4_addr = ipv4_addr

    @staticmethod
    def is_valid_path(dst):
        try:
            Path(dst)
            return True
        except ValueError:
            return False

    @property
    def port(self) -> int:

        """Getter for the EclipseCopy port property."""

        return self._port

    @port.setter
    def port(self, port: Union[str, int]):

        """
        Setter for the EclipseCopy port property.

        :param port: Port number (string or integer)
        :raises ValueError:
        :raises WellKnownPortError:
        """

        # cast str port to and integer
        if isinstance(port, str):
            if not port.isnumeric():
                raise ValueError(f"Invalid port number: '{port}'")
            else:
                port = int(port)

        # make sure port number is not from well-know designated ports.
        if self._is_wellknown_port(port):
            raise WellKnownPortError(f"Port '{port}' is in well-known range [0~1023]")

        # update the network path
        self._port = port
        self._network_path = self._network_path_(self.port, self.ipv4_addr)

    @property
    def network_path(self) -> str:

        """Get the network_path property."""

        return self._network_path

    def set_network_info(self, port: Union[str, int] = "", nas_location: str = ""):

        """
        Set and update network related properties.

        :param port: Port number.
        :param nas_location: IPv4 Address.
        :raises ConnectionError:
        :raises ValueError:
        """

        if not self.is_ipv4_address(nas_location):
            raise ValueError(f"Invalid IPv4 Address: '{nas_location}'")

        if self._service_unavailable(nas_location, port):
            raise ConnectionError(f"Service at '{self._network_path_(port, nas_location)}' is invalid or unavailable.")

        if not self.nasbox:
            self.nasbox = Nasbox()

        if port:
            self.port = port

        if nas_location:
            self.ipv4_addr = nas_location

        # if params weren't passed, use object properties
        _port = port if port else self.port
        _nas_location = nas_location if nas_location else self.ipv4_addr

        # assign the properties.
        self.nasbox = Nasbox()
        self.nasbox.set_ipv4_addr(_nas_location)
        self._network_path = self._network_path_(self.port, self.ipv4_addr)
        self._copy_dst = urljoin(self.network_path, self.dst_dir)

    @property
    def drive(self) -> Drive:

        """Get the drive property."""

        return self._drive

    @drive.setter
    def drive(self, drive: Drive):

        """Set teh drive property."""

        self._drive = drive

    @property
    def folder_mapping(self) -> FolderMapDefinition:

        """Get the folder mapping property."""

        return self._folder_mapping

    @folder_mapping.setter
    def folder_mapping(self, folder_mapping: FolderMapDefinition):

        """Set the folder_mapping property."""

        self._folder_mapping = folder_mapping

    @property
    def nasbox(self) -> Nasbox:

        """Get the nasbox property."""

        return self._nasbox

    @nasbox.setter
    def nasbox(self, nasbox: Nasbox):

        """Set the nasbox property."""

        self._nasbox = nasbox

    @property
    def files(self) -> list:

        """Get the files property."""

        return self._files

    @property
    def records(self) -> list:

        """Get the records property."""

        return self._records

    @property
    def nas_id(self):

        """Get the nas_id property."""

        return self._nas_id

    @nas_id.setter
    def nas_id(self, nas_id: int):

        """
        Set the nas_id property.

        Sets the nas_id property, updating any associated
        properties that use the nas_id.

        :param nas_id:
        """

        if nas_id <= 0:
            raise ValueError("nas_id must be >= 1")

        self._nas_id = nas_id

        # make sure to set the drive nas_id if necessary
        if self._drive and self._drive.nas_id <= 0:
            self._drive.nas_id = nas_id

        if self._records:
            # update the nas_id for the sensor data records
            for record in self._records:
                if record.nas_id <= 0:
                    record.nas_id = nas_id

    @property
    def delivery_id(self):

        """Get the delivery_id property."""

        return self._delivery_id

    @delivery_id.setter
    def delivery_id(self, delivery_id: int):

        """
        Set the delivery id property.

        Sets the delivery id property, updating any associated
        properties that use the delivery_id.

        :param delivery_id:
        :return:
        """

        if delivery_id <= 0:
            raise ValueError("delivery_id must be >= 1")

        self._delivery_id = delivery_id

        # make sure to set the drive delivery_id if necessary
        if self._drive and self._drive.delivery_id <= 0:
            self._drive.delivery_id = delivery_id

        if self._records:
            # update the delivery_id for the sensor data records
            for record in self._records:
                if record.delivery_id <= 0:
                    record.delivery_id = delivery_id

    def _post_records(self, file_errs: dict) -> Union[dict, None]:

        """
        Issue a POST request to the server for all the file records.

        :param file_errs: A list of files that failed to copy.
        :return:
        """

        file_records = [  # remove any files for record creation that failed to copy
            f for f in self._files
            if f not in file_errs["file"]
        ]
        records = self._create_records(file_records)
        erq = EclipseRequest("POST", records)
        res = erq.send()
        return res

    def copy(self) -> dict[str: list[str]]:

        """
        Copy from the delivered source folder structure and translate
        into the GeoBC defined folder structure.

        Note that as of August 12, 2023, the folder structure of src
        is defined by the folder tree delivered by the currently contracted
        company responsible for acquisition

        :return: None if successful, else a dictionary containing any failed file copy items (keys: ["file", "err"])
        :raises MissingFkError:
        :raises MissingNetworkConfigError:
        """

        if not self.dst_dir:
            raise ValueError("The 'dst_dir' property has not been set.")

        # throw exceptions if proper attributes are not set.
        self._validate_copy()

        # copy the files to the network location
        failed_copy = {"file": [], "err": []}
        for file in self._files:
            try:
                f_dir = os.path.dirname(file)
                dst_dir = urljoin(self._copy_dst, f_dir)
                os.makedirs(dst_dir, exist_ok=True)
                shutil.copy2(file, dst_dir)

            except Exception as err:
                failed_copy["file"].append(file)
                failed_copy["err"].append(err)

        # Update the drive records.
        erq = EclipseRequest("POST", self._drive)
        res = erq.send()
        if not res:
            raise ConnectionError("Failed to post drive record to Eclipse database.")

        # Update the file records
        self._post_records(failed_copy)

        return failed_copy

    def _validate_copy(self):

        """
        Run validation methods before continuing network-enabled copy.

        :raises MissingFkError:
        :raises MissingNetworkPropertiesError:
        """

        if not self._is_valid_foreign_keys(self.nas_id, self.delivery_id):
            raise MissingFkError
        if not self._is_valid_network_properties(self.port, self.ipv4_addr):
            raise MissingNetworkPropertiesError

    @staticmethod
    def _is_valid_network_properties(port: Union[str, int], ipv4_addr: str) -> bool:

        """Make sure port and ipv4_addr properties are not default or empty."""

        if isinstance(port, str):
            port = int(port)

        return port > 0 and ipv4_addr

    @staticmethod
    def _is_wellknown_port(port: Union[str, int]) -> bool:

        """Make assigned port number is not within well-known port range."""

        if isinstance(port, str):
            port = int(port)

        return port <= NetworkConfig.PORT.FORBIDDEN.WellKnown.P_1023

    @staticmethod
    def _is_valid_foreign_keys(nas_id: int, delivery_id: int) -> bool:

        """Make sure foreign keys are set properly and are note default values."""

        return nas_id > 0 or delivery_id > 0

    def _gather_files(self):

        """
        Copy from the delivered source folder structure and translate
        into the GeoBC defined folder structure.

        Note that as of August 12, 2023, the folder structure of src
        is defined by the folder tree delivered by the currently contracted
        company responsible for acquisition
        """

        fmap = self.folder_mapping
        if fmap:
            src_files = []
            for folder in fmap.keys():

                sources = fmap[folder][FolderMapKey.SOURCE_FOLDERS]
                extensions = fmap[folder][FolderMapKey.FILE_EXTENSIONS]

                for source in sources:  # Gather files with desired extensions
                    is_recursive = source.endswith("*")
                    src_full = os.path.join(self._src_dir, source)  # join the src root with current relative path
                    files = []
                    for ext in extensions:
                        files.extend(
                            glob(os.path.join(src_full, "*" + ext), recursive=is_recursive)
                        )
                    if files:
                        src_files.extend(files)

            if src_files:  # If files found with extensions, copy them to the GeoBC folder mappings
                self._files = src_files

    def _create_records(self, files: list[str]) -> list[SensorData]:

        """
        Copy from the delivered source folder structure and translate
        into the GeoBC defined folder structure.

        Note that as of August 12, 2023, the folder structure of src
        is defined by the folder tree delivered by the currently contracted
        company responsible for acquisition
        """

        records = []

        if files:
            for f in files:
                record = SensorData(file_path=f)
                if self._nas_id > 0:
                    record.nas_id = self._nas_id
                if self._delivery_id > 0:
                    record.delivery_id = self._delivery_id
                records.append(record)

        return records

    @staticmethod
    def _network_path_(port: Union[str, int], ipv4_addr: str) -> str:
        return f"http://{ipv4_addr}:{port}"

    @staticmethod
    def _service_available(ipv4_addr: str, port: Union[str, int]) -> bool:

        """
        Check if service is available for connection.

        Uses the ipv4 address and port number to verify
        if a target service is available for connection.

        :param ipv4_addr: IPv4 Address
        :param port: Port number.
        :return: True of False (bool)
        """

        if isinstance(port, str):
            port = int(port)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect((ipv4_addr, port))
                return True
            except socket.error:
                return False

    def _service_unavailable(self, ipv4_addr: str, port: Union[str, int]) -> bool:

        """
        Check if service is unavailable for connection.

        Wrapper for more verbose use of service_available method.

        :param ipv4_addr: IPv4 Address
        :param port: Port number.
        :return: True of False (bool)
        """
        if isinstance(port, str):
            port = int(port)

        return not self._service_available(ipv4_addr, port)

    @staticmethod
    def is_ipv4_address(addr: str) -> bool:
        try:
            socket.inet_aton(addr)
            return True
        except socket.error:
            return False


def main():

    # Quick and dirty "GUI"
    src = askdirectory(title="Select the source ROOT directory (Copy from).")
    dst = askdirectory(title="Select the destination ROOT directory. (Copy to)")
    print(src, dst)


if __name__ == "__main__":
    main()
