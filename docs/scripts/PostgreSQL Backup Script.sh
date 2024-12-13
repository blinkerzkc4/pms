#!/bin/bash

# Set the current date for the backup file
BACKUP_DATE=$(date +"%Y%m%d%H%M%S")

# Set the path where you want to store the backups
BACKUP_DIR="/home/pms/backup"

# Set PostgreSQL connection parameters
PG_USER="yojana_db_user"
PG_DB="yojana_db"
PG_PASSWORD="Yoj@na@321"
PG_HOST="127.0.0.1"

# Set the PGPASSWORD environment variable for password authentication
export PGPASSWORD="$PG_PASSWORD"

# Perform the backup using pg_dump
pg_dump -U $PG_USER -h $PG_HOST -d $PG_DB > $BACKUP_DIR/$BACKUP_DATE.backup

# Unset the PGPASSWORD environment variable
unset PGPASSWORD

# Optional: Compress the backup file
# gzip $BACKUP_DIR/$BACKUP_DATE.backup

# Optional: Remove backups older than a certain period
find $BACKUP_DIR -type f -name '*.backup' -mtime +7 -exec rm {} \;