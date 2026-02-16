#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Daily Hours Report Generator
    Genera un reporte de horas trabajadas a partir de un PRD diario.

.DESCRIPTION
    Lee un archivo PRD_YYYYMMDD.md, extrae las tareas y sus horas,
    calcula las duraciones y genera un reporte de horas trabajadas.

.PARAMETER PRDFile
    Ruta del archivo PRD a analizar (ej: PRD_260216.md)

.PARAMETER Output
    Directorio de salida para el reporte (opcional, por defecto: mismo directorio que PRD)

.EXAMPLE
    .\generate_hours_report.ps1 -PRDFile "PRD_260216.md"

.EXAMPLE
    .\generate_hours_report.ps1 -PRDFile "PRD_260216.md" -Output "./reports"
#>

param(
    [Parameter(Mandatory=$true)]
    [string]$PRDFile,
    
    [Parameter(Mandatory=$false)]
    [string]$Output
)

function Parse-Time {
    param([string]$TimeStr)
    
    try {
        $time = [datetime]::ParseExact($TimeStr.Trim(), "HH:mm", $null)
        return $time.TimeOfDay
    }
    catch {
        return $null
    }
}

function Calculate-Duration {
    param(
        [timespan]$StartTime,
        [timespan]$EndTime
    )
    
    if ($null -eq $StartTime -or $null -eq $EndTime) {
        return $null
    }
    
    $start_mins = $StartTime.TotalMinutes
    $end_mins = $EndTime.TotalMinutes
    
    if ($end_mins -ge $start_mins) {
        return [int]($end_mins - $start_mins)
    }
    else {
        return [int]((24 * 60 - $start_mins) + $end_mins)
    }
}

function Extract-Tasks {
    param([string]$Content)
    
    $tasks = @()
    # PatrÃ³n efectivo: ### [algo] N. DescripciÃ³n â€” **HH:MM**
    # Busca: lÃ­nea con ###, nÃºmero, punto, descripciÃ³n, y hora en formato HH:MM
    $pattern = '###\s+.+?\s+(\d+)\.\s+(.+?)\s+\*\*(\d{2}:\d{2})\*\*'
    
    $matches = [regex]::Matches($Content, $pattern, [System.Text.RegularExpressions.RegexOptions]::Singleline)
    
    foreach ($match in $matches) {
        $taskNum = $match.Groups[1].Value
        $taskName = $match.Groups[2].Value.Trim()
        $timeStr = $match.Groups[3].Value
        $timeObj = Parse-Time -TimeStr $timeStr
        
        if ($null -ne $timeObj) {
            $tasks += [PSCustomObject]@{
                Number  = $taskNum
                Name    = $taskName
                Time    = $timeObj
                TimeStr = $timeStr
            }
        }
    }
    
    return $tasks
}

function Generate-Report {
    param(
        [string]$PRDFile,
        [string]$OutputDir
    )
    
    # Verificar que el archivo existe
    if (-not (Test-Path $PRDFile)) {
        return $null, "Archivo no encontrado: $PRDFile"
    }
    
    # Leer contenido
    $content = Get-Content -Path $PRDFile -Raw -Encoding UTF8
    
    # Extraer fecha
    if ($content -match '# PRD - ([^`n]+)') {
        $dateStr = $matches[1]
    }
    else {
        return $null, "No se encontrÃ³ la fecha en el PRD"
    }
    
    # Extraer tareas
    $tasks = Extract-Tasks -Content $content
    
    if ($tasks.Count -eq 0) {
        return $null, "No se encontraron tareas con horas"
    }
    
    # Calcular duraciones
    $taskDurations = @()
    $totalMinutes = 0
    
    for ($i = 0; $i -lt $tasks.Count; $i++) {
        $task = $tasks[$i]
        $durationMins = $null
        
        if ($i -lt $tasks.Count - 1) {
            # DuraciÃ³n = hora de prÃ³xima tarea - hora actual
            $startTime = $task.Time
            $endTime = $tasks[$i + 1].Time
            $durationMins = Calculate-Duration -StartTime $startTime -EndTime $endTime
            $totalMinutes += $durationMins
        }
        else {
            # Para la Ãºltima tarea, asumir 1 hora
            $durationMins = 60
            $totalMinutes += $durationMins
        }
        
        $hours = [int]($durationMins / 60)
        $mins = $durationMins % 60
        $durationStr = if ($durationMins -ge 60) { 
            "{0}h {1}m" -f $hours, $mins 
        } 
        else { 
            "{0}m" -f $durationMins 
        }
        
        $taskDurations += [PSCustomObject]@{
            Number      = $task.Number
            Name        = $task.Name
            Time        = $task.TimeStr
            DurationMins = $durationMins
            DurationStr = $durationStr
        }
    }
    
    # Generar contenido del reporte
    $totalHours = [int]($totalMinutes / 60)
    $remainingMins = $totalMinutes % 60
    $totalHoursDecimal = [math]::Round($totalMinutes / 60, 2)
    
    $reportContent = @"
# Reporte de Horas â€” $dateStr

## Resumen

- **Tareas**: $($taskDurations.Count)
- **Horas totales**: $($totalHours)h $($remainingMins)m ($($totalHoursDecimal)h)

---

## Desglose por Tarea

"@
    
    foreach ($task in $taskDurations) {
        $reportContent += @"
### $($task.Number). $($task.Name)
- **Hora inicio**: $($task.Time)
- **DuraciÃ³n**: $($task.DurationStr)

"@
    }
    
    $avgMinutes = [math]::Round($totalMinutes / $taskDurations.Count, 0)
    
    $reportContent += @"
---

## Totales

**Horas trabajadas**: $($totalHours)h $($remainingMins)m
**Promedio por tarea**: $avgMinutes minutos
**Generado**: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
"@
    
    # Determinar archivo de salida
    if ($Output) {
        $outputPath = $Output
        if (-not (Test-Path $outputPath)) {
            New-Item -ItemType Directory -Path $outputPath -Force | Out-Null
        }
        $prdFileName = (Get-Item $PRDFile).BaseName
        $reportFile = Join-Path $outputPath "HORAS_$prdFileName.md"
    }
    else {
        $prdDir = (Get-Item $PRDFile).Directory.FullName
        $prdFileName = (Get-Item $PRDFile).BaseName
        $reportFile = Join-Path $prdDir "HORAS_$prdFileName.md"
    }
    
    # Escribir reporte
    try {
        $reportContent | Out-File -FilePath $reportFile -Encoding UTF8
        return $reportFile, "Reporte generado exitosamente"
    }
    catch {
        return $null, "Error al generar reporte: $($_.Exception.Message)"
    }
}

# Ejecutar generaciÃ³n
$reportFile, $message = Generate-Report -PRDFile $PRDFile -OutputDir $Output

if ($reportFile) {
    Write-Host "âœ… $message" -ForegroundColor Green
    Write-Host "   Archivo: $reportFile"
    exit 0
}
else {
    Write-Host "âŒ Error: $message" -ForegroundColor Red
    exit 1
}

