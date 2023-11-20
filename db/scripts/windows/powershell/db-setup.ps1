# PowerShell Script

# Load config
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
. .\db-config.ps1
. .\db-env.ps1

# DB Table References
$ENCODING = "latin1"
$NAMESPACE = "public"
$TABLE_BCGS20K = "${NAMESPACE}.BCGS20k"
$TABLE_BCGS2500K = "${NAMESPACE}.BCGS2500k"

# Create the database and tables
psql -h $HOST_NAME -d $DB_NAME -U $USER_NAME -f $SCRIPT_SCHEMA
Write-Host "  Database creation and table generation complete."

# Populate the static reference tables
psql -h $HOST_NAME -d $DB_NAME -U $USER_NAME -f $SCRIPT_REFTABLE
Write-Host "  Initial reference tables generated."

# Read and insert BCGS 2500K and 20K tile geometry into reference tables
Write-Host "  Creating BCGS reference tables ..."
# -- BCGS20K Grid insertion
Set-ACL -Path $BCGS_SHP_DIR_20K -AclObject (Get-Acl -Path $BCGS_SHP_DIR_20K).SetAccessRule((New-Object System.Security.AccessControl.FileSystemAccessRule("Everyone","FullControl","Allow")))
shp2pgsql -c -m $COLUMN_MAP_20K -W $ENCODING $BCGS_SHP_20K $TABLE_BCGS20K | psql -h $HOST_NAME -d $DB_NAME -U $USER_NAME
Write-Host "  BCGS20K reference table done."
# -- BCGS2500K Grid insertion
Set-ACL -Path $BCGS_SHP_DIR_2500K -AclObject (Get-Acl -Path $BCGS_SHP_DIR_2500K).SetAccessRule((New-Object System.Security.AccessControl.FileSystemAccessRule("Everyone","FullControl","Allow")))
shp2pgsql -c -m $COLUMN_MAP_2500K -W $ENCODING $BCGS_SHP_2500K $TABLE_BCGS2500K | psql -h $HOST_NAME -d $DB_NAME -U $USER_NAME
Write-Host "  BCGS2500K reference table done."

# Run post insertion
psql -h $HOST_NAME -d $DB_NAME -U $USER_NAME -f $SCRIPT_INSERTION
Write-Host "================ Complete! ================"
