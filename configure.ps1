# PowerShell script equivalent to configure.sh

$CONFIG_DIR = ".\django_backend\config"
$FRONTEND_DIR = ".\qrcode_frontend"

# Print function
function Write-Status {
    param(
        [string]$Level,
        [string]$Message
    )
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Write-Host "[$timestamp] [$Level] $Message"
}

# Error handling
$ErrorActionPreference = "Stop"
trap {
    Write-Status -Level "ERROR" -Message "An error occurred on line $($_.InvocationInfo.ScriptLineNumber)"
    exit 1
}

# Create config directories
Write-Status -Level "INFO" -Message "Creating config directories"
New-Item -ItemType Directory -Force -Path $CONFIG_DIR | Out-Null
New-Item -ItemType Directory -Force -Path $FRONTEND_DIR | Out-Null

# Function to create config files
function New-ConfigFile {
    param(
        [string]$File,
        [string]$Content
    )
    $filename = Split-Path $File -Leaf
    Write-Status -Level "INFO" -Message "Creating: $filename"
    Set-Content -Path $File -Value $Content
    Write-Status -Level "INFO" -Message "Created: $filename"
}

# frontend .env
New-ConfigFile -File "$FRONTEND_DIR\.env" -Content "SECRET_BASE_API=http://localhost:8000"

# Summary
Write-Status -Level "INFO" -Message "Configuration setup completed"
Write-Host "`nCreated files:"
Get-ChildItem -Path $CONFIG_DIR, "$FRONTEND_DIR\.env" -File | ForEach-Object {
    Get-Item $_.FullName | Select-Object Mode, LastWriteTime, Length, Name
}
