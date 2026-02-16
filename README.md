# PRD Diario - GitHub Copilot Skill

Skill para GitHub Copilot que gestiona tareas diarias creando PRDs estructurados con formato jerárquico legible. Incluye generación automática de reportes de horas y dashboard visual HTML interactivo.

## 🎯 Características

✅ **Formato jerárquico legible** - Estructura clara con encabezados H3 y emojis  
✅ **Timestamps precisos** - Registra hora exacta de cada tarea  
✅ **Documentación completa** - Descripción + Solución para auditoría  
✅ **Reportes automáticos de horas** - Scripts Python/PowerShell generan reportes diarios  
✅ **Dashboard visual HTML** - Dashboard interactivo con gráficos y tema light/dark  
✅ **Gestión de pendientes** - Seguimiento de tareas incompletas  
✅ **Git-friendly** - Markdown puro, fácil de versionear  
✅ **Scripts reutilizables** - Python y PowerShell para toda la automatización  

## 📦 Contenido

```
prd-diario/
├── SKILL.md                            # Documentación principal (5 fases)
├── config.json                         # Configuración centralizada
├── scripts/
│   ├── create_daily_prd.py            # Crea nuevo PRD_YYYYMMDD.md
│   ├── create_daily_prd.ps1           # Versión PowerShell
│   ├── generate_hours_report.py       # Genera HORAS_PRD_YYYYMMDD.md
│   ├── generate_hours_report.ps1      # Versión PowerShell
│   ├── generate_dashboard.py          # Genera PRD_YYYYMMDD_DASHBOARD.html
│   └── generate_dashboard.ps1         # Versión PowerShell
├── references/
│   └── structure.md                   # Documentación detallada
└── assets/
    └── template.md                    # Plantilla base
```

## 🚀 Instalación

### Opción 1: Instalación Automática

1. Clonar el repositorio:
```bash
git clone https://github.com/lunasoft2001/github-copilot-skill-prddiario.git
cd github-copilot-skill-prddiario
```

2. Copiar a la carpeta de skills de Copilot:

**Windows:**
```powershell
Copy-Item -Recurse . "$env:USERPROFILE\.copilot\skills\prd-diario" -Force
```

**macOS/Linux:**
```bash
cp -r . ~/.copilot/skills/prd-diario
```

### Opción 2: Manual

Copiar la carpeta `github-copilot-skill-prddiario` a:
- **Windows**: `%USERPROFILE%\.copilot\skills\prd-diario`
- **macOS/Linux**: `~/.copilot/skills/prd-diario`

## 📝 Uso

### Con Claude/GitHub Copilot

Simplemente pide lo que necesites:

```
"Crear PRD de hoy"
"Completé: Revisar tareas en Trello, tomó 15 minutos, a las 09:00"
"Tenemos tarea pendiente: Revisar servidor Proxmox"
"Genera el reporte de horas de hoy"
```

### ⚙️ Configuración

El skill incluye un archivo `config.json` que define la carpeta de salida por defecto:

```json
{
  "prd_output_directory": "~/Documents/prd_diarios"
}
```

**Cómo funciona:**
- Los scripts leen automáticamente `config.json` al inicio
- Los archivos se guardan en `~/Documents/prd_diarios/` por defecto
- Puedes sobrescribir la configuración con argumentos `--path` o `--output`
- Totalmente backward compatible

**Cambiar la carpeta por defecto:**
Edita `config.json` y cambia la ruta deseada. Por ejemplo:
```json
{
  "prd_output_directory": "~/Dropbox/PRDs"
}
```

### Scripts Directos

#### Crear PRD Nuevo

**Python:**
```bash
python scripts/create_daily_prd.py
# → Crea: ~/Documents/prd_diarios/PRD_260216.md

# Con fecha específica:
python scripts/create_daily_prd.py --date 20260217
# → Crea: ~/Documents/prd_diarios/PRD_260217.md
```

**PowerShell:**
```powershell
.\scripts\create_daily_prd.ps1
.\scripts\create_daily_prd.ps1 -Date "2026-02-16"
.\scripts\create_daily_prd.ps1 -Output "./mi_carpeta"
```

#### Generar Reporte de Horas


**Python:**
```bash
python scripts/generate_hours_report.py PRD_260216.md
# → Crea: ~/Documents/prd_diarios/HORAS_PRD_260216.md

# Sobrescribir carpeta de salida:
python scripts/generate_hours_report.py PRD_260216.md --output ./reportes
# → Crea: ./reportes/HORAS_PRD_260216.md
```

**PowerShell:**
```powershell
.\scripts\generate_hours_report.ps1 -PRDFile "PRD_260216.md" [-Output "./reports"]
```

Genera automáticamente `HORAS_PRD_YYYYMMDD.md` con:
- Desglose de horas por tarea
- Duración de cada tarea
- Total de horas trabajadas
- Promedio por tarea

#### Generar Dashboard Visual HTML

**Python:**
```bash
python scripts/generate_dashboard.py PRD_260216.md
# → Crea: ~/Documents/prd_diarios/PRD_260216_DASHBOARD.html

# Sobrescribir carpeta de salida:
python scripts/generate_dashboard.py PRD_260216.md --output ./dashboards
# → Crea: ./dashboards/PRD_260216_DASHBOARD.html
```

**PowerShell:**
```powershell
.\scripts\generate_dashboard.ps1 -PRDFile "PRD_260216.md" [-Output "./dashboards"]
```

Genera automáticamente `PRD_YYYYMMDD_DASHBOARD.html` con:
- Estadísticas en tiempo real (tareas, horas, progreso)
- Barra de progreso visual
- Cards por cada tarea completada/pendiente
- Toggle theme light/dark
- Diseño responsive (funciona en móvil)
- Archivo HTML standalone (sin dependencias externas)
- Abre directamente en navegador

### Formato Jerárquico (Nuevo)

```markdown
# PRD - 16 de febrero de 2026

## Resumen Ejecutivo

- **Fecha**: 16 de febrero de 2026
- **Tareas completadas**: 5
- **Tareas pendientes**: 1
- **Total de horas**: 4h 20m

---

## Tareas Realizadas

### ✅ 1. Revisar tareas en Trello — **09:00**

**Descripción**  
Morning standup: Revisión de tareas pendientes del sprint. Se identificaron 12 tareas en el backlog y 3 en progreso.

**Solución**  
Se revisaron prioridades con el equipo. Se replanificó una tarea de baja prioridad. Se inició trabajo en tarea crítica.

### ✅ 2. Solucionar bug en formulario — **11:15**

**Descripción**  
Usuario reportó error en validación de email. La validación rechazaba emails válidos con subdominios.

**Solución**  
Se identificó regex incorrecto. Se actualizó patrón a RFC 5322. Se testeó con 50 casos. Desplegado en producción.

---

## Tareas Pendientes

### ⏳ 1. Apagado controlado Proxmox — **16:00**

**Descripción**  
Servidor principal funcionando lentamente. Requiere shutdown ordenado y análisis.

**Estado**  
En curso
```

Ver [references/structure.md](references/structure.md) para documentación completa.

## 📊 Ejemplo de Reporte de Horas

Cuando ejecutas `generate_hours_report.py` en un PRD:

```markdown
# Reporte de Horas — 16 de Febrero de 2026

## Resumen

- **Tareas**: 8
- **Horas totales**: 4h 20m (4.33h)

---

## Desglose por Tarea

### 1. Revisar tareas asignadas en Trello
- **Hora inicio**: 09:00
- **Duración**: 15m

### 2. Solucionar problema en Access
- **Hora inicio**: 09:15
- **Duración**: 30m

[... más tareas ...]

---

## Totales

**Horas trabajadas**: 4h 20m
**Promedio por tarea**: 32 minutos
**Generado**: 2026-02-16 14:35:22
```

## 🔗 Integración con Otros Skills

Este skill puede trabajar junto con:
- **Skill PRD** - Para análisis profesionales complejos incorporados en PRDs diarios
- **Git Commit** - Para versionear PRDs diarios automáticamente

## 🛠️ Mejor Práctica

1. **Crea PRD cada mañana** - Usa uno de los scripts o pide a Claude
2. **Registra tareas completadas** - Con descripción, solución y hora exacta
3. **Documenta bien** - Explica QUÉ se hizo, POR QUÉ y RESULTADO obtenido
4. **Marca pendientes** - Al final del día, lista lo incompleto
5. **Genera reporte de horas** - Al cierre del día, corre el script de horas
6. **Visualiza en dashboard** - Abre el HTML en navegador para ver progreso visual
7. **Revisa completitud** - Antes de terminar, valida toda la información

## 📖 Documentación

- [SKILL.md](SKILL.md) - Documentación principal del skill (5 fases de trabajo)
- [references/structure.md](references/structure.md) - Detalles técnicos y mejores prácticas
- [assets/template.md](assets/template.md) - Plantilla lista para usar

## 📝 Historial de Cambios

### v1.2 (2026-02-16)
- ✅ Dashboard HTML visual e interactivo (Python + PowerShell)
- ✅ Estadísticas en tiempo real con gráficos
- ✅ Theme toggle (light/dark mode con localStorage)
- ✅ Diseño responsive para móvil
- ✅ Fase 5: Visualización en dashboard

### v1.1 (2026-02-16)
- ✅ Nuevo formato jerárquico (### ✅ N. Task — **HH:MM**)
- ✅ Scripts de generación de reportes de horas (Python + PowerShell)
- ✅ Documentación actualizada con ejemplos nuevos
- ✅ Fase 4: Reportes automáticos de horas

### v1.0 (2026-02-16)
- Versión inicial con creación de PRDs
- Scripts Python y PowerShell
- Fase 1-3: Crear, registrar tareas, gestionar pendientes

## 📄 Licencia

MIT License - Libre para usar y modificar
