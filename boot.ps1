param (
    [string]$VAR_CONTEXT
)

if ($VAR_CONTEXT -eq "production") {
    $VAR_CONTEXT = "production"
} else {
    $VAR_CONTEXT = "development"
}

Write-Output "environment set to: $VAR_CONTEXT"
$env:FLASK_CONTEXT = $VAR_CONTEXT

# Usar Python del .venv si existe
$repoRoot = $PSScriptRoot
$venvPython = Join-Path $repoRoot '.venv/Scripts/python.exe'
if (Test-Path $venvPython) {
    & $venvPython app.py
} else {
    python app.py
}