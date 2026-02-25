#!/usr/bin/env python3
"""
Create Daily PRD Script
Genera automáticamente un nuevo PRD diario con nombre y estructura correctos.

Uso:
    python create_daily_prd.py [--date YYYYMMDD] [--path ./path/to/folder]

Ejemplos:
    python create_daily_prd.py                          # Crea PRD para hoy
    python create_daily_prd.py --date 20260217         # Crea PRD para fecha específica
    python create_daily_prd.py --path ./PRD             # Crea en carpeta específica
"""

import argparse
import os
import json
from datetime import datetime, timedelta
from pathlib import Path

# Load configuration
CONFIG_FILE = Path(__file__).parent.parent / "config.json"
DEFAULT_BASE_DIR = "."
USE_DAILY_FOLDERS = True
PRD_DOCUMENTS_DIR = "~/Documents/prd_diarios/PRD_DOCUMENTS"

if CONFIG_FILE.exists():
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            config = json.load(f)
            # Try to get PRD documents directory from folders config
            prd_docs = config.get("folders", {}).get("prd_documents")
            if prd_docs:
                PRD_DOCUMENTS_DIR = os.path.expanduser(prd_docs)
            # Fallback to old config format
            if not prd_docs:
                DEFAULT_BASE_DIR = os.path.expanduser(
                    config.get("prd_base_directory", ".")
                )
                PRD_DOCUMENTS_DIR = DEFAULT_BASE_DIR
            USE_DAILY_FOLDERS = config.get("features", {}).get("use_daily_folders", True)
    except Exception:
        PRD_DOCUMENTS_DIR = DEFAULT_BASE_DIR

TEMPLATE = """# PRD - {date_spanish}

## Resumen Ejecutivo

- **Fecha**: {date_spanish}
- **Tareas completadas**: 0
- **Tareas pendientes**: 0
- **Total de horas**: 0h 0m

---

## Tareas Realizadas

*No hay tareas registradas aún*

---

## Tareas Pendientes

*Ninguna por el momento*

---

## Notas Adicionales

- Documento creado para seguimiento de tareas diarias
- Se actualizará conforme se realicen actividades
- Creado automáticamente el {timestamp}
"""

SPANISH_MONTHS = {
    1: "enero",
    2: "febrero",
    3: "marzo",
    4: "abril",
    5: "mayo",
    6: "junio",
    7: "julio",
    8: "agosto",
    9: "septiembre",
    10: "octubre",
    11: "noviembre",
    12: "diciembre"
}


def parse_date(date_str):
    """Parse YYYYMMDD format to datetime object."""
    try:
        return datetime.strptime(date_str, "%Y%m%d")
    except ValueError:
        raise ValueError(f"Formato de fecha inválido: {date_str}. Use YYYYMMDD")


def format_spanish_date(date_obj):
    """Format date as 'DD de MMMM de YYYY' in Spanish."""
    day = date_obj.day
    month = SPANISH_MONTHS[date_obj.month]
    year = date_obj.year
    return f"{day} de {month} de {year}"


def create_prd(date_str=None, path=None):
    """
    Create a new daily PRD file in PRD_DOCUMENTS directory.
    
    Args:
        date_str: Date in YYYYMMDD format. If None, uses today's date.
        path: Directory where PRD should be created. If None, uses config default.
    
    Returns:
        tuple: (filename, filepath, success: bool, message: str)
    """
    if path is None:
        path = PRD_DOCUMENTS_DIR
    
    # Determine date
    if date_str is None:
        date_obj = datetime.now()
    else:
        date_obj = parse_date(date_str)
    
    # Create output directory
    output_dir = Path(path).expanduser()
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate filename
    date_formatted = date_obj.strftime("%Y%m%d")
    filename = f"PRD_{date_formatted}.md"
    filepath = output_dir / filename
    
    # Check if file already exists
    if filepath.exists():
        return filename, str(filepath), False, "Archivo ya existe"
    
    # Generate content
    date_spanish = format_spanish_date(date_obj)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    content = TEMPLATE.format(date_spanish=date_spanish, timestamp=timestamp)
    
    # Write file
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return filename, str(filepath), True, "Creado exitosamente"
    except Exception as e:
        return filename, str(filepath), False, str(e)


def main():
    parser = argparse.ArgumentParser(
        description="Crear un nuevo PRD diario en carpeta PRD_DOCUMENTS",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  python create_daily_prd.py                    # Crea PRD para hoy
  python create_daily_prd.py --date 20260217   # Crea para fecha específica
  python create_daily_prd.py --path ./Custom   # Especifica carpeta custom
        """
    )
    parser.add_argument('--date', help='Fecha en formato YYYYMMDD (default: hoy)')
    parser.add_argument('--path', default=None, help=f'Ruta (default: {PRD_DOCUMENTS_DIR})')
    
    args = parser.parse_args()
    
    filename, filepath, success, message = create_prd(args.date, args.path)
    
    if success:
        print(f"✅ {message}: {filepath}")
        return 0
    else:
        print(f"❌ Error: {message}")
        print(f"   Archivo: {filepath}")
        return 1


if __name__ == "__main__":
    exit(main())
