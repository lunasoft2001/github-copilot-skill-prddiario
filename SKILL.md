---
name: prddiario
description: 'Gestiona tareas diarias con formato jerárquico legible, documentación completa (descripción + solución) con timestamps, y genera reportes automáticos de horas trabajadas. Usa cuando necesites crear PRD diario, registrar tareas completadas, gestionar pendientes, o generar reportes de horas. Incluye scripts Python/PowerShell para automatizar todo.'
license: MIT
---

# PRD Diario - Gestor de Tareas Diarias

## Descripción General

Automatiza la creación y organización de Documentos de Requisitos de Productos (PRD) diarios para un seguimiento estructurado de tareas. Organiza todo en carpetas diarias con formato YYMMDD. Ideal para:

- **Organización por carpetas diarias** (formato YYMMDD: 260225, 260226, etc.)
- **Registro de tareas** con timestamps exactos y documentación completa
- **Gestión unificada** de PRD, conversaciones y documentos del día
- **Resúmenes automáticos** que analizan metadatos de archivos
- **Rastreo de inicio de jornada** usando fecha de creación de documentos
- **Reportes de horas trabajadas** y auditoría completa
- **Seguimiento de tareas pendientes** para el día siguiente

## Cuándo Usar Este Skill

Use este skill cuando:

- Necesite **iniciar el día** y crear la carpeta + PRD diario
- Quiera **registrar tareas** completadas con hora exacta  
- Deba **documentar soluciones** de manera estructurada
- Tenga **tareas pendientes** que requieran seguimiento
- Necesite **guardar conversaciones** o documentos del día en un solo lugar
- Quiera **generar resumen del día** automático con metadatos
- Necesite **reportes de horas** trabajadas al final del día
- Desee saber **cuándo empezó el día** (primer documento creado)
- El usuario pida "crear PRD diario", "iniciar día", "registrar tarea", "resumen del día" o "generar reporte de horas"

## Flujo de Trabajo

### Fase 0: Inicio del Día (NUEVO)

Cuando empiece el día de trabajo:

1. **Crear carpeta diaria**: Crea automáticamente carpeta con formato YYMMDD
2. **Crear PRD**: Genera PRD_YYYYMMDD.md dentro de la carpeta
3. **Listo para trabajar**: La carpeta está lista para recibir todos los documentos del día

**Estructura creada:**
```
~/Documents/prd_diarios/
  └── 260225/                    # Carpeta del día (YYMMDD)
      ├── README.md              # Info de la carpeta
      └── PRD_20260225.md        # PRD del día
```

### Fase 1: Durante el Día

Mientras trabajas:

1. **Registrar tareas**: Añade tareas completadas con timestamps
2. **Guardar documentos**: Guarda conversaciones, notas, archivos en la carpeta del día
3. **Actualizar PRD**: Documenta descripción + solución de cada tarea

**Ejemplo de estructura durante el día:**
```
260225/
  ├── README.md
  ├── PRD_20260225.md
  ├── conversacion_cliente_proyecto_X.md
  ├── notas_meeting_equipo.md
  └── diagrama_arquitectura.png
```

### Fase 2: Fin del Día

Al terminar la jornada:

1. **Generar resumen del día**: Ejecuta `generate_day_summary.py`
2. **Analiza metadatos**: Lee fechas de creación de todos los archivos
3. **Calcula horas**: Determina inicio (primer archivo) y tareas realizadas
4. **Crea reporte**: Genera RESUMEN_YYMMDD.md con toda la información

**Estructura final:**
```
260225/
  ├── README.md
  ├── PRD_20260225.md
  ├── conversacion_cliente_proyecto_X.md
  ├── notas_meeting_equipo.md
  ├── diagrama_arquitectura.png
  ├── RESUMEN_260225.md          # ← Generado automáticamente
  └── HORAS_PRD_20260225.md      # ← Opcional: reporte de horas detallado
```

### Fase 3 (Antigua): Registrar Tareas Realizadas

Para cada tarea completada:

```markdown
### ✅ N. Nombre de la Tarea — **HH:MM**

**Descripción**  
Contexto y motivo de la tarea. Qué problema se resolvía, de dónde venía la solicitud.

**Solución**  
Qué se hizo y cómo se resolvió. Pasos tomados, tecnologías usadas, resultado final.
```

**Ejemplo:**

```markdown
### ✅ 1. Revisar tareas asignadas en Trello — **09:00**

**Descripción**  
Morning standup: Revisión de tareas pendientes del sprint. Se identificaron 12 tareas en el backlog y 3 en progreso.

**Solución**  
Se revisaron prioridades con el equipo. Se replanificó una tarea de baja prioridad. Se inició trabajo en tarea crítica de cliente.
```

### Fase 3: Gestionar Tareas Pendientes

Para tareas incompletas:

```markdown
### ⏳ X. Nombre de Tarea Pendiente — **HH:MM**

**Descripción**  
Contexto de la tarea pendiente...

**Estado**  
En curso / Bloqueado / En espera
```

### Fase 4: Generar Reportes de Horas

Al final del día, para generar un reporte automático:

**Python:**
```bash
python scripts/generate_hours_report.py PRD_260216.md
```

**PowerShell:**
```powershell
.\scripts\generate_hours_report.ps1 -PRDFile "PRD_260216.md"
```

Genera automáticamente `HORAS_PRD_260216.md` con:
- Desglose por tarea con duración
- Horas totales trabajadas
- Promedio por tarea
- Timestamp de generación

## Resumen Ejecutivo

- **Fecha**: DD de MMMM de YYYY
- **Tareas completadas**: N
- **Tareas pendientes**: M
- **Total de horas**: Xh YYm

## Tareas Realizadas

### ✅ 1. Primera Tarea — **09:00**

**Descripción**  
...

**Solución**  
...

### ✅ 2. Segunda Tarea — **10:30**

**Descripción**  
...

**Solución**  
...

## Tareas Pendientes

### ⏳ 1. Tarea Pendiente — **16:00**

**Descripción**  
...

**Estado**  
En curso

## Notas Adicionales

- Observaciones importantes
```

## Patrón de Uso - Paso a Paso

### Iniciar el Día (NUEVO)

```
Usuario: "Vamos a iniciar el día" o "Crear PRD de hoy"
Claude:
1. Obtiene fecha actual (ej: 25 de febrero de 2026)
2. Crea carpeta 260225 si no existe
3. Crea PRD_20260225.md dentro de la carpeta
4. La carpeta queda lista para recibir documentos del día
```

**Ejemplo de comando:**
```bash
python scripts/create_daily_prd.py
```

### Guardar Documentos Durante el Día (NUEVO)

```
Usuario: "Guarda esta conversación en el día de hoy"
Claude:
1. Identifica la carpeta del día (ej: 260225)
2. Guarda el archivo dentro de esa carpeta
3. El archivo queda organizado junto al PRD
```

**Estructura generada:**
```
260225/
  ├── PRD_20260225.md
  ├── conversacion_proyecto_X.md  ← Nuevo
  └── README.md
```

### Crear PRD Nuevo (Método Original)

```
Usuario: "Vamos a crear el PRD de hoy"
Claude:
1. Obtiene fecha actual (ej: 16 de febrero de 2026)
2. Si use_daily_folders=true, crea carpeta 260216
3. Crea PRD_20260216.md dentro de la carpeta (o en ruta especificada)
4. Abre el archivo para edición
```

### Registrar Tarea Completada

```
Usuario: "Completé: Revisar correos. Tomó 45 minutos. Fueron 23 correos nuevos, respondí prioritarios."
Claude:
1. Obtiene hora actual: 10:30
2. Calcula número: siguiente número disponible
3. Agrega sección con formato jerárquico:
   ### ✅ N. Revisar correos — **10:30**
   **Descripción**  
   Revisión diaria de correos...
   **Solución**  
   Se procesaron 23 correos nuevos...
4. Actualiza PRD en archivo
```

### Generar Reporte de Horas

```
Usuario: "Genera el reporte de horas de hoy"
Claude:
1. Ejecuta: python scripts/generate_hours_report.py PRD_260216.md
2. Lee todas las tareas y timestamps del PRD
3. Calcula duración entre tareas
4. Genera HORAS_PRD_260216.md con totales
5. Confirma generación exitosa
```

### Generar Resumen del Día (NUEVO)

```
Usuario: "Dame un resumen del día" o "Genera resumen del día"
Claude:
1. Ejecuta: python scripts/generate_day_summary.py
2. Analiza carpeta del día (ej: 260225)
3. Lee metadatos de TODOS los archivos (fechas creación/modificación)
4. Determina hora de inicio (primer archivo creado)
5. Extrae tareas del PRD (completadas y pendientes)
6. Calcula horas trabajadas
7. Genera RESUMEN_260225.md con:
   - Información general (inicio, tareas, horas, documentos)
   - Tareas realizadas (con timestamps)
   - Tareas pendientes
   - Lista de todos los documentos con metadatos
8. Confirma generación exitosa
```

**Ejemplo de salida:**
```
✅ Resumen generado exitosamente: 260225/RESUMEN_260225.md

📊 Estadísticas:
   - Tareas completadas: 5
   - Tareas pendientes: 2
   - Horas trabajadas: 7h 30m
   - Documentos: 8
```

## Características Clave

✅ **Carpetas Diarias** - Organiza todo en carpetas YYMMDD (260225, 260226...)  
✅ **Gestión Unificada** - PRD + conversaciones + documentos en un solo lugar  
✅ **Metadatos de Archivos** - Rastrea fecha creación/modificación de documentos  
✅ **Hora de Inicio Automática** - Detecta cuándo empezó el día (primer archivo)  
✅ **Formato Jerárquico** - Estructura clara con encabezados H3 y emojis  
✅ **Timestamps Exactos** - Registra hora de inicio de cada tarea  
✅ **Documentación Completa** - Descripción + Solución para auditoría  
✅ **Resumen Automático del Día** - Analiza carpeta y genera reporte completo  
✅ **Reportes de Horas** - Scripts Python/PowerShell generan horas trabajadas  
✅ **Gestión de Pendientes** - Seguimiento de tareas en progreso  
✅ **Git-friendly** - Markdown puro, fácil de versionear  
✅ **Rastreabilidad Completa** - Auditoría diaria con toda la información

## Ejemplos de Registros Reales

### Tarea Simple (Bug Fix)

```markdown
### ✅ 2. Corregir validación en formulario — **11:15**

**Descripción**  
Usuario reportó error en validación de email en formulario de contacto. La validación rechazaba emails válidos con subdominios. Impacta signup de nuevos usuarios.

**Solución**  
Se identificó regex incorrecto en campo email (patrón muy restrictivo). Se actualizó patrón de validación a RFC 5322. Se testeó con 50 casos de prueba. Desplegado en producción. Validado con clientes específicos.
```

### Tarea Compleja (Integración)

```markdown
### ✅ 5. Integración con API de Stripe — **14:45**

**Descripción**  
Cliente solicita añadir nuevo proveedor de pagos (Stripe) al sistema. Requerido conectar a sistema actual, modificar flujo de checkout y actualizar documentación. Esta es actividad crítica para Q1.

**Solución**  
Se implementó cliente Stripe official. Se integraron webhooks para confirmación de pago y reembolsos. Se actualizó checkout para soportar múltiples proveedores (Stripe + PayPal). Testing completado con casos de éxito y error. Demo realizado con cliente. Documentación actualizada.
```

## Scripts Disponibles

### create_daily_folder.py (NUEVO)

Crea una carpeta diaria con formato YYMMDD y README.md inicial.

```bash
python scripts/create_daily_folder.py [--date 2026-02-25] [--path ./path]
```

**Características:**
- Crea carpeta con formato YYMMDD (260225 para 25 de febrero de 2026)
- Genera README.md dentro de la carpeta con información del día
- Verifica si la carpeta ya existe antes de crear

### create_daily_prd.py (ACTUALIZADO)

Crea un nuevo archivo PRD_YYYYMMDD.md **dentro de la carpeta del día**.

```bash
python scripts/create_daily_prd.py [--date 2026-02-16] [--path ./path]
```

**Novedades:**
- Si `use_daily_folders: true` en config.json, crea automáticamente la carpeta YYMMDD
- Guarda el PRD dentro de la carpeta del día
- Incluye timestamp de creación en el documento

### create_daily_prd.ps1

Versión PowerShell de creación de PRD con soporte para carpetas diarias.

```powershell
.\scripts\create_daily_prd.ps1 -Date "2026-02-16" -Output "./path"
```

### generate_day_summary.py (NUEVO)

Analiza todos los archivos de la carpeta del día y genera un resumen completo.

```bash
python scripts/generate_day_summary.py [--date 20260225] [--path ./base] [--output ./reports]
```

**Características:**
- Lee **metadatos** de todos los archivos (fecha creación, modificación, tamaño)
- Determina **hora de inicio del día** (primer archivo creado)
- Extrae **tareas del PRD** (completadas y pendientes)
- Calcula **horas trabajadas** basado en timestamps
- Lista **todos los documentos** generados en el día
- Genera **RESUMEN_YYMMDD.md** con análisis completo

**Output:** `RESUMEN_260225.md` dentro de la carpeta del día

### generate_hours_report.py

Analiza un PRD y genera reporte de horas trabajadas.

```bash
python scripts/generate_hours_report.py PRD_260216.md [--output ./reports]
```

**Output:** `HORAS_PRD_260216.md` con desglose detallado

### generate_hours_report.ps1

Versión PowerShell de generación de reportes.

```powershell
.\scripts\generate_hours_report.ps1 -PRDFile "PRD_260216.md" -Output "./reports"
```

## Checklist de Completitud

Antes de terminar el día, verifica:

- [ ] ¿Todas las tareas realizadas tienen descripción clara?
- [ ] ¿Cada solución explica QUÉ se hizo y POR QUÉ?
- [ ] ¿Hay timestamps para cada tarea?
- [ ] ¿Las tareas pendientes están claramente documentadas?
- [ ] ¿El PRD está guardado en la carpeta del día (YYMMDD)?
- [ ] ¿Todos los documentos del día están en la carpeta diaria?
- [ ] ¿Has generado el resumen del día? (`generate_day_summary.py`)
- [ ] ¿Verificaste que el resumen incluye hora de inicio correcta?
- [ ] ¿Generaste el reporte de horas detallado? (opcional: `generate_hours_report.py`)
- [ ] ¿Validaste que los totales de horas son correctos?

**NUEVO: Checklist Carpetas Diarias**

- [ ] ¿La carpeta tiene formato YYMMDD correcto?
- [ ] ¿Hay un README.md descriptivo en la carpeta?
- [ ] ¿El RESUMEN_YYMMDD.md fue generado?
- [ ] ¿Están todos los documentos relevantes archivados?

## Referencias

- [Estructura Detallada](references/structure.md) - Detalles técnicos completos
- [Plantilla](assets/template.md) - Plantilla lista para usar
- [Skill PRD](../prd/SKILL.md) - Para análisis profesionales profundos

## Licencia

MIT License - Libre para usar y modificar
