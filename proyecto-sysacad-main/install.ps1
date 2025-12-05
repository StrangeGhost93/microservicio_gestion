<#
Instalación de dependencias con entorno virtual local (.venv)

Este script:
	1) Crea un entorno virtual local en .venv si no existe.
	2) Activa ese entorno virtual.
	3) Actualiza pip/setuptools/wheel (opcional) y luego instala requirements.txt.

Nota: No usa rutas absolutas del autor. Todo es relativo al directorio del repo.
#>

$ErrorActionPreference = 'Stop'

# Ir al directorio donde está este script (raíz del repo)
Set-Location -Path $PSScriptRoot

$venvPath = Join-Path $PSScriptRoot '.venv'
$activatePs1 = Join-Path $venvPath 'Scripts/Activate.ps1'

if (-not (Test-Path $venvPath)) {
		Write-Host "Creando entorno virtual en: $venvPath" -ForegroundColor Cyan
		python -m venv $venvPath
}

if (-not (Test-Path $activatePs1)) {
		throw "No se encontró el script de activación: $activatePs1. Revisa que Python esté instalado y que la creación del venv haya sido exitosa."
}

Write-Host "Activando entorno virtual local (.venv)..." -ForegroundColor Cyan
& $activatePs1

Write-Host "Actualizando instaladores base..." -ForegroundColor DarkCyan
python -m pip install --upgrade pip setuptools wheel

Write-Host "Instalando dependencias desde requirements.txt..." -ForegroundColor Cyan
pip install -r requirements.txt

Write-Host "✅ Dependencias instaladas en el entorno .venv" -ForegroundColor Green