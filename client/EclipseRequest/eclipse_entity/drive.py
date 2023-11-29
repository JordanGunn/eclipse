import os
import json
import shutil
import psutil
import platform


# check the native OS
IS_WINDOWS = (platform.system().lower() == "windows")
if IS_WINDOWS:
    import win32api
else:
    import pyudev


class Drive(object):

    def __init__(self, nas_id: int, delivery_id: int):

        self._file_count = -1
        self._drive_path = ""
        self._serial_number = ""
        self._storage_total_gb = float("nan")
        self._storage_used_gb = float("nan")

        self._nas_id = nas_id
        self._delivery_id = delivery_id

    # -- DRIVE
    @property
    def drive_path(self):
        return self._drive_path

    @drive_path.setter
    def drive_path(self, drive_path: str):

        if self._is_external_drive(drive_path):
            self._drive_path = drive_path
        else:
            self._drive_path = None

    # -- SERIAL_NUMBER
    @property
    def serial_number(self):
        return self._serial_number

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
            self._serial_number = serial_number

        # otherwise, get the serial number from the drive letter
        else:
            dp = self._drive_path
            if not dp:
                self._serial_number = ""

            sn_func = self._serial_number_win \
                if IS_WINDOWS else self._serial_number_linux

            self._serial_number = sn_func(dp)

    # -- NAS_ID
    @property
    def nas_id(self):
        return self._nas_id

    @nas_id.setter
    def nas_id(self, nas_id):
        self._nas_id = nas_id

    # -- DELIVERY_ID
    @property
    def delivery_id(self):
        return self._delivery_id

    @delivery_id.setter
    def delivery_id(self, delivery_id):
        self._delivery_id = delivery_id

    @property
    def storage_total_gb(self):
        return self._storage_total_gb

    @property
    def storage_used_gb(self):
        return self._storage_used_gb

    def set_storage_info(self, storage_used_gb: float = None):

        """Set the storage_used_gb and storage_total_gb properties."""

        if storage_used_gb:
            self._storage_used_gb = storage_used_gb
        else:
            if self._drive_path and os.path.exists(self._drive_path):
                usage = shutil.disk_usage(self._drive_path)
                self._storage_total_gb = usage.total / (1024 ** 3)
                self._storage_used_gb = usage.used / (1024 ** 3)
            else:
                self._storage_total_gb = None
                self._storage_used_gb = None

    @property
    def file_count(self):
        return self._file_count

    @file_count.setter
    def file_count(self, file_count: int = 0):

        if file_count:
            self._file_count = file_count
        else:
            if self._drive_path and os.path.exists(self._drive_path):
                self._file_count = sum([len(files) for _, _, files in os.walk(self._drive_path)])
            else:
                self._file_count = None

    @staticmethod
    def _serial_number_win(drive_letter: str) -> str:

        """Get the drive serial number on Windows machines."""

        drive_info = win32api.GetVolumeInformation(drive_letter)
        return drive_info[1]

    @staticmethod
    def _serial_number_linux(drive_name: str) -> str:
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

    def serialize(self) -> str:
        """
        Serialize the object to a JSON-formatted string.
        """
        drive_data = {
            "drive_path": self.drive_path,
            "serial_number": self.serial_number,
            "storage_total_gb": self.storage_total_gb,
            "storage_used_gb": self.storage_used_gb,
            "file_count": self.file_count,
            "nas_id": self.nas_id,
            "delivery_id": self.delivery_id
        }
        return json.dumps(drive_data, indent=4)


def main():

    drive = Drive(1, 1)


if __name__ == "__main__":
    main()
