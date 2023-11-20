# PowerShell Script

# Configuration parameters for ECLIPSE
$HOST_NAME = "localhost"
$HOST_IP = "127.0.0.1"
$DB_NAME = "eclipse"
$USER_NAME = "postgres"
$PASSWORD = "postgres"

# PostgresDB environment variable (do not change).
$env:PGPASSWORD = $PASSWORD
