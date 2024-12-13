#!/bin/bash

# Database backup directory
DATABASE_BACKUP_DIR=/home/pms/backup

# Array of frontend directories
declare -A frontend_directories=(
    ["lmc"]="home/pms/pms_frontend"
    ["kmc"]="/home/pms/pms-frontends/kmc"
    ["jsmc"]="/home/pms/pms-frontends/jsmc"
    ["rishimun"]="/home/pms/pms-frontends/rishimun"
    ["mithila"]="/home/pms/pms-frontends/mithila"
)

# Array of server names
declare -A server_names=(
    ["lmc"]="Lalitpur Metropolitan City"
    ["kmc"]="Kathmandu Metropolitan City"
    ["jsmc"]="Janakpur Sub-Metropolitan City"
    ["rishimun"]="Rishing Municipality"
    ["mithila"]="Mithila Municipality"
)

# Array of backend directories
declare -A backend_directories=(
    ["lmc"]="/home/pms/shangrila-pms-backend"
    ["kmc"]="/home/pms/pms-backends/kmc"
    ["jsmc"]="/home/pms/pms-backends/jsmc"
    ["rishimun"]="/home/pms/pms-backends/rishimun"
    ["mithila"]="/home/pms/pms-backends/mithila"
)

# Array of backend service names
declare -A backend_service_names=(
    ["lmc"]="pms_backend_gunicorn"
    ["kmc"]="pms_backend_gunicorn_kmc"
    ["jsmc"]="pms_backend_gunicorn_jsmc"
    ["rishimun"]="pms_backend_gunicorn_rishimun"
    ["mithila"]="pms_backend_gunicorn_mithila"
)

# Array of Database users
declare -A database_users=(
    ["lmc"]="yojana_db_user"
    ["kmc"]="pms_kmclivedb"
    ["jsmc"]="pms_janakpur"
    ["rishimun"]="pms_rishingmun"
    ["mithila"]="pms_mithila"
)

# Array of Database names
declare -A database_names=(
    ["lmc"]="yojana_db"
    ["kmc"]="pms18_kmclivedb"
    ["jsmc"]="janakpur_pmsdb"
    ["rishimun"]="rishingmun_pmsdb"
    ["mithila"]="mithila_pmsdb"
)

# Array of Database passwords
declare -A database_passwords=(
    ["lmc"]="DB_PASS"
    ["kmc"]="DB_PASS"
    ["jsmc"]="DB_PASS"
    ["rishimun"]="DB_PASS"
    ["mithila"]="DB_PASS"
)

# Array of Database hosts
declare -A database_hosts=(
    ["lmc"]="127.0.0.1"
    ["kmc"]="172.19.0.24"
    ["jsmc"]="172.19.0.24"
    ["rishimun"]="172.19.0.24"
    ["mithila"]="172.19.0.24"
)