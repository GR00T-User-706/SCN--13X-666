# ShadowVeil Installation Script (Windows)

# Check for admin privileges
$isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "⚠️  Run as Administrator for full functionality" -ForegroundColor Yellow
    $choice = Read-Host "Continue without admin? [y/N]"
    if ($choice -ne 'y') { exit }
}

# Verify Python
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Python not found. Please install Python 3.8+ from python.org" -ForegroundColor Red
    exit 1
}

# Create virtual environment
$venvPath = "$env:USERPROFILE\.shadowveil_venv"
Write-Host "🔧 Creating virtual environment..." -ForegroundColor Cyan
python -m venv $venvPath
& "$venvPath\Scripts\activate.ps1"

# Install package
Write-Host "⬇️  Installing ShadowVeil..." -ForegroundColor Cyan
pip install git+https://github.com/your-username/shadowveil.git

# Create shortcut
$shortcutPath = "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\ShadowVeil.lnk"
$targetPath = "$venvPath\Scripts\shadowveil.exe"

if (Test-Path $targetPath) {
    $WshShell = New-Object -ComObject WScript.Shell
    $Shortcut = $WshShell.CreateShortcut($shortcutPath)
    $Shortcut.TargetPath = $targetPath
    $Shortcut.Save()
}

# Verify installation
if (Test-Path $targetPath) {
    Write-Host "`n✅ Installation complete!" -ForegroundColor Green
    Write-Host "Run 'shadowveil --help' from Start Menu or PowerShell`n" -ForegroundColor Cyan
} else {
    Write-Host "`n❌ Installation failed!" -ForegroundColor Red
    Write-Host "Manual activation:" -ForegroundColor Yellow
    Write-Host "1. Open PowerShell"
    Write-Host "2. & '$venvPath\Scripts\Activate.ps1'"
    Write-Host "3. shadowveil --help"
}

# Hub integration instructions
Write-Host "`nFor dashboard integration:" -ForegroundColor Magenta
Write-Host "1. Add this path to your hub's module directory:"
Write-Host "   $venvPath\Lib\site-packages\shadowveil"
Write-Host "2. Restart your cybersecurity hub`n" -ForegroundColor Cyan