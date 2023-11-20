# PowerShell Script

# Variable pre-declarations
$FLIST_20K = $null
$FLIST_2500K = $null

# Params (Change as needed)
$DB = "eclipse"
$EPSG_ALBERS_CSRS = 3005
$DIR_SCRIPT_DATA = "..\..\data"
$DIR_VECTOR_DATA = "${env:HOME}\work\geobc\vector_data"  # --> CHANGE TO DATA LOCATION

# Relative paths to SQL scripts
$PATH_SQL_SCRIPTS = "..\..\.."
$SCRIPT_ROLES = "${PATH_SQL_SCRIPTS}\${DB}_roles.sql"
$SCRIPT_SCHEMA = "${PATH_SQL_SCRIPTS}\${DB}_schema.sql"
$SCRIPT_REFTABLE = "${PATH_SQL_SCRIPTS}\${DB}_reftables.sql"
$SCRIPT_INSERTION = "${PATH_SQL_SCRIPTS}\${DB}_insertion.sql"

# Relative paths to files containing data
$COLUMN_MAP_20K = "${DIR_SCRIPT_DATA}\col-map-20K"
$COLUMN_MAP_2500K = "${DIR_SCRIPT_DATA}\col-map-2500K"

# Paths to data (Change as needed)
$BCGS_ROOT_20K = "${DIR_VECTOR_DATA}\BCGS_20K"
$BCGS_ROOT_2500K = "${DIR_VECTOR_DATA}\BCGS_2500K"
$BCGS_SHP_DIR_20K = "${BCGS_ROOT_20K}\BCGS_20K_GRID"
$BCGS_SHP_DIR_2500K = "${BCGS_ROOT_2500K}\BCGS_2500_GRID"
$BCGS_SHP_20K = "${BCGS_SHP_DIR_20K}\20K_GRID_polygon.shp"
$BCGS_SHP_2500K = "${BCGS_SHP_DIR_2500K}\BCGS2500GR_polygon.shp"
