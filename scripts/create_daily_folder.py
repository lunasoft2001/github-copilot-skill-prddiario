#!/usr/bin/env python3
"""
Create Daily Folder Script
Crea una carpeta diaria con formato YYMMDD para organizar todos los documentos del día.

Uso:
    python create_daily_folder.py [--date YYYYMMDD] [--path ./path/to/base]

Ejemplos:
    python create_daily_folder.py                          # Crea carpeta para hoy
    python create_daily_folder.py --date 20260225         # Crea carpeta para fecha específica
    python create_daily_folder.py --path ./PRD             # Crea en carpeta base específica
"""

import argparse
import os
import json
from datetime import datetime
from pathlib import Path

# Load configuration
CONFIG_FILE = Path(__file__).parent.parent / "config.json"
DEFAULT_DAILY_WORK_DIR = "~/Documents/prd_diarios/DAILY_WORK"

if CONFIG_FILE.exists():
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            config = json.load(f)
            DEFAULT_DAILY_WORK_DIR = os.path.expanduser(
                config.get("folders", {}).get("daily_work", DEFAULT_DAILY_WORK_DIR)
            )
    except Exception:
        pass


def parse_date(date_str):
    """Parse YYYYMMDD format to datetime object."""
    try:
        return datetime.strptime(date_str, "%Y%m%d")
    except ValueError:
        raise ValueError(f"Formato de fecha inválido: {date_str}. Use YYYYMMDD")


def create_daily_folder(date_str=None, base_path=None):
    """
    Create a daily folder with format YYMMDD in DAILY_WORK directory.
    
    Args:
        date_str: Date in YYYYMMDD format. If None, uses today's date.
        base_path: Base directory where folder should be created. If None, uses config default.
    
    Returns:
        tuple: (folder_name, folder_path, success: bool, message: str)
    """
    if base_path is None:
        base_path = DEFAULT_DAILY_WORK_DIR
    
    # Determine date
    if date_str is None:
        date_obj = datetime.now()
    else:
        date_obj = parse_date(date_str)
    
    # Create base directory if it doesn't exist
    base_dir = Path(base_path).expanduser()
    base_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate folder name (YYMMDD format)
    folder_name = date_obj.strftime("%y%m%d")
    folder_path = base_dir / folder_name
    
    # Check if folder already exists
    if folder_path.exists():
        return folder_name, str(folder_path), True, "Carpeta ya existe"
    
    # Create folder
    try:
        folder_path.mkdir(parents=True, exist_ok=True)
        
        # Create a README.md inside with the date
        readme_path = folder_path / "README.md"
        readme_content = f"""# Trabajo del Día - {date_obj.strftime('%d/%m/%Y')}

Esta carpeta contiene todos los documentos del trabajo realizado durante el día.

## Estructura

- **PRD**: Documento de tareas realizadas (guardado en carpeta PRD_DOCUMENTS)
- **Conversaciones**: Logs de conversaciones importantes
- **Notas**: Apuntes y decisiones del día
- **Documentos**: Archivos relevantes generados

## Referencia

- PRD: `PRD_DOCUMENTS/PRD_{date_obj.strftime('%Y%m%d')}.md`
- Resumen: `REPORTS/RESUMEN_{folder_name}.md`

---

*Carpeta creada automáticamente por script create_daily_folder.py*
*Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        return folder_name, str(folder_path), True, "Carpeta creada exitosamente"
    except Exception as e:
        return folder_name, str(folder_path), False, str(e)


def main():
    parser = argparse.ArgumentParser(
        description="Crear una carpeta diaria con formato YYMMDD en DAILY_WORK",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  python create_daily_folder.py                    # Crea carpeta para hoy
  python create_daily_folder.py --date 20260225   # Crea para fecha específica
  python create_daily_folder.py --path ./Custom   # Especifica carpeta custom
        """
    )
    parser.add_argument('--date', help='Fecha en formato YYYYMMDD (default: hoy)')
    parser.add_argument('--path', default=None, help=f'Ruta base (default: {DEFAULT_DAILY_WORK_DIR})')
    
    args = parser.parse_args()
    
    folder_name, folder_path, success, message = create_daily_folder(args.date, args.path)
    
    if success:
        print(f"✅ {message}: {folder_path}")
        return 0
    else:
        print(f"❌ Error: {message}")
        print(f"   Carpeta: {folder_path}")
        return 1


if __name__ == "__main__":
    exit(main())
