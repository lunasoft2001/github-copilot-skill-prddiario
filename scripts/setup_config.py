#!/usr/bin/env python3
"""
PRD Diario - Setup Configuration Wizard
Script interactivo para configurar rutas de PRD diarios, trabajo diario y otros componentes.

Primera ejecución: Crea archivo config.json con las preferencias del usuario.
Ejecuciones posteriores: Carga la configuración existente.

Uso:
    python setup_config.py              # Ejecuta wizard interactivo
    python setup_config.py --reset      # Resetea configuración
    python setup_config.py --show       # Muestra configuración actual
"""

import argparse
import json
import os
from pathlib import Path
from datetime import datetime

CONFIG_FILE = Path(__file__).parent.parent / "config.json"


def tint(color, text):
    """Simple ANSI color codes for terminal output."""
    colors = {
        'reset': '\033[0m',
        'bold': '\033[1m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'cyan': '\033[96m',
    }
    return f"{colors.get(color, '')}{text}{colors['reset']}"


def get_valid_path(prompt, default=None, allow_home=True):
    """Get and validate a directory path from user input."""
    while True:
        if default:
            display_default = default.replace(os.path.expanduser("~"), "~")
            user_input = input(f"{prompt} [{display_default}]: ").strip()
            if not user_input:
                path = default
            else:
                path = user_input
        else:
            path = input(f"{prompt}: ").strip()
        
        if not path:
            print(tint('yellow', "⚠️  Ruta no puede estar vacía"))
            continue
        
        # Expand ~ to home directory
        if allow_home and path.startswith("~"):
            path = os.path.expanduser(path)
        
        # Create directory structure preview
        path_obj = Path(path)
        print(tint('cyan', f"   📁 {path_obj.expanduser()}"))
        
        confirm = input(tint('blue', "   ¿Es correcta esta ruta? (s/n): ")).strip().lower()
        if confirm == 's':
            # Ensure path exists or can be created
            path_obj.mkdir(parents=True, exist_ok=True)
            return path if "~" in path else str(path_obj.absolute())
        else:
            print()


def run_wizard():
    """Interactive configuration wizard."""
    print(tint('bold', "\n" + "="*60))
    print(tint('bold', "  PRD Diario - Asistente de Configuración Inicial"))
    print(tint('bold', "="*60 + "\n"))
    
    config = {
        "version": "1.0.0",
        "created": datetime.now().isoformat(),
        "last_updated": datetime.now().isoformat(),
        "description": "Configuración de PRD Diario con carpetas separadas",
        "folders": {},
        "features": {},
        "notes": "Personaliza estas rutas según tu flujo de trabajo"
    }
    
    print(tint('bold', "📂 CONFIGURACIÓN DE CARPETAS\n"))
    
    # PRD Documents Directory
    print(tint('cyan', "1️⃣  Carpeta de Documentos PRD"))
    print("   Donde se guardarán los PRD_YYYYMMDD.md")
    print("   (Ej: ~/Documents/prd_diarios/PRD_DOCUMENTS)\n")
    
    prd_docs = get_valid_path(
        "   Ruta para documentos PRD",
        default="~/Documents/prd_diarios/PRD_DOCUMENTS"
    )
    config["folders"]["prd_documents"] = prd_docs
    print(tint('green', "   ✅ Configurado\n"))
    
    # Daily Work Directory
    print(tint('cyan', "2️⃣  Carpeta de Trabajo Diario"))
    print("   Donde se organizarán las carpetas YYMMDD por día")
    print("   (Ej: ~/Documents/prd_diarios/DAILY_WORK)\n")
    
    daily_work = get_valid_path(
        "   Ruta para trabajo diario",
        default="~/Documents/prd_diarios/DAILY_WORK"
    )
    config["folders"]["daily_work"] = daily_work
    print(tint('green', "   ✅ Configurado\n"))
    
    # Reports Directory
    print(tint('cyan', "3️⃣  Carpeta de Reportes (opcional)"))
    print("   Donde se guardarán reportes, resúmenes finales, etc.")
    print("   (Ej: ~/Documents/prd_diarios/REPORTS)\n")
    
    reports = get_valid_path(
        "   Ruta para reportes",
        default="~/Documents/prd_diarios/REPORTS"
    )
    config["folders"]["reports"] = reports
    print(tint('green', "   ✅ Configurado\n"))
    
    # Archives Directory
    print(tint('cyan', "4️⃣  Carpeta de Archivos Completados (opcional)"))
    print("   Donde archivar días completados")
    print("   (Ej: ~/Documents/prd_diarios/ARCHIVES)\n")
    
    archives = get_valid_path(
        "   Ruta para archivos completados",
        default="~/Documents/prd_diarios/ARCHIVES"
    )
    config["folders"]["archives"] = archives
    print(tint('green', "   ✅ Configurado\n"))
    
    # Features Configuration
    print(tint('bold', "\n⚙️  CONFIGURACIÓN DE FEATURES\n"))
    
    print(tint('cyan', "Características disponibles:\n"))
    
    use_daily_folders = input(
        "¿Usar organización con carpetas diarias YYMMDD? (s/n) [s]: "
    ).strip().lower() != 'n'
    config["features"]["use_daily_folders"] = use_daily_folders
    print()
    
    auto_summary = input(
        "¿Generar resumen automático del día? (s/n) [s]: "
    ).strip().lower() != 'n'
    config["features"]["auto_summary"] = auto_summary
    print()
    
    track_metadata = input(
        "¿Rastrear metadatos de archivos? (s/n) [s]: "
    ).strip().lower() != 'n'
    config["features"]["track_file_metadata"] = track_metadata
    print()
    
    # Display summary
    print(tint('bold', "\n" + "="*60))
    print(tint('bold', "  📋 RESUMEN DE CONFIGURACIÓN"))
    print(tint('bold', "="*60 + "\n"))
    
    print(tint('cyan', "📂 CARPETAS:\n"))
    for folder_name, folder_path in config["folders"].items():
        display_path = folder_path.replace(os.path.expanduser("~"), "~")
        print(f"   • {folder_name.upper()}")
        print(f"     → {display_path}\n")
    
    print(tint('cyan', "⚙️  FEATURES:\n"))
    for feature_name, enabled in config["features"].items():
        status = tint('green', "✅ Habilitado") if enabled else tint('yellow', "⏸️  Deshabilitado")
        print(f"   • {feature_name}: {status}")
    print()
    
    # Final confirmation
    confirm = input(
        tint('blue', "¿Guardar esta configuración? (s/n): ")
    ).strip().lower()
    
    if confirm == 's':
        try:
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            print(tint('green', f"\n✅ Configuración guardada en: {CONFIG_FILE}\n"))
            return True
        except Exception as e:
            print(tint('yellow', f"\n❌ Error guardando configuración: {e}\n"))
            return False
    else:
        print(tint('yellow', "\n⏸️  Configuración cancelada. No se guardaron cambios.\n"))
        return False


def show_current_config():
    """Display current configuration."""
    if not CONFIG_FILE.exists():
        print(tint('yellow', "⚠️  No hay configuración guardada.\n"))
        print("Ejecuta: python setup_config.py")
        print("Para crear la configuración inicial.\n")
        return
    
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    print(tint('bold', "\n" + "="*60))
    print(tint('bold', "  📋 CONFIGURACIÓN ACTUAL"))
    print(tint('bold', "="*60 + "\n"))
    
    print(tint('cyan', f"Creada: {config.get('created', 'N/A')}\n"))
    
    print(tint('cyan', "📂 CARPETAS:\n"))
    for folder_name, folder_path in config["folders"].items():
        display_path = folder_path.replace(os.path.expanduser("~"), "~")
        exists = "✅" if Path(folder_path).exists() else "❌"
        print(f"   {exists} {folder_name.upper()}")
        print(f"      → {display_path}\n")
    
    print(tint('cyan', "⚙️  FEATURES:\n"))
    for feature_name, enabled in config["features"].items():
        status = tint('green', "✅ Habilitado") if enabled else tint('yellow', "⏸️  Deshabilitado")
        print(f"   • {feature_name}: {status}")
    print()


def reset_config():
    """Reset configuration."""
    if CONFIG_FILE.exists():
        confirm = input(
            tint('yellow', "⚠️  ¿Estás seguro de que quieres resetear la configuración? (s/n): ")
        ).strip().lower()
        
        if confirm == 's':
            CONFIG_FILE.unlink()
            print(tint('green', "✅ Configuración eliminada.\n"))
            run_wizard()
        else:
            print(tint('yellow', "⏸️  Reset cancelado.\n"))
    else:
        print(tint('yellow', "⚠️  No hay configuración para resetear.\n"))


def main():
    parser = argparse.ArgumentParser(
        description="Configurar rutas de PRD Diario",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  python setup_config.py              # Executar wizard interactivo
  python setup_config.py --show       # Mostrar configuración actual
  python setup_config.py --reset      # Resetear configuración
        """
    )
    parser.add_argument('--reset', action='store_true', help='Resetear configuración')
    parser.add_argument('--show', action='store_true', help='Mostrar configuración actual')
    
    args = parser.parse_args()
    
    if args.reset:
        reset_config()
    elif args.show:
        show_current_config()
    else:
        # Check if config exists
        if CONFIG_FILE.exists():
            print(tint('cyan', "ℹ️  Ya existe una configuración guardada.\n"))
            show = input("¿Quieres (v)er la actual o (a)ctualizar? (v/a): ").strip().lower()
            if show == 'v':
                show_current_config()
            elif show == 'a':
                run_wizard()
        else:
            run_wizard()


if __name__ == "__main__":
    main()
