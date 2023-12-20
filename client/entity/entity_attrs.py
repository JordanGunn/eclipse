
class EntityName:

    """Valid entity names for eclipse tables."""

    DRIVE = "drive"
    EPOCH = "epoch"
    LIDAR = "lidar"
    NASBOX = "nasbox"
    ECLIPSE = "eclipse"
    BCGS20K = "bcgs20k"
    UTM_ZONE = "utmzone"
    DELIVERY = "delivery"
    BCGS2500K = "bcgs2500k"
    LIDAR_STRIP = "lidarraw"
    TRAJECTORY = "trajectory"
    SENSOR_DATA = "sensordata"
    LIDAR_TILE = "lidarclassified"
    DERIVED_PRODUCT = "derivedproduct"
    PROCESSING_STATUS = "processingstatus"
    SPATIAL_REFERENCE = "spatialreference"


class EntityAttributes:

    """Valid entity names for eclipse tables."""

    DRIVE = ("file_count", "serial_number", "storage_total_gb", "storage_used_gb", "nas_id", "delivery_id")
    EPOCH = None
    LIDAR = None
    NASBOX = None
    ECLIPSE = None
    BCGS20K = None
    UTM_ZONE = None
    TRAJECTORY = None
    SENSOR_DATA = ("file_path", "file_name", "file_size", "delivery_id", "nas_id", "trajectory_id")
    DELIVERY = ("receiver_name", "comments", "timestamp")
    LIDAR_RAW = None
    BCGS2500K = None
    DERIVED_PRODUCT = None
    LIDAR_CLASSIFIED = None
    PROCESSING_STATUS = None
    SPATIAL_REFERENCE = None


"""Map of entity name to entity attributes."""
ENTITY_ATTR_MAP = {
    EntityName.DRIVE: EntityAttributes.DRIVE,
    EntityName.EPOCH: EntityAttributes.EPOCH,
    EntityName.LIDAR: EntityAttributes.LIDAR,
    EntityName.NASBOX: EntityAttributes.NASBOX,
    EntityName.ECLIPSE: EntityAttributes.ECLIPSE,
    EntityName.BCGS20K: EntityAttributes.BCGS20K,
    EntityName.UTM_ZONE: EntityAttributes.UTM_ZONE,
    EntityName.DELIVERY: EntityAttributes.DELIVERY,
    EntityName.LIDAR_STRIP: EntityAttributes.LIDAR_RAW,
    EntityName.BCGS2500K: EntityAttributes.BCGS2500K,
    EntityName.DERIVED_PRODUCT: EntityAttributes.DERIVED_PRODUCT,
    EntityName.LIDAR_TILE: EntityAttributes.LIDAR_CLASSIFIED,
    EntityName.PROCESSING_STATUS: EntityAttributes.PROCESSING_STATUS,
    EntityName.SPATIAL_REFERENCE: EntityAttributes.SPATIAL_REFERENCE,
    EntityName.SENSOR_DATA: EntityAttributes.SENSOR_DATA,
    EntityName.TRAJECTORY: EntityAttributes.TRAJECTORY
}


