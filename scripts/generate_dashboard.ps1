#!/usr/bin/env pwsh
<#
.SYNOPSIS
    PRD Dashboard Generator
    Convierte un PRD Markdown a un Dashboard HTML visual e interactivo.

.PARAMETER PRDFile
    Archivo PRD a convertir (ej: PRD_260216.md)

.PARAMETER Output
    Directorio de salida (opcional)

.EXAMPLE
    .\generate_dashboard.ps1 -PRDFile "PRD_260216.md"

.EXAMPLE
    .\generate_dashboard.ps1 -PRDFile "PRD_260216.md" -Output "./dashboards"
#>

param(
    [Parameter(Mandatory=$true)]
    [string]$PRDFile,
    
    [Parameter(Mandatory=$false)]
    [string]$Output
)

function Parse-PRD {
    param([string[]]$Lines)
    
    $data = @{
        date = ''
        summary = @{}
        completed_tasks = @()
        pending_tasks = @()
        notes = ''
    }
    
    # Extract date
    $dateMatch = $lines | Where-Object { $_.Contains('# PRD -') } | Select-Object -First 1
    if ($dateMatch) {
        $data.date = $dateMatch.Replace('# PRD - ', '').Trim()
    }
    
    # Simple task extraction - just look for lines starting with ###
    for ($i = 0; $i -lt $lines.Count; $i++) {
        $line = $lines[$i]
        
        # Must start with ###
        if ($line.Length -lt 3 -or $line.Substring(0, 3) -ne '###') {
            continue
        }
        
        # Must contain emoji
        if (-not ($line.Contains('✅') -or $line.Contains('⏳'))) {
            continue
        }
        
        $isCompleted = $line.Contains('✅')
        
        # Extract task number using simple method
        $numMatch = $line | Select-String -Pattern '(\d+)\.'
        if ($null -eq $numMatch) { continue }
        $taskNum = $numMatch.Matches[0].Groups[1].Value
        
        # Extract name - everything after number and before em-dash or separator
        $dashPos = $line.IndexOf('—')
        if ($dashPos -lt 0) {
            $dashPos = $line.IndexOf('--')
        }
        if ($dashPos -lt 0) { continue }
        
        # Find start of name (after ".")
        $dotPos = $line.IndexOf('.')
        if ($dotPos -lt 0) { continue }
        $taskName = $line.Substring($dotPos + 1, $dashPos - $dotPos - 1).Trim()
        
        # Extract time between ** **
        $timeMatch = $line | Select-String -Pattern '\*\*([^*]+)\*\*'
        $taskTime = if ($null -ne $timeMatch) { $timeMatch.Matches[0].Groups[1].Value } else { '' }
        
        # Get description (next non-empty lines after **Description**)
        $description = ''
        $solution = ''
        $status = ''
        
        $j = $i + 1
        while ($j -lt $lines.Count -and -not $lines[$j].StartsWith('###')) {
            if ($lines[$j].Contains('**Descripción**') -or $lines[$j].Contains('**Descripcion**')) {
                $j++
                while ($j -lt $lines.Count -and $lines[$j].Trim() -ne '' -and -not $lines[$j].Contains('**')) {
                    $description += $lines[$j].Trim() + ' '
                    $j++
                }
                $description = $description.Trim()
            } elseif ($lines[$j].Contains('**Solución**') -or $lines[$j].Contains('**Solucion**')) {
                $j++
                while ($j -lt $lines.Count -and $lines[$j].Trim() -ne '' -and -not $lines[$j].Contains('**') -and -not $lines[$j].StartsWith('---')) {
                    $solution += $lines[$j].Trim() + ' '
                    $j++
                }
                $solution = $solution.Trim()
            } elseif ($lines[$j].Contains('**Estado**')) {
                $j++
                while ($j -lt $lines.Count -and $lines[$j].Trim() -ne '' -and -not $lines[$j].Contains('**') -and -not $lines[$j].StartsWith('---')) {
                    $status += $lines[$j].Trim() + ' '
                    $j++
                }
                $status = $status.Trim()
            } else {
                $j++
            }
        }
        
        # Add task
        if ($isCompleted) {
            $data.completed_tasks += @{
                number = $taskNum
                name = $taskName
                time = $taskTime
                description = $description
                solution = $solution
            }
        } else {
            $data.pending_tasks += @{
                number = $taskNum
                name = $taskName
                time = $taskTime
                description = $description
                status = $status
            }
        }
    }
    
    return $data
}

function Generate-HTML {
    param([hashtable]$PRDData)
    
    $completedCount = $PRDData.completed_tasks.Count
    $pendingCount = $PRDData.pending_tasks.Count
    $totalTasks = $completedCount + $pendingCount
    $completionPct = if ($totalTasks -gt 0) { [int]($completedCount / $totalTasks * 100) } else { 0 }
    
    if ($PRDData.summary.ContainsKey('Total de horas')) {
        $totalHours = $PRDData.summary['Total de horas']
    } else {
        $totalHours = '0h 0m'
    }
    
    # Generate completed tasks HTML
    $completedHtml = ''
    foreach ($task in $PRDData.completed_tasks) {
        $completedHtml += @"
        <div class="task-card completed" data-task-id="completed-$($task.number)">
            <div class="task-header">
                <span class="task-emoji">✅</span>
                <h3 class="task-title">$($task.number). $($task.name)</h3>
                <span class="task-time">🕐 $($task.time)</span>
            </div>
            <div class="task-body">
                <div class="task-section">
                    <h4>📝 Descripción</h4>
                    <p>$($task.description)</p>
                </div>
                <div class="task-section">
                    <h4>✔️ Solución</h4>
                    <p>$($task.solution)</p>
                </div>
            </div>
        </div>

"@
    }
    
    # Generate pending tasks HTML
    $pendingHtml = ''
    foreach ($task in $PRDData.pending_tasks) {
        $pendingHtml += @"
        <div class="task-card pending" data-task-id="pending-$($task.number)">
            <div class="task-header">
                <span class="task-emoji">⏳</span>
                <h3 class="task-title">$($task.number). $($task.name)</h3>
                <span class="task-time">🕐 $($task.time)</span>
            </div>
            <div class="task-body">
                <div class="task-section">
                    <h4>📝 Descripción</h4>
                    <p>$($task.description)</p>
                </div>
                <div class="task-section">
                    <h4>📊 Estado</h4>
                    <p><strong>$($task.status)</strong></p>
                </div>
            </div>
        </div>

"@
    }
    
    if ([string]::IsNullOrEmpty($completedHtml)) {
        $completedHtml = '<div class="empty-state"><div class="empty-state-icon">📭</div><p>No hay tareas completadas aún</p></div>'
    }
    
    if ([string]::IsNullOrEmpty($pendingHtml)) {
        $pendingHtml = '<div class="empty-state"><div class="empty-state-icon">✨</div><p>¡No hay tareas pendientes! 🎉</p></div>'
    }
    
    $timestamp = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'
    
    $html = @"
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PRD Dashboard - $($PRDData.date)</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        :root {
            --primary: #6366f1;
            --primary-dark: #4f46e5;
            --success: #10b981;
            --warning: #f59e0b;
            --bg-dark: #0f172a;
            --bg-light: #f8fafc;
            --card-dark: #1e293b;
            --card-light: #ffffff;
            --text-dark: #e2e8f0;
            --text-light: #1e293b;
            --border-dark: #334155;
            --border-light: #e2e8f0;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            transition: background-color 0.3s, color 0.3s;
            padding: 20px;
        }
        
        body.dark-mode {
            background-color: var(--bg-dark);
            color: var(--text-dark);
        }
        
        body.light-mode {
            background-color: var(--bg-light);
            color: var(--text-light);
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 40px;
            padding-bottom: 20px;
            border-bottom: 2px solid var(--border-dark);
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 5px;
        }
        
        .header-date {
            font-size: 1.1em;
            opacity: 0.8;
        }
        
        .theme-toggle {
            background: var(--primary);
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 1em;
            transition: background-color 0.3s;
        }
        
        .theme-toggle:hover {
            background-color: var(--primary-dark);
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }
        
        .stat-card {
            padding: 25px;
            border-radius: 12px;
            border: 1px solid var(--border-dark);
        }
        
        body.dark-mode .stat-card {
            background-color: var(--card-dark);
        }
        
        body.light-mode .stat-card {
            background-color: var(--card-light);
            border-color: var(--border-light);
        }
        
        .stat-card h3 {
            font-size: 0.9em;
            opacity: 0.7;
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .stat-value {
            font-size: 2.5em;
            font-weight: bold;
            color: var(--primary);
            margin-bottom: 10px;
        }
        
        .stat-subtext {
            font-size: 0.9em;
            opacity: 0.7;
        }
        
        .progress-bar {
            width: 100%;
            height: 8px;
            background-color: var(--border-dark);
            border-radius: 4px;
            overflow: hidden;
            margin-top: 10px;
        }
        
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, var(--success), var(--primary));
            transition: width 0.5s ease;
        }
        
        .section {
            margin-bottom: 50px;
        }
        
        .section h2 {
            font-size: 1.8em;
            margin-bottom: 25px;
            padding-bottom: 10px;
            border-bottom: 3px solid var(--primary);
        }
        
        .tasks-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 20px;
        }
        
        .task-card {
            border-radius: 12px;
            border: 2px solid var(--border-dark);
            overflow: hidden;
            transition: all 0.3s;
            cursor: pointer;
        }
        
        body.dark-mode .task-card {
            background-color: var(--card-dark);
        }
        
        body.light-mode .task-card {
            background-color: var(--card-light);
            border-color: var(--border-light);
        }
        
        .task-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(99, 102, 241, 0.2);
        }
        
        .task-card.completed .task-header {
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(99, 102, 241, 0.1));
            border-bottom: 2px solid var(--success);
        }
        
        .task-card.pending .task-header {
            background: linear-gradient(135deg, rgba(245, 158, 11, 0.1), rgba(99, 102, 241, 0.1));
            border-bottom: 2px solid var(--warning);
        }
        
        .task-header {
            padding: 20px;
            display: flex;
            align-items: center;
            gap: 15px;
        }
        
        .task-emoji {
            font-size: 1.8em;
        }
        
        .task-title {
            flex: 1;
            font-size: 1.1em;
        }
        
        .task-time {
            font-size: 0.9em;
            opacity: 0.7;
            white-space: nowrap;
        }
        
        .task-body {
            padding: 20px;
        }
        
        .task-section {
            margin-bottom: 15px;
        }
        
        .task-section:last-child {
            margin-bottom: 0;
        }
        
        .task-section h4 {
            font-size: 0.9em;
            margin-bottom: 8px;
            opacity: 0.8;
            font-weight: 600;
        }
        
        .task-section p {
            font-size: 0.95em;
            line-height: 1.6;
            opacity: 0.9;
        }
        
        .empty-state {
            text-align: center;
            padding: 40px;
            opacity: 0.6;
        }
        
        .empty-state-icon {
            font-size: 3em;
            margin-bottom: 10px;
        }
        
        @media (max-width: 768px) {
            .header {
                flex-direction: column;
                gap: 20px;
                text-align: center;
            }
            
            .tasks-grid {
                grid-template-columns: 1fr;
            }
            
            .stats-grid {
                grid-template-columns: 1fr;
            }
        }
        
        footer {
            text-align: center;
            margin-top: 50px;
            padding-top: 20px;
            border-top: 1px solid var(--border-dark);
            opacity: 0.6;
            font-size: 0.9em;
        }
    </style>
</head>
<body class="dark-mode">
    <div class="container">
        <div class="header">
            <div>
                <h1>📊 PRD Dashboard</h1>
                <p class="header-date">📅 $($PRDData.date)</p>
            </div>
            <button class="theme-toggle" onclick="toggleTheme()">🌙 Modo Oscuro</button>
        </div>
        
        <!-- Estadísticas -->
        <div class="stats-grid">
            <div class="stat-card">
                <h3>Tareas Completadas</h3>
                <div class="stat-value">$completedCount</div>
                <div class="stat-subtext">de $totalTasks tareas totales</div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: $completionPct%"></div>
                </div>
            </div>
            
            <div class="stat-card">
                <h3>Tareas Pendientes</h3>
                <div class="stat-value">$pendingCount</div>
                <div class="stat-subtext">en progreso</div>
            </div>
            
            <div class="stat-card">
                <h3>Horas Trabajadas</h3>
                <div class="stat-value">$totalHours</div>
                <div class="stat-subtext">productividad del día</div>
            </div>
            
            <div class="stat-card">
                <h3>Tasa de Completación</h3>
                <div class="stat-value">$completionPct%</div>
                <div class="stat-subtext">progreso diario</div>
            </div>
        </div>
        
        <!-- Tareas Completadas -->
        <div class="section">
            <h2>✅ Tareas Completadas ($completedCount)</h2>
            <div class="tasks-grid">
                $completedHtml
            </div>
        </div>
        
        <!-- Tareas Pendientes -->
        <div class="section">
            <h2>⏳ Tareas Pendientes ($pendingCount)</h2>
            <div class="tasks-grid">
                $pendingHtml
            </div>
        </div>
        
        <footer>
            <p>Dashboard generado: $timestamp</p>
            <p>💾 Datos vinculados desde PRD Markdown</p>
        </footer>
    </div>
    
    <script>
        // Tema oscuro/claro
        function toggleTheme() {
            const body = document.body;
            const button = document.querySelector('.theme-toggle');
            
            if (body.classList.contains('dark-mode')) {
                body.classList.remove('dark-mode');
                body.classList.add('light-mode');
                button.textContent = '☀️ Modo Claro';
                localStorage.setItem('theme', 'light');
            } else {
                body.classList.remove('light-mode');
                body.classList.add('dark-mode');
                button.textContent = '🌙 Modo Oscuro';
                localStorage.setItem('theme', 'dark');
            }
        }
        
        // Restaurar tema guardado
        window.addEventListener('DOMContentLoaded', () => {
            const savedTheme = localStorage.getItem('theme') || 'dark';
            document.body.classList.add(savedTheme + '-mode');
            const button = document.querySelector('.theme-toggle');
            button.textContent = savedTheme === 'dark' ? '☀️ Modo Claro' : '🌙 Modo Oscuro';
        });
    </script>
</body>
</html>
"@
    
    return $html
}

# Main logic
if (-not (Test-Path $PRDFile)) {
    Write-Host "❌ Error: Archivo no encontrado: $PRDFile" -ForegroundColor Red
    exit 1
}

# Read and parse
$lines = @(Get-Content -Path $PRDFile -Encoding UTF8)
$prdData = Parse-PRD -Lines $lines
$html = Generate-HTML -PRDData $prdData

# Determine output
if ($Output) {
    $outputPath = $Output
    if (-not (Test-Path $outputPath)) {
        New-Item -ItemType Directory -Path $outputPath -Force | Out-Null
    }
    $prdFileName = (Get-Item $PRDFile).BaseName
    $dashboardFile = Join-Path $outputPath "$prdFileName`_DASHBOARD.html"
} else {
    $prdDir = (Get-Item $PRDFile).Directory.FullName
    $prdFileName = (Get-Item $PRDFile).BaseName
    $dashboardFile = Join-Path $prdDir "$prdFileName`_DASHBOARD.html"
}

# Write HTML
try {
    $html | Out-File -FilePath $dashboardFile -Encoding UTF8
    Write-Host "✅ Dashboard generado exitosamente" -ForegroundColor Green
    Write-Host "   Archivo: $dashboardFile"
    exit 0
}
catch {
    Write-Host "❌ Error al generar dashboard: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}
