# Create Daily PRD Script (PowerShell)
# Genera automáticamente un nuevo PRD diario con nombre y estructura correctos.
#
# Uso:
#   .\create_daily_prd.ps1 [-Date "yyyyMMdd"] [-Path "./path/to/folder"]
#
# Ejemplos:
#   .\create_daily_prd.ps1                          # Crea PRD para hoy
#   .\create_daily_prd.ps1 -Date "20260217"        # Crea PRD para fecha específica
#   .\create_daily_prd.ps1 -Path "C:\My\Path"      # Crea en carpeta específica

param(
    [string]$Date,
    [string]$Path = "."
)

$ErrorActionPreference = "Stop"

# Spanish month names
$SpanishMonths = @{
    1 = "enero"
    2 = "febrero"
    3 = "marzo"
    4 = "abril"
    5 = "mayo"
    6 = "junio"
    7 = "julio"
    8 = "agosto"
    9 = "septiembre"
    10 = "octubre"
    11 = "noviembre"
    12 = "diciembre"
}

# Function to format date to Spanish format
function Format-SpanishDate {
    param([datetime]$DateObj)
    
    $day = $DateObj.Day
    $month = $SpanishMonths[$DateObj.Month]
    $year = $DateObj.Year
    
    return "$day de $month de $year"
}

# Function to parse YYYYMMDD format
function Parse-DateString {
    param([string]$DateStr)
    
    try {
        return [datetime]::ParseExact($DateStr, "yyyyMMdd", $null)
    }
    catch {
        throw "Formato de fecha inválido: $DateStr. Use yyyyMMdd"
    }
}

# Determine date
if ([string]::IsNullOrWhiteSpace($Date)) {
    $DateObj = Get-Date
} else {
    $DateObj = Parse-DateString $Date
}

# Create directory if it doesn't exist
$OutputDir = New-Item -ItemType Directory -Path $Path -Force
$DateFormatted = $DateObj.ToString("yyyyMMdd")
$Filename = "PRD_$DateFormatted.md"
$FilePath = Join-Path -Path $OutputDir.FullName -ChildPath $Filename

# Check if file already exists
if (Test-Path $FilePath) {
    Write-Host "❌ Error: Archivo ya existe: $FilePath" -ForegroundColor Red
    exit 1
}

# Template
$DateSpanish = Format-SpanishDate $DateObj

$Template = @"
# PRD - $DateSpanish

## Resumen Ejecutivo

Documento de registro de tareas realizadas durante el día con descripciones, soluciones y horas de ejecución.

---

## Tareas Realizadas

| # | Tarea | Descripción | Solución | Hora |
|---|-------|-------------|----------|------|
| | | | | |

---

## Tareas Pendientes

*Ninguna por el momento*

---

## Notas Adicionales

- Documento creado para seguimiento de tareas diarias
- Se actualizará conforme se realicen actividades
"@

# Write file
try {
    Set-Content -Path $FilePath -Value $Template -Encoding UTF8
    Write-Host "✅ Creado exitosamente: $FilePath" -ForegroundColor Green
    exit 0
}
catch {
    Write-Host "❌ Error al crear archivo: $_" -ForegroundColor Red
    exit 1
}
