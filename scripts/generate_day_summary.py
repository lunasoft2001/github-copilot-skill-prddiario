#!/usr/bin/env python3
"""
Daily Summary Generator
Genera un resumen completo del día analizando todos los archivos en la carpeta diaria.

Características:
- Lee metadatos de archivos (fecha creación, modificación)
- Extrae tareas del PRD del día
- Calcula hora de inicio del día (primer archivo creado)
- Genera resumen con horas trabajadas y documentos
creados

Uso:
    python generate_day_summary.py [--date YYYYMMDD] [--path ./base/path] [--output ./output]

Ejemplos:
    python generate_day_summary.py                          # Resumen de hoy
    python generate_day_summary.py --date 20260225         # Resumen de fecha específica
    python generate_day_summary.py --output ./reports       # Específica carpeta de salida
"""

import argparse
import os
import json
import re
from pathlib import Path
from datetime import datetime, timedelta
import platform

# Load configuration
CONFIG_FILE = Path(__file__).parent.parent / "config.json"
DEFAULT_BASE_DIR = "."
DEFAULT_REPORTS_DIR = None

if CONFIG_FILE.exists():
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            config = json.load(f)
            folders = config.get("folders", {})
            DEFAULT_BASE_DIR = os.path.expanduser(
                folders.get("daily_work", ".")
            )
            DEFAULT_REPORTS_DIR = os.path.expanduser(
                folders.get("reports", None)
            )
    except Exception:
        pass

SPANISH_MONTHS = {
    1: "enero", 2: "febrero", 3: "marzo", 4: "abril",
    5: "mayo", 6: "junio", 7: "julio", 8: "agosto",
    9: "septiembre", 10: "octubre", 11: "noviembre", 12: "diciembre"
}


def parse_date(date_str):
    """Parse YYYYMMDD format to datetime object."""
    try:
        return datetime.strptime(date_str, "%Y%m%d")
    except ValueError:
        raise ValueError(f"Formato de fecha inválido: {date_str}. Use YYYYMMDD")


def format_spanish_date(date_obj):
    """Format date as 'DD de MMMM de YYYY' in Spanish."""
    return f"{date_obj.day} de {SPANISH_MONTHS[date_obj.month]} de {date_obj.year}"


def get_file_metadata(filepath):
    """Get creation and modification times for a file."""
    stat = os.stat(filepath)
    
    # Different platforms store creation time differently
    if platform.system() == 'Darwin':  # macOS
        creation_time = datetime.fromtimestamp(stat.st_birthtime)
    elif platform.system() == 'Windows':
        creation_time = datetime.fromtimestamp(stat.st_ctime)
    else:  # Linux and others
        # Linux doesn't reliably store creation time, use modification time
        creation_time = datetime.fromtimestamp(stat.st_mtime)
    
    modification_time = datetime.fromtimestamp(stat.st_mtime)
    
    return {
        'creation_time': creation_time,
        'modification_time': modification_time,
        'size': stat.st_size
    }


def extract_tasks_from_prd(prd_content):
    """Extract tasks from PRD content using hierarchical format."""
    tasks = []
    
    # Pattern: ### [emoji] N. Description — **HH:MM**
    # Matches both ✅ (completed) and ⏳ (pending)
    pattern = r'###\s+(.+?)\s+(\d+)\.\s+(.+?)\s+—\s+\*\*(\d{2}:\d{2})\*\*'
    
    matches = re.finditer(pattern, prd_content, re.DOTALL)
    for match in matches:
        emoji = match.group(1).strip()
        task_num = match.group(2)
        task_name = match.group(3).strip()
        time_str = match.group(4)
        
        # Determine status based on emoji
        if '✅' in emoji:
            status = 'completada'
        elif '⏳' in emoji:
            status = 'pendiente'
        else:
            status = 'desconocido'
        
        tasks.append({
            'number': task_num,
            'name': task_name,
            'time': time_str,
            'status': status,
            'emoji': emoji
        })
    
    return tasks


def calculate_work_hours(tasks, first_file_time):
    """Calculate total work hours based on tasks and file timestamps."""
    if not tasks:
        return 0, 0
    
    # Get times
    times = []
    for task in tasks:
        try:
            hour, minute = map(int, task['time'].split(':'))
            task_datetime = first_file_time.replace(hour=hour, minute=minute, second=0)
            times.append(task_datetime)
        except:
            continue
    
    if not times:
        return 0, 0
    
    # Calculate duration from first to last task
    if len(times) > 1:
        total_minutes = (max(times) - min(times)).total_seconds() / 60
    else:
        # If only one task, assume at least 30 minutes
        total_minutes = 30
    
    hours = int(total_minutes // 60)
    minutes = int(total_minutes % 60)
    
    return hours, minutes


def analyze_daily_folder(date_obj, base_path):
    """Analyze all files in the daily folder."""
    folder_name = date_obj.strftime("%y%m%d")
    folder_path = Path(base_path).expanduser() / folder_name
    
    if not folder_path.exists():
        return None, f"Carpeta no encontrada: {folder_path}"
    
    # Collect all files
    files = []
    for file in folder_path.iterdir():
        if file.is_file() and not file.name.startswith('.'):
            metadata = get_file_metadata(file)
            files.append({
                'name': file.name,
                'path': str(file),
                'metadata': metadata
            })
    
    if not files:
        return None, "No se encontraron archivos en la carpeta"
    
    # Sort by creation time
    files.sort(key=lambda x: x['metadata']['creation_time'])
    
    # Find PRD file
    prd_file = None
    prd_content = None
    for file in files:
        if file['name'].startswith('PRD_'):
            prd_file = file
            with open(file['path'], 'r', encoding='utf-8') as f:
                prd_content = f.read()
            break
    
    # Extract tasks if PRD exists
    tasks = []
    if prd_content:
        tasks = extract_tasks_from_prd(prd_content)
    
    # Calculate work hours
    first_file_time = files[0]['metadata']['creation_time']
    hours, minutes = calculate_work_hours(tasks, first_file_time)
    
    return {
        'folder_path': str(folder_path),
        'folder_name': folder_name,
        'files': files,
        'prd_file': prd_file,
        'tasks': tasks,
        'start_time': first_file_time,
        'total_hours': hours,
        'total_minutes': minutes,
        'completed_tasks': len([t for t in tasks if t['status'] == 'completada']),
        'pending_tasks': len([t for t in tasks if t['status'] == 'pendiente'])
    }, None


def generate_summary_report(analysis, date_obj, output_dir=None):
    """Generate a markdown summary report."""
    
    date_spanish = format_spanish_date(date_obj)
    folder_name = analysis['folder_name']
    
    # Generate report content
    report = f"""# Resumen del Día - {date_spanish}

## Información General

- **Carpeta**: `{folder_name}`
- **Hora de inicio**: {analysis['start_time'].strftime('%H:%M')} (primer archivo creado)
- **Tareas completadas**: {analysis['completed_tasks']}
- **Tareas pendientes**: {analysis['pending_tasks']}
- **Horas trabajadas**: {analysis['total_hours']}h {analysis['total_minutes']}m
- **Documentos creados**: {len(analysis['files'])}

---

## Tareas Realizadas

"""
    
    # Add completed tasks
    completed_tasks = [t for t in analysis['tasks'] if t['status'] == 'completada']
    if completed_tasks:
        for task in completed_tasks:
            report += f"### {task['emoji']} {task['number']}. {task['name']} — **{task['time']}**\n\n"
    else:
        report += "*No se registraron tareas completadas*\n\n"
    
    report += "---\n\n## Tareas Pendientes\n\n"
    
    # Add pending tasks
    pending_tasks = [t for t in analysis['tasks'] if t['status'] == 'pendiente']
    if pending_tasks:
        for task in pending_tasks:
            report += f"### {task['emoji']} {task['number']}. {task['name']} — **{task['time']}**\n\n"
    else:
        report += "*No hay tareas pendientes*\n\n"
    
    report += "---\n\n## Documentos Generados\n\n"
    
    # List all files
    for idx, file in enumerate(analysis['files'], 1):
        creation = file['metadata']['creation_time'].strftime('%H:%M:%S')
        modification = file['metadata']['modification_time'].strftime('%H:%M:%S')
        size_kb = file['metadata']['size'] / 1024
        
        report += f"{idx}. **{file['name']}**\n"
        report += f"   - Creado: {creation}\n"
        report += f"   - Modificado: {modification}\n"
        report += f"   - Tamaño: {size_kb:.2f} KB\n\n"
    
    report += f"""---

## Metadatos

- **Resumen generado**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Carpeta analizada**: `{analysis['folder_path']}`
- **Script**: `generate_day_summary.py`

---

*Este resumen fue generado automáticamente analizando todos los archivos de la carpeta del día.*
"""
    
    # Save report
    if output_dir is None:
        if DEFAULT_REPORTS_DIR:
            reports_path = Path(DEFAULT_REPORTS_DIR).expanduser()
            reports_path.mkdir(parents=True, exist_ok=True)
            output_path = reports_path / f"RESUMEN_{folder_name}.md"
        else:
            # Fallback: save in the daily work folder
            output_path = Path(analysis['folder_path']) / f"RESUMEN_{folder_name}.md"
    else:
        output_path = Path(output_dir).expanduser() / f"RESUMEN_{folder_name}.md"
        output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    return str(output_path)


def main():
    parser = argparse.ArgumentParser(
        description="Generar resumen del día analizando carpeta diaria",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  python generate_day_summary.py                    # Resumen de hoy
  python generate_day_summary.py --date 20260225   # Resumen de fecha específica
  python generate_day_summary.py --output ./custom  # Guardar en carpeta custom
        """
    )
    parser.add_argument('--date', help='Fecha en formato YYYYMMDD (default: hoy)')
    parser.add_argument('--path', default=None, help=f'Ruta base DAILY_WORK (default: {DEFAULT_BASE_DIR})')
    parser.add_argument('--output', default=None, help='Carpeta de salida para reporte (default: carpeta REPORTS)')
    
    args = parser.parse_args()
    
    # Determine date
    if args.date:
        date_obj = parse_date(args.date)
    else:
        date_obj = datetime.now()
    
    base_path = args.path if args.path else DEFAULT_BASE_DIR
    
    # Analyze folder
    print(f"📁 Analizando carpeta del día {format_spanish_date(date_obj)}...")
    analysis, error = analyze_daily_folder(date_obj, base_path)
    
    if error:
        print(f"❌ Error: {error}")
        return 1
    
    # Generate report
    print(f"📝 Generando resumen...")
    report_path = generate_summary_report(analysis, date_obj, args.output)
    
    print(f"✅ Resumen generado exitosamente: {report_path}")
    print(f"\n📊 Estadísticas:")
    print(f"   - Tareas completadas: {analysis['completed_tasks']}")
    print(f"   - Tareas pendientes: {analysis['pending_tasks']}")
    print(f"   - Horas trabajadas: {analysis['total_hours']}h {analysis['total_minutes']}m")
    print(f"   - Documentos: {len(analysis['files'])}")
    
    return 0


if __name__ == "__main__":
    exit(main())
