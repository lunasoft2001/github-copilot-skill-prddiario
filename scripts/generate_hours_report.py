#!/usr/bin/env python3
"""
Daily Hours Report Generator
Genera un reporte de horas trabajadas a partir de un PRD diario.

Uso:
    python generate_hours_report.py PRD_YYYYMMDD.md [--output ./path]

Ejemplos:
    python generate_hours_report.py PRD_260216.md
    python generate_hours_report.py PRD_260216.md --output ./reports
"""

import argparse
import os
import json
import re
from pathlib import Path
from datetime import datetime, time

# Load configuration
CONFIG_FILE = Path(__file__).parent.parent / "config.json"
DEFAULT_OUTPUT_DIR = None

if CONFIG_FILE.exists():
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            config = json.load(f)
            default_output = config.get("prd_output_directory", None)
            if default_output:
                DEFAULT_OUTPUT_DIR = os.path.expanduser(default_output)
    except Exception:
        pass

def parse_time(time_str):
    """Parse time string in HH:MM format to time object."""
    try:
        return datetime.strptime(time_str.strip(), "%H:%M").time()
    except ValueError:
        return None

def calculate_duration(start_time, end_time):
    """Calculate duration in minutes between two times."""
    if not start_time or not end_time:
        return None
    
    # Convert to minutes since midnight
    start_mins = start_time.hour * 60 + start_time.minute
    end_mins = end_time.hour * 60 + end_time.minute
    
    if end_mins >= start_mins:
        return end_mins - start_mins
    else:
        # Handle day wrap (shouldn't happen in normal case)
        return (24 * 60 - start_mins) + end_mins

def extract_tasks_from_prd(prd_content):
    """Extract tasks and times from PRD content."""
    tasks = []
    
    # Pattern: ### [character] N. Description **HH:MM**
    pattern = r'###\s+.+?\s+(\d+)\.\s+(.+?)\s+\*\*(\d{2}:\d{2})\*\*'
    
    matches = re.finditer(pattern, prd_content, re.DOTALL)
    for match in matches:
        task_num = match.group(1)
        task_name = match.group(2).strip()
        time_str = match.group(3)
        time_obj = parse_time(time_str)
        
        if time_obj:
            tasks.append({
                'number': task_num,
                'name': task_name,
                'time': time_obj,
                'time_str': time_str
            })
    
    return tasks

def generate_report(prd_file, output_dir=None):
    """Generate hours report from PRD file."""
    
    # Use default output dir if not specified
    if output_dir is None:
        output_dir = DEFAULT_OUTPUT_DIR
    
    # Read PRD file
    prd_path = Path(prd_file)
    if not prd_path.exists():
        return None, f"Archivo no encontrado: {prd_file}"
    
    with open(prd_path, 'r', encoding='utf-8') as f:
        prd_content = f.read()
    
    # Extract date from PRD
    date_match = re.search(r'# PRD - (\d{1,2} de \w+ de \d{4})', prd_content)
    if not date_match:
        return None, "No se encontró la fecha en el PRD"
    
    date_str = date_match.group(1)
    
    # Extract tasks
    tasks = extract_tasks_from_prd(prd_content)
    
    if not tasks:
        return None, "No se encontraron tareas con horas"
    
    # Calculate durations
    task_durations = []
    total_minutes = 0
    
    for i, task in enumerate(tasks):
        if i < len(tasks) - 1:
            # Duration = time of next task - time of current task
            start_time = task['time']
            end_time = tasks[i + 1]['time']
            duration_mins = calculate_duration(start_time, end_time)
            total_minutes += duration_mins
        else:
            # For last task, estimate based on typical work session
            duration_mins = 60  # Default 1 hour for last task
            total_minutes += duration_mins
        
        task_durations.append({
            'number': task['number'],
            'name': task['name'],
            'time': task['time_str'],
            'duration_mins': duration_mins,
            'duration_str': f"{duration_mins // 60}h {duration_mins % 60}m" if duration_mins >= 60 else f"{duration_mins}m"
        })
    
    # Generate report content
    report_content = f"""# Reporte de Horas – {date_str}

## Resumen

- **Tareas**: {len(task_durations)}
- **Horas totales**: {total_minutes // 60}h {total_minutes % 60}m ({total_minutes / 60:.2f}h)

---

## Desglose por Tarea

"""
    
    for task in task_durations:
        report_content += f"### {task['number']}. {task['name']}\n"
        report_content += f"- **Hora inicio**: {task['time']}\n"
        report_content += f"- **Duración**: {task['duration_str']}\n\n"
    
    report_content += "---\n\n"
    report_content += f"## Totales\n\n"
    report_content += f"**Horas trabajadas**: {total_minutes // 60}h {total_minutes % 60}m\n"
    report_content += f"**Promedio por tarea**: {total_minutes / len(task_durations):.0f} minutos\n"
    report_content += f"**Generado**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    
    # Determine output file
    if output_dir:
        output_path = Path(output_dir).expanduser()
        output_path.mkdir(parents=True, exist_ok=True)
        report_file = output_path / f"HORAS_{prd_path.stem}.md"
    else:
        report_file = prd_path.parent / f"HORAS_{prd_path.stem}.md"
    
    # Write report
    try:
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report_content)
        return str(report_file), "Reporte generado exitosamente"
    except Exception as e:
        return None, f"Error al generar reporte: {str(e)}"

def main():
    parser = argparse.ArgumentParser(
        description="Generar reporte de horas trabajadas a partir de PRD diario",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  python generate_hours_report.py PRD_260216.md
  python generate_hours_report.py PRD_260216.md --output ./reports
        """
    )
    parser.add_argument('prd_file', help='Archivo PRD a analizar')
    parser.add_argument('--output', help=f'Directorio de salida para el reporte (default: {DEFAULT_OUTPUT_DIR or "mismo dir del PRD"})')
    
    args = parser.parse_args()
    
    report_file, message = generate_report(args.prd_file, args.output)
    
    if report_file:
        print(f"✅ {message}")
        print(f"   Archivo: {report_file}")
        return 0
    else:
        print(f"❌ {message}")
        return 1

if __name__ == "__main__":
    exit(main())
