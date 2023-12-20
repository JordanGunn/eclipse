# system imports
import os
import shutil
from glob import glob
from urllib.parse import urljoin
from typing import Optional, Union
from tkinter.filedialog import askdirectory

# user imports
from client.eclipse_config import NativeOS
from client.eclipse_request import EclipseRequest
from client.entity import Nasbox, SensorData, Drive
from .folder_map import FolderMapDefinition, FolderMapKey
if NativeOS.IS_LINUX:
    from client.entity import NasboxLinux as Nas
elif NativeOS.IS_WINDOWS:
    from client.entity import NasboxWindows as Nas
else:
    raise OSError("Unsupported Operating System.")


class EclipseCopy:

    def __init__(
            self, src: str, dst: str, nas_id: Optional[Union[int, str]] = -1,
            delivery_id: Optional[Union[int, str]] = -1, folder_mapping: Optional[FolderMapDefinition] = None
    ):

        """
        Initialize an EclipseCopy object. \n
        \n
        Creates an EclipseCopy object. Note that the only mandatory constructor
        arguments are 'src' and 'dst'. This means that if any other parameters are not
        passed via the constructor, they should be set accordingly before executing
        the copy() method.

        :param src: Source directory (external drive).
        :param dst: Destination directory (network drive).
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
        self._src = ""
        self._dst = ""

        # int attributes
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
        self.src = src
        self.dst = dst
        if nas_id > 0:
            self.nas_id = nas_id
        if delivery_id > 0:
            self.delivery_id = delivery_id

    @property
    def src(self) -> str:

        """Getter for the EclipseCopy src property (copy source)."""

        return self._src

    @src.setter
    def src(self, src: str):

        """
        Setter for the EclipseCopy src property

        :param src: A valid drive path.
        :raises ValueError:
        """

        if not os.path.exists(src):
            raise ValueError(f"Path {src} does not exist.")

        else:  # set the src and update related properties.
            self._src = src
            self._drive = Drive()
            self._drive.set_drive_info(src)
            self._gather_files()

    @property
    def dst(self) -> str:

        """Getter for the EclipseCopy dst property (copy destination)."""

        return self._dst

    @dst.setter
    def dst(self, dst: str):

        """
        Setter for the EclipseCopy dst property (Copy Destination).

        :param dst: Copy Destination (IPv4 address or valid network path.)
        :raises ValueError:
        """

        if self.nasbox and not self.nasbox.path:
            self.nasbox.path = dst
        else:
            self.nasbox = Nasbox.create(dst)

        self._dst = self.nasbox.path

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
    def nasbox(self) -> Nas:

        """Get the nasbox property."""

        return self._nasbox

    @nasbox.setter
    def nasbox(self, nasbox: Nas):

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
        if self._drive and self.delivery_id > 0:
            self._drive.delivery_id = delivery_id

        if self._records:
            # update the delivery_id for the sensor data records
            for record in self._records:
                if record.delivery_id > 0:
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

    def copy(self, dst: str = "") -> dict[str: list[str]]:

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

        if not self.dst and not dst:
            raise ValueError("The 'dst_dir' property has not been set.")

        # throw exceptions if proper attributes are not set.
        if not self._is_valid_foreign_keys(self.nas_id, self.delivery_id):
            raise MissingFkError

        if dst:  # option to overwrite destination by passing as argument.
            self.dst = dst

        # copy the files to the network location
        failed_copy = {"file": [], "err": []}
        for file in self._files:
            try:
                f_dir = os.path.dirname(file)
                f_dir = f_dir[1:] if f_dir.startswith(os.path.sep) else f_dir
                dst = self._dst + os.path.sep + f_dir
                os.makedirs(dst, exist_ok=True)
                shutil.copy2(file, dst)

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
                    src_full = os.path.join(self._src, source)  # join the src root with current relative path
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


class MissingFkError(Exception):
    """Exception indicating that EclipseCopy is missing the delivery id foreign key."""

    def __init__(self, message="Missing foreign keys: Make sure 'delivery_id' and 'nas_id' are set correctly."):
        self.message = message
        super().__init__(self.message)


def main():

    # Quick and dirty "GUI"
    src = askdirectory(title="Select the source ROOT directory (Copy from).")
    dst = askdirectory(title="Select the destination ROOT directory. (Copy to)")
    print(src, dst)


if __name__ == "__main__":
    main()
