# system imports
import os
import shutil
import subprocess
from glob import glob
from typing import Optional
from tkinter.filedialog import askdirectory

# user imports
from client.eclipse_request import EclipseRequest
from client.entity import Nasbox, SensorData, Drive, Delivery
from folder_map import KISIK_TO_GEOBC, FolderMapDefinition, FolderMapKey
from client.eclipse_config import IS_LINUX, IS_WINDOWS, IS_UNSUPPORTED_OS


# TODO SET FILE PERMISSIONS OF SOURCE TO READ ONLY

class EclipseCopy:

    def __init__(
            self, src: Optional[str] = None, dst: Optional[str] = None, nas_id: Optional[int] = -1,
            delivery_id: Optional[int] = -1, folder_mapping: Optional[FolderMapDefinition] = None
    ):

        self._src = ""
        self._dst = ""
        self._nas_id = -1
        self._delivery_id = -1
        self._files = []
        self._records = []
        self._drive = None
        self._nasbox = None
        self._delivery = None
        self._folder_mapping = folder_mapping

        # Call property setters if actual values passed
        if src:
            self.src = src
        if dst:
            self.dst = dst
        if nas_id > 0:
            self.nas_id = nas_id
        if delivery_id > 0:
            self.delivery_id = delivery_id

    @property
    def src(self) -> str:
        return self._src

    @src.setter
    def src(self, src: str):

        if not os.path.exists(src):
            raise ValueError(f"Path {src} does not exist.")

        else:  # set the source and anything else we can.
            self._src = src
            if not self._drive:
                self._drive = Drive()
                self._drive.set_drive_info(src)

            if not self._files:
                self._gather_files()
                self._create_records()

    @property
    def dst(self) -> str:
        return self._dst

    @dst.setter
    def dst(self, dst: str):
        if not os.path.exists(dst):
            raise ValueError(f"Path {dst} does not exist.")

        self._dst = dst
        if not self._nasbox:
            self._nasbox = Nasbox()
            self._nasbox.set_ipv4_addr(dst)

    @property
    def drive(self) -> Drive:
        return self._drive

    @drive.setter
    def drive(self, drive: Drive):
        self._drive = drive

    @property
    def folder_mapping(self) -> FolderMapDefinition:
        return self._folder_mapping

    @folder_mapping.setter
    def folder_mapping(self, folder_mapping: FolderMapDefinition):
        self._folder_mapping = folder_mapping

    @property
    def nasbox(self) -> Nasbox:
        return self._nasbox

    @nasbox.setter
    def nasbox(self, nasbox: Nasbox):
        self._nasbox = nasbox

    @property
    def files(self) -> list:
        return self._files

    @property
    def records(self) -> list:
        return self._records

    @property
    def nas_id(self):
        return self._nas_id

    @nas_id.setter
    def nas_id(self, nas_id: int):

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
        return self._delivery_id

    @delivery_id.setter
    def delivery_id(self, delivery_id: int):

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
            for folder in fmap:

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

    def _create_records(self):

        """
        Copy from the delivered source folder structure and translate
        into the GeoBC defined folder structure.

        Note that as of August 12, 2023, the folder structure of src
        is defined by the folder tree delivered by the currently contracted
        company responsible for acquisition
        """

        records = []
        files = self._files
        if files:
            for f in files:
                record = SensorData(f)
                if self._nas_id > 0:
                    record.nas_id = self._nas_id
                if self._delivery_id > 0:
                    record.delivery_id = self._delivery_id
                records.append(record)

        self._records = records

    @staticmethod
    def _linux_shell_copy(src, dst):
        """
        Perform recursive copy using Linux shell-command.

        :param src: The source directory.
        :param dst: The destination Directory.
        """

        if not src.endswith('/'):
            src += '/'
        if not dst.endswith('/'):
            dst += '/'

        # Construct the rsync command
        cmd = [ 'rsync', '-a', '--include', '*/', '--exclude', '*', src, dst]

        # Execute the command
        subprocess.run(cmd, check=True)

    @staticmethod
    def _win_shell_copy(src, dst):

        """
        Perform recursive copy using Windows shell-command.

        :param src: The source directory.
        :param dst: The destination Directory.
        """

        cmd = ['robocopy', src, dst, '/E', '/XF', '*']

        # Execute the command
        subprocess.run(cmd, check=True)

    def _copy_folder_structure(self, src, dst) -> str:
        """
        Copies the folder structure from source to dest, excluding files.
        :param src: The source directory path.
        :param dst: The destination directory path.
        :return: The copied destination folder
        """

        # get the new copied destination
        head, root = os.path.split(src)
        dest_root = os.path.join(dst, root)
        os.makedirs(dest_root, exist_ok=True)
        self._linux_shell_copy(src, dest_root) \
            if IS_LINUX \
            else self._win_shell_copy(src, dest_root)

        return dest_root

    def copy(self) -> list:

        """
        Copy from the delivered source folder structure and translate
        into the GeoBC defined folder structure.

        Note that as of August 12, 2023, the folder structure of src
        is defined by the folder tree delivered by the currently contracted
        company responsible for acquisition

        :return: A list of files that failed to copy (if any.)
        """

        if not self.dst:
            raise ValueError("The 'dst' property has not been set.")

        if self.nas_id <= 0:
            raise CopyError.NoNasIdFkError
        if self.delivery_id <= 0:
            raise CopyError.NoDeliveryIdFkError

        failed_copy = []
        erq = EclipseRequest("POST", self._drive)
        for record, file in zip(self._records, self._files):
            try:
                f_dir = os.path.dirname(file)
                dest_dir = os.path.join(self.dst, f_dir)
                os.makedirs(dest_dir, exist_ok=True)
                shutil.copy2(file, dest_dir)
                erq = EclipseRequest("POST", record)
                erq.send()
            except Exception as e:
                failed_copy.append((file, e))

        return failed_copy


def lp_ftree_json(path: str):
    """
    Generates a JSON representation of the folder structure for the given path.
    """
    tree = {}
    if os.path.isdir(path):
        for item in os.listdir(path):
            sub_path = os.path.join(path, item)
            if os.path.isdir(sub_path):
                tree[item] = lp_ftree_json(sub_path)
    return tree


class CopyError:
    class NoDeliveryIdFkError(Exception):
        """Exception indicating that a drive record is missing the delivery id foreign key."""

        def __init__(self, message="Entity does not contain delivery_id foreign key attribute."):
            self.message = message
            super().__init__(self.message)

    class NoNasIdFkError(Exception):
        """Exception indicating that a drive record is missing the nas_id foreign key."""

        def __init__(self, message="Entity does not contain nas_id foreign key attribute."):
            self.message = message
            super().__init__(self.message)


def main():

    # Quick and dirty "GUI"
    src = askdirectory(title="Select the source ROOT directory (Copy from).")
    dst = askdirectory(title="Select the destination ROOT directory. (Copy to)")



if __name__ == "__main__":
    main()