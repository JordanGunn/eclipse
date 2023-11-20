# PowerShell Script

# Turn off echo
$Host.UI.RawUI.WindowTitle = "Running Script"

# Load your config and environment variables
. .\db-config.ps1
. .\db-env.ps1

$PATH_SQL_SCRIPTS = "..\.."
$SCRIPT_PURGE = "${PATH_SQL_SCRIPTS}\eclipse_purge.sql"

# Run the SQL script
psql -h $HOST_NAME -U $USER_NAME -d $DB_NAME -a -f $SCRIPT_PURGE
