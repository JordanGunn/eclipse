from os import path


class ShpFileExt:

    """Enum Class containing all valid shapefile and shapefile auxiliary file extensions."""

    SHP = ".shp"          # Main file containing geometry data
    SHX = ".shx"          # Shape index format
    DBF = ".dbf"          # Database format (contains attribute data for shapes)
    PRJ = ".prj"          # Projection format (contains coordinate system information)
    SBN = ".sbn"          # Spatial index of features
    SBX = ".sbx"          # Spatial index of features
    FBN = ".fbn"          # Read-only spatial index of features
    FBX = ".fbx"          # Read-only spatial index of features
    AIN = ".ain"          # Attribute index of active fields in a table
    AIH = ".aih"          # Attribute index of active fields in a table
    IXS = ".ixs"          # Geocoding index for read-write shapefiles
    MXS = ".mxs"          # Geocoding index for read-write shapefiles (ODB format)
    ATX = ".atx"          # An attribute index for the .dbf file in the form of shapefilename.atx (ArcGIS 8 and later)
    CPG = ".cpg"          # Character encoding format
    SHP_XML = ".shp.xml"  # Metadata (XML format)
    LIST = [
        SHP, SHX,  DBF, PRJ, SBN, SBX, FBN, FBX,
        AIN, AIH, IXS, MXS, ATX, SHP_XML, CPG
    ]


class VectorFileExt:

    """Enum Class containing common vector file extensions."""

    KML = ".kml"
    KMZ = ".kmz"
    CSV = ".csv"
    GPKG = ".gpkg"
    LIST = [
        KML,
        KMZ,
        CSV,
        GPKG,
        *ShpFileExt.LIST
    ]


class GeoBCDirName:
    """Valid Geobc Directory names based on specifications."""

    AUXILIARY = "AUXILIARY"
    COVERAGE = "COVERAGE"
    BASE_STATION = "BASE_STATION"
    CONTROL = "CONTROL"
    RAW_LIDAR = "RAW_LIDAR"
    IMU_GPS = "IMU_GPS"
    ALL = [
        AUXILIARY, COVERAGE, BASE_STATION,
        CONTROL, RAW_LIDAR, IMU_GPS
    ]


class RiProcessExtName:
    """Enum class containing lists of file extensions associated with GeoBC Directory Names."""

    AUXILIARY = [".rxp", ".rdp"]
    COVERAGE = [*VectorFileExt.LIST]
    BASE_STATION = [".rinex", ".obs"]
    CONTROL = [*VectorFileExt.LIST]
    RAW_LIDAR = [".laz", ".las"]
    IMU_GPS = [".dat", ".imu", ".igs", ".out", ".raw", "pos.*"]
    ALL = [*AUXILIARY, *COVERAGE, *BASE_STATION, *CONTROL, *RAW_LIDAR, *IMU_GPS]


class RiProcessSourceDir:
    """
    Enum class containing verbose naming for lists of source directories associated with particular data.

    Note that path names are adjusted dynamically based on the native OS. Additionally, wild cards are
    included in path names to indicate the existence of many subdirectories holding target data.
    """

    AUXILIARY = [f"03_RIEGL_RAW{path.sep}02_RXP{path.sep}**", f"06_RIEGL_PROC{path.sep}07_RDB"]
    COVERAGE = [f"06_RIEGL_PROC{path.sep}09_EXPORT", f"06_RIEGL_PROC{path.sep}06_GEOIMAGES"]
    BASE_STATION = [f"05_INS-GPS_PROC{path.sep}03_BASE"]
    CONTROL = [f"09_EXPORT"]
    RAW_LIDAR = [f"06_RIEGL_PROC{path.sep}04_EXPORT"]
    IMU_GPS = [f"05_INS-GPS_PROC{path.sep}01_POS", f"01_MON{path.sep}INS-GPS_1", f"02_FULL{path.sep}INS-GPS_1"]
    ALL = [*AUXILIARY, *COVERAGE, *BASE_STATION, *CONTROL, *RAW_LIDAR, *IMU_GPS]
