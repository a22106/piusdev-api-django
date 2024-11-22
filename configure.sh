#!/bin/bash

CONFIG_DIR="./django_backend/config"
FRONTEND_DIR="./qrcode_frontend"

# Print function
print_status() {
    local level=$1
    shift
    local message=$@
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] [$level] $message"
}


# Error handling
set -e
trap 'print_status ERROR "An error occurred on line $LINENO"' ERR

# Create config directories
print_status INFO "Creating config directories"
mkdir -p "$CONFIG_DIR"
mkdir -p "$FRONTEND_DIR"


# Function to create config files
create_config() {
    local file=$1
    local content=$2
    local filename=$(basename "$file")

    print_status INFO "Creating: $filename"
    echo "$content" > "$file" && print_status INFO "Created: $filename"
}

# frontend .env
create_config "$FRONTEND_DIR/.env" "SECRET_BASE_API=http://localhost:8000"

# Summary
print_status INFO "Configuration setup completed"
echo -e "\nCreated files:"
find "$CONFIG_DIR" "$FRONTEND_DIR/.env" -type f -exec ls -l {} \;