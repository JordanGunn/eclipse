from typing import Dict
from .const import RiProcessSourceDir, GeoBCDirName, GeoBCDirExt


class FolderMapKey:
    """Valid folder map keys."""

    SOURCE_FOLDERS = "source_folders"
    FILE_EXTENSIONS = "file_extensions"


"""Type definition for defined folder mapping."""
FolderMapDefinition = Dict[str, Dict[str, list[str]]]


"""Kisik folder structure (RiProcess default output tree) to GeoBC spec folder structure."""
KISIK_TO_GEOBC = {

    GeoBCDirName.AUXILIARY: {
        FolderMapKey.SOURCE_FOLDERS: RiProcessSourceDir.AUXILIARY,
        FolderMapKey.FILE_EXTENSIONS: GeoBCDirExt.AUXILIARY
    },

    GeoBCDirName.COVERAGE: {
        FolderMapKey.SOURCE_FOLDERS: RiProcessSourceDir.COVERAGE,
        FolderMapKey.FILE_EXTENSIONS: GeoBCDirExt.COVERAGE
    },

    GeoBCDirName.BASE_STATION: {
        FolderMapKey.SOURCE_FOLDERS: RiProcessSourceDir.BASE_STATION,
        FolderMapKey.FILE_EXTENSIONS: GeoBCDirExt.BASE_STATION
    },

    GeoBCDirName.CONTROL: {
        FolderMapKey.SOURCE_FOLDERS: RiProcessSourceDir.CONTROL,
        FolderMapKey.FILE_EXTENSIONS: GeoBCDirExt.CONTROL
    },

    GeoBCDirName.RAW_LIDAR: {
        FolderMapKey.SOURCE_FOLDERS: RiProcessSourceDir.RAW_LIDAR,
        FolderMapKey.FILE_EXTENSIONS: GeoBCDirExt.RAW_LIDAR
    },

    GeoBCDirName.IMU_GPS: {
        FolderMapKey.SOURCE_FOLDERS: RiProcessSourceDir.IMU_GPS,
        FolderMapKey.FILE_EXTENSIONS: GeoBCDirExt.IMU_GPS
    }
}
