Write-Host "Creating venv..." -ForegroundColor Cyan
python -m venv $PSScriptRoot\_venv

Write-Host "Entering venv..." -ForegroundColor Cyan
& $PSScriptRoot\_venv\Scripts\Activate.ps1

Write-Host "Installing packages..." -ForegroundColor Cyan
pip install -r $PSScriptRoot\requirements.txt

Write-Host "Done!" -ForegroundColor Cyan