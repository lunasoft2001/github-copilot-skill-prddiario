#!/usr/bin/env python3
"""
PRD Dashboard Generator
Convierte un PRD Markdown a un Dashboard HTML visual e interactivo.

Uso:
    python generate_dashboard.py PRD_260216.md [--output ./path]

Genera: PRD_260216_DASHBOARD.html (auto-abre en navegador)
"""

import argparse
import re
import json
from pathlib import Path
from datetime import datetime

def parse_prd_markdown(content):
    """Parse PRD markdown content to extract structured data."""
    data = {
        'date': '',
        'summary': {},
        'completed_tasks': [],
        'pending_tasks': [],
        'notes': ''
    }
    
    # Extract date
    date_match = re.search(r'# PRD - (.+)', content)
    if date_match:
        data['date'] = date_match.group(1).strip()
    
    # Extract summary (key: value pairs)
    summary_section = re.search(r'## Resumen Ejecutivo\n(.*?)\n---', content, re.DOTALL)
    if summary_section:
        summary_text = summary_section.group(1)
        for line in summary_text.split('\n'):
            if '**' in line and ':' in line:
                match = re.search(r'\*\*(.+?)\*\*:\s*(.+)', line)
                if match:
                    key, value = match.groups()
                    data['summary'][key.strip()] = value.strip()
    
    # Extract completed tasks - more flexible pattern
    completed_pattern = r'###\s+.+?\s+(\d+)\.\s+(.+?)\s+(?:—|--)\s+\*\*(\d{2}:\d{2})\*\*\n+\*\*Descripción\*\*\s*\n\n?(.+?)\n+\*\*Solución\*\*\s*\n\n?(.+?)(?=\n---\n###|\n\n###|$)'
    for match in re.finditer(completed_pattern, content, re.DOTALL):
        task_num, task_name, time_str, desc, solution = match.groups()
        data['completed_tasks'].append({
            'number': task_num,
            'name': task_name.strip(),
            'time': time_str,
            'description': desc.strip(),
            'solution': solution.strip()
        })
    
    # Extract pending tasks - more flexible pattern
    pending_pattern = r'###\s+.+?\s+(\d+)\.\s+(.+?)\s+(?:—|--)\s+\*\*(\d{2}:\d{2})\*\*\n+\*\*Descripción\*\*\s*\n\n?(.+?)\n+\*\*Estado\*\*\s*\n\n?(.+?)(?=\n---\n###|\n\n###|$)'
    for match in re.finditer(pending_pattern, content, re.DOTALL):
        task_num, task_name, time_str, desc, status = match.groups()
        data['pending_tasks'].append({
            'number': task_num,
            'name': task_name.strip(),
            'time': time_str,
            'description': desc.strip(),
            'status': status.strip()
        })
    
    return data

def generate_html(prd_data):
    """Generate HTML dashboard from PRD data."""
    
    completed_count = len(prd_data['completed_tasks'])
    pending_count = len(prd_data['pending_tasks'])
    total_tasks = completed_count + pending_count
    completion_pct = int((completed_count / total_tasks * 100)) if total_tasks > 0 else 0
    
    # Extract hours from summary
    total_hours = prd_data['summary'].get('Total de horas', '0h 0m')
    
    # Generate task cards HTML
    completed_html = ''
    for task in prd_data['completed_tasks']:
        completed_html += f"""
        <div class="task-card completed" data-task-id="completed-{task['number']}">
            <div class="task-header">
                <span class="task-emoji">✅</span>
                <h3 class="task-title">{task['number']}. {task['name']}</h3>
                <span class="task-time">🕐 {task['time']}</span>
            </div>
            <div class="task-body">
                <div class="task-section">
                    <h4>📝 Descripción</h4>
                    <p>{task['description']}</p>
                </div>
                <div class="task-section">
                    <h4>✔️ Solución</h4>
                    <p>{task['solution']}</p>
                </div>
            </div>
        </div>
        """
    
    pending_html = ''
    for task in prd_data['pending_tasks']:
        pending_html += f"""
        <div class="task-card pending" data-task-id="pending-{task['number']}">
            <div class="task-header">
                <span class="task-emoji">⏳</span>
                <h3 class="task-title">{task['number']}. {task['name']}</h3>
                <span class="task-time">🕐 {task['time']}</span>
            </div>
            <div class="task-body">
                <div class="task-section">
                    <h4>📝 Descripción</h4>
                    <p>{task['description']}</p>
                </div>
                <div class="task-section">
                    <h4>📊 Estado</h4>
                    <p><strong>{task['status']}</strong></p>
                </div>
            </div>
        </div>
        """
    
    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PRD Dashboard - {prd_data['date']}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        :root {{
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
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            transition: background-color 0.3s, color 0.3s;
            padding: 20px;
        }}
        
        body.dark-mode {{
            background-color: var(--bg-dark);
            color: var(--text-dark);
        }}
        
        body.light-mode {{
            background-color: var(--bg-light);
            color: var(--text-light);
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        
        .header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 40px;
            padding-bottom: 20px;
            border-bottom: 2px solid var(--border-dark);
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 5px;
        }}
        
        .header-date {{
            font-size: 1.1em;
            opacity: 0.8;
        }}
        
        .theme-toggle {{
            background: var(--primary);
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 1em;
            transition: background-color 0.3s;
        }}
        
        .theme-toggle:hover {{
            background-color: var(--primary-dark);
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }}
        
        .stat-card {{
            padding: 25px;
            border-radius: 12px;
            border: 1px solid var(--border-dark);
        }}
        
        body.dark-mode .stat-card {{
            background-color: var(--card-dark);
        }}
        
        body.light-mode .stat-card {{
            background-color: var(--card-light);
            border-color: var(--border-light);
        }}
        
        .stat-card h3 {{
            font-size: 0.9em;
            opacity: 0.7;
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .stat-value {{
            font-size: 2.5em;
            font-weight: bold;
            color: var(--primary);
            margin-bottom: 10px;
        }}
        
        .stat-subtext {{
            font-size: 0.9em;
            opacity: 0.7;
        }}
        
        .progress-bar {{
            width: 100%;
            height: 8px;
            background-color: var(--border-dark);
            border-radius: 4px;
            overflow: hidden;
            margin-top: 10px;
        }}
        
        .progress-fill {{
            height: 100%;
            background: linear-gradient(90deg, var(--success), var(--primary));
            transition: width 0.5s ease;
        }}
        
        .section {{
            margin-bottom: 50px;
        }}
        
        .section h2 {{
            font-size: 1.8em;
            margin-bottom: 25px;
            padding-bottom: 10px;
            border-bottom: 3px solid var(--primary);
        }}
        
        .tasks-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 20px;
        }}
        
        .task-card {{
            border-radius: 12px;
            border: 2px solid var(--border-dark);
            overflow: hidden;
            transition: all 0.3s;
            cursor: pointer;
        }}
        
        body.dark-mode .task-card {{
            background-color: var(--card-dark);
        }}
        
        body.light-mode .task-card {{
            background-color: var(--card-light);
            border-color: var(--border-light);
        }}
        
        .task-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(99, 102, 241, 0.2);
        }}
        
        .task-card.completed .task-header {{
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(99, 102, 241, 0.1));
            border-bottom: 2px solid var(--success);
        }}
        
        .task-card.pending .task-header {{
            background: linear-gradient(135deg, rgba(245, 158, 11, 0.1), rgba(99, 102, 241, 0.1));
            border-bottom: 2px solid var(--warning);
        }}
        
        .task-header {{
            padding: 20px;
            display: flex;
            align-items: center;
            gap: 15px;
        }}
        
        .task-emoji {{
            font-size: 1.8em;
        }}
        
        .task-title {{
            flex: 1;
            font-size: 1.1em;
        }}
        
        .task-time {{
            font-size: 0.9em;
            opacity: 0.7;
            white-space: nowrap;
        }}
        
        .task-body {{
            padding: 20px;
        }}
        
        .task-section {{
            margin-bottom: 15px;
        }}
        
        .task-section:last-child {{
            margin-bottom: 0;
        }}
        
        .task-section h4 {{
            font-size: 0.9em;
            margin-bottom: 8px;
            opacity: 0.8;
            font-weight: 600;
        }}
        
        .task-section p {{
            font-size: 0.95em;
            line-height: 1.6;
            opacity: 0.9;
        }}
        
        .empty-state {{
            text-align: center;
            padding: 40px;
            opacity: 0.6;
        }}
        
        .empty-state-icon {{
            font-size: 3em;
            margin-bottom: 10px;
        }}
        
        @media (max-width: 768px) {{
            .header {{
                flex-direction: column;
                gap: 20px;
                text-align: center;
            }}
            
            .tasks-grid {{
                grid-template-columns: 1fr;
            }}
            
            .stats-grid {{
                grid-template-columns: 1fr;
            }}
        }}
        
        footer {{
            text-align: center;
            margin-top: 50px;
            padding-top: 20px;
            border-top: 1px solid var(--border-dark);
            opacity: 0.6;
            font-size: 0.9em;
        }}
    </style>
</head>
<body class="dark-mode">
    <div class="container">
        <div class="header">
            <div>
                <h1>📊 PRD Dashboard</h1>
                <p class="header-date">📅 {prd_data['date']}</p>
            </div>
            <button class="theme-toggle" onclick="toggleTheme()">🌙 Modo Oscuro</button>
        </div>
        
        <!-- Estadísticas -->
        <div class="stats-grid">
            <div class="stat-card">
                <h3>Tareas Completadas</h3>
                <div class="stat-value">{completed_count}</div>
                <div class="stat-subtext">de {total_tasks} tareas totales</div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {completion_pct}%"></div>
                </div>
            </div>
            
            <div class="stat-card">
                <h3>Tareas Pendientes</h3>
                <div class="stat-value">{pending_count}</div>
                <div class="stat-subtext">en progreso</div>
            </div>
            
            <div class="stat-card">
                <h3>Horas Trabajadas</h3>
                <div class="stat-value">{total_hours}</div>
                <div class="stat-subtext">productividad del día</div>
            </div>
            
            <div class="stat-card">
                <h3>Tasa de Completación</h3>
                <div class="stat-value">{completion_pct}%</div>
                <div class="stat-subtext">progreso diario</div>
            </div>
        </div>
        
        <!-- Tareas Completadas -->
        <div class="section">
            <h2>✅ Tareas Completadas ({completed_count})</h2>
            <div class="tasks-grid">
                {completed_html if completed_html else '<div class="empty-state"><div class="empty-state-icon">📭</div><p>No hay tareas completadas aún</p></div>'}
            </div>
        </div>
        
        <!-- Tareas Pendientes -->
        <div class="section">
            <h2>⏳ Tareas Pendientes ({pending_count})</h2>
            <div class="tasks-grid">
                {pending_html if pending_html else '<div class="empty-state"><div class="empty-state-icon">✨</div><p>¡No hay tareas pendientes! 🎉</p></div>'}
            </div>
        </div>
        
        <footer>
            <p>Dashboard generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p>💾 Datos vinculados desde PRD Markdown</p>
        </footer>
    </div>
    
    <script>
        // Tema oscuro/claro
        function toggleTheme() {{
            const body = document.body;
            const button = document.querySelector('.theme-toggle');
            
            if (body.classList.contains('dark-mode')) {{
                body.classList.remove('dark-mode');
                body.classList.add('light-mode');
                button.textContent = '☀️ Modo Claro';
                localStorage.setItem('theme', 'light');
            }} else {{
                body.classList.remove('light-mode');
                body.classList.add('dark-mode');
                button.textContent = '🌙 Modo Oscuro';
                localStorage.setItem('theme', 'dark');
            }}
        }}
        
        // Restaurar tema guardado
        window.addEventListener('DOMContentLoaded', () => {{
            const savedTheme = localStorage.getItem('theme') || 'dark';
            document.body.classList.add(savedTheme + '-mode');
            const button = document.querySelector('.theme-toggle');
            button.textContent = savedTheme === 'dark' ? '☀️ Modo Claro' : '🌙 Modo Oscuro';
        }});
    </script>
</body>
</html>
"""
    
    return html

def main():
    parser = argparse.ArgumentParser(
        description="Generar dashboard HTML desde PRD Markdown"
    )
    parser.add_argument('prd_file', help='Archivo PRD a convertir')
    parser.add_argument('--output', help='Directorio de salida')
    
    args = parser.parse_args()
    
    prd_path = Path(args.prd_file)
    if not prd_path.exists():
        print(f"❌ Error: Archivo no encontrado: {args.prd_file}")
        return 1
    
    # Read and parse PRD
    with open(prd_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    prd_data = parse_prd_markdown(content)
    html = generate_html(prd_data)
    
    # Determine output file
    if args.output:
        output_path = Path(args.output)
        output_path.mkdir(parents=True, exist_ok=True)
        dashboard_file = output_path / f"{prd_path.stem}_DASHBOARD.html"
    else:
        dashboard_file = prd_path.parent / f"{prd_path.stem}_DASHBOARD.html"
    
    # Write HTML
    try:
        with open(dashboard_file, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"✅ Dashboard generado exitosamente")
        print(f"   Archivo: {dashboard_file}")
        return 0
    except Exception as e:
        print(f"❌ Error al generar dashboard: {str(e)}")
        return 1

if __name__ == "__main__":
    exit(main())
