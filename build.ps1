# build.ps1 - Build portable EXE with PyInstaller

# Check if Python is available
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Error "Python is not installed or not in PATH. Please install Python and try again."
    exit 1
}

# Install PyInstaller if missing
Write-Host "Checking PyInstaller..."
$pyInstallerCheck = python -m pip show pyinstaller 2>$null
if (-not $pyInstallerCheck) {
    Write-Host "PyInstaller not found, installing..."
    python -m pip install pyinstaller
}

# Define paths
$scriptName = "video_cleaner_gui.py"
$iconPath = "app_icon.ico"
$versionFile = "version.txt"

# Check required files
if (-not (Test-Path $scriptName)) {
    Write-Error "Script file '$scriptName' not found."
    exit 1
}
if (-not (Test-Path $iconPath)) {
    Write-Warning "Icon file '$iconPath' not found. Building without icon."
    $iconPath = $null
}
if (-not (Test-Path $versionFile)) {
    Write-Warning "Version file '$versionFile' not found. Building without version info."
    $versionFile = $null
}

# Build command construction
$buildCmd = "pyinstaller --noconfirm --onefile --windowed"
if ($iconPath) { $buildCmd += " --icon=`"$iconPath`"" }
if ($versionFile) { $buildCmd += " --version-file=`"$versionFile`"" }
$buildCmd += " `"$scriptName`""

Write-Host "Running build command:"
Write-Host $buildCmd

# Run the build
Invoke-Expression $buildCmd

Write-Host "Build finished. Check the 'dist' folder for your EXE."
