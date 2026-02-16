---
name: prd-diario
description: 'Gestiona tareas diarias con formato jerárquico legible, documentación completa (descripción + solución) con timestamps, y genera reportes automáticos de horas trabajadas. Usa cuando necesites crear PRD diario, registrar tareas completadas, gestionar pendientes, o generar reportes de horas. Incluye scripts Python/PowerShell para automatizar todo.'
license: MIT
---

# PRD Diario - Gestor de Tareas Diarias

## Descripción General

Automatiza la creación y actualización de Documentos de Requisitos de Productos (PRD) diarios para un seguimiento estructurado de tareas. Ideal para:

- Registro de tareas realizadas con timestamps exactos
- Documentación detallada de descripción y soluciones implementadas
- Gestión de tareas pendientes para el día siguiente
- Generación automática de reportes de horas trabajadas
- Auditoría y reportes diarios a stakeholders

## Cuándo Usar Este Skill

Use este skill cuando:

- Necesite crear un PRD nuevo para un día específico
- Quiera registrar tareas completadas con hora exacta
- Deba documentar soluciones de manera estructurada
- Tenga tareas pendientes que requieran seguimiento
- Necesite generar reportes de horas trabajadas al final del día
- El usuario pida "crear PRD diario", "registrar tarea completada", o "generar reporte de horas"

## Flujo de Trabajo

### Fase 1: Inicialización Diaria

Cuando sea la primera vez en el día:

1. **Verificar archivo existente**: Busca `PRD_YYYYMMDD.md` en carpeta del proyecto
2. **Si existe**: Continúa a Fase 2
3. **Si no existe**: Crea nuevo PRD usando `scripts/create_daily_prd.py` o `create_daily_prd.ps1`

### Fase 2: Registrar Tareas Realizadas

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

## Estructura Recomendada del PRD Diario

Ver [structure.md](references/structure.md) para detalles completos.

**Resumen rápido:**

```markdown
# PRD - DD de MMMM de YYYY

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

### Crear PRD Nuevo

```
Usuario: "Vamos a crear el PRD de hoy"
Claude:
1. Obtiene fecha actual (ej: 16 de febrero de 2026)
2. Verifica si existe PRD_260216.md
3. Si no existe, crea usando scripts/create_daily_prd.py
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

## Características Clave

✅ **Formato Jerárquico** - Estructura clara con encabezados H3 y emojis  
✅ **Timestamps Exactos** - Registra hora de inicio de cada tarea  
✅ **Documentación Completa** - Descripción + Solución para auditoría  
✅ **Reportes Automáticos** - Scripts Python/PowerShell generan horas  
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

### create_daily_prd.py

Crea un nuevo archivo PRD_YYYYMMDD.md con estructura base.

```bash
python scripts/create_daily_prd.py [--date 2026-02-16] [--output ./path]
```

### create_daily_prd.ps1

Versión PowerShell de creación de PRD.

```powershell
.\scripts\create_daily_prd.ps1 -Date "2026-02-16" -Output "./path"
```

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
- [ ] ¿El archivo está guardado con nombre PRD_YYYYMMDD.md?
- [ ] ¿Has generado el reporte de horas? (python/powershell script)
- [ ] ¿Validaste que los totales de horas son correctos?

## Referencias

- [Estructura Detallada](references/structure.md) - Detalles técnicos completos
- [Plantilla](assets/template.md) - Plantilla lista para usar
- [Skill PRD](../prd/SKILL.md) - Para análisis profesionales profundos

## Licencia

MIT License - Libre para usar y modificar
