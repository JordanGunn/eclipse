# system imports
import os
import shutil
import psutil
from typing import Union, Optional

# system-specific imports
try:
    import win32api  # windows os
except ImportError:
    win32api = None

try:
    import pyudev  # windows os
except ImportError:
    pyudev = None

# user imports
from .entity_attrs import EntityName
from .entity import Entity


# =====================================================================


class Drive(Entity):

    def __init__(self, nas_id: Optional[int] = -1, delivery_id: Optional[int] = -1):

        super().__init__()
        self._name = EntityName.DRIVE

        self.file_count_ = -1
        self.drive_path_ = ""
        self.serial_number_ = ""
        self.storage_total_gb_ = float("nan")
        self.storage_used_gb_ = float("nan")

        self.nas_id_ = nas_id
        self.delivery_id_ = delivery_id

    # -- DRIVE_PATH
    @property
    def drive_path(self):
        return self.drive_path_

    @drive_path.setter
    def drive_path(self, drive_path: str):

        if self._is_external_drive(drive_path):
            self.drive_path_ = drive_path
            if not self.serial_number_:
                self.serial_number = ""  # Empty string will check the drive path.
        else:
            self.drive_path_ = None

    # -- SERIAL_NUMBER
    @property
    def serial_number(self):
        return self.serial_number_

    @serial_number.setter
    def serial_number(self, serial_number: str = ""):

        """
        Cross-platform setter for the serial number of an external drive.
        Compatible with Linux and Windows OS.

        Note that if no drive_path is set, method will fail silently
        by setting the serial_number to an empty string.
        """

        # if passed directly
        if serial_number:
            self.serial_number_ = serial_number

        # otherwise, get the serial number from the drive letter
        else:
            dp = self.drive_path_
            if not dp:
                self.serial_number_ = ""

            sn_func = self._serial_number_win \
                if win32api else self._serial_number_linux

            self.serial_number_ = sn_func(dp)

    # -- NAS_ID
    @property
    def nas_id(self):
        return self.nas_id_

    @nas_id.setter
    def nas_id(self, nas_id: Union[int, str]):
        if isinstance(nas_id, int):
            self.nas_id_ = nas_id
        elif isinstance(nas_id, str) and nas_id.isnumeric():
            self.nas_id_ = int(nas_id)
        else:
            raise ValueError(f"Invalid: '{nas_id}'. Argument 'nas_id' must be an integer.")

    # -- DELIVERY_ID
    @property
    def delivery_id(self):
        return self.delivery_id_

    @delivery_id.setter
    def delivery_id(self, delivery_id: Union[int, str]):
        if isinstance(delivery_id, int):
            self.nas_id_ = delivery_id
        elif isinstance(delivery_id, str) and delivery_id.isnumeric():
            self.nas_id_ = int(delivery_id)
        else:
            raise ValueError(f"Invalid: '{delivery_id}'. Argument 'nas_id' must be an integer.")

    @property
    def storage_total_gb(self):
        return self.storage_total_gb_

    @property
    def storage_used_gb(self):
        return self.storage_used_gb_

    def set_drive_info(self, drive_path: Optional[str] = None):

        """Set the storage_used_gb and storage_total_gb properties."""

        # update the drive path if passed as arg
        if drive_path:
            self.drive_path_ = drive_path

        # otherwise, use the existing drive path.
        if self.drive_path_ and os.path.exists(self.drive_path_):
            self.file_count = 0      # setter looks at drive path when passed an empty string.
            self.serial_number = ""  # setter looks at drive path when passed an empty string.
            usage = shutil.disk_usage(self.drive_path_)
            self.storage_total_gb_ = usage.total / (1024 ** 3)
            self.storage_used_gb_ = usage.used / (1024 ** 3)

    @property
    def file_count(self):
        return self.file_count_

    @file_count.setter
    def file_count(self, file_count: int = 0):

        if file_count:
            self.file_count_ = file_count
        else:
            if self.drive_path_ and os.path.exists(self.drive_path_):
                self.file_count_ = sum([len(files) for _, _, files in os.walk(self.drive_path_)])
            else:
                self.file_count_ = -1

    @staticmethod
    def _serial_number_win(drive_letter: str) -> str:

        """Get the drive serial number on Windows machines."""
        # noinspection PyUnresolvedReferences
        drive_info = win32api.GetVolumeInformation(drive_letter)
        return drive_info[1]

    @staticmethod
    def _serial_number_linux(drive_name: str) -> str:
        # noinspection PyUnresolvedReferences
        context = pyudev.Context()
        serial_number = None

        for device in context.list_devices(subsystem='block', DEVTYPE='disk'):
            if device.device_node.endswith(drive_name):
                serial_number = device.get('ID_SERIAL_SHORT')
                break

        if serial_number:
            return serial_number
        else:
            return "Serial number not found or drive does not exist."

    @staticmethod
    def _is_external_drive(drive_path: str) -> bool:

        """Check if a drive path is associated with an external drive."""

        path = os.path.normpath(drive_path)

        for prt in psutil.disk_partitions():
            # check if path starts with the mount point of a partition
            if os.path.commonpath([path, prt.mountpoint]) == prt.mountpoint:
                # make sure external drive not in C:
                if prt.device != "C:\\":
                    return True

        return False
