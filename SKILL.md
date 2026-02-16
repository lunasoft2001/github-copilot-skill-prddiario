---
name: prd-diario
description: 'Gestiona tareas diarias creando PRDs estructurados con tabla de tareas realizadas, pendientes y soluciones. Integra el skill PRD para generación profesional. Usa cuando necesites crear o actualizar un PRD diario, registrar tareas completadas con horas y descripciones, o planificar tareas pendientes para el día siguiente.'
license: MIT
---

# PRD Diario - Gestor de Tareas Diarias

## Descripción General

Automatiza la creación y actualización de Documentos de Requisitos de Productos (PRD) diarios para un seguimiento estructurado de tareas. Ideal para equipos que necesitan:

- Registro automático de tareas realizadas con timestamps
- Seguimiento de soluciones implementadas
- Gestión de tareas pendientes para el día siguiente
- Documento centralizado para auditoría y reportes

## Cuándo Usar Este Skill

Use este skill cuando:

- Necesite crear un PRD nuevo para un día específico
- Quiera registrar tareas completadas con hora exacta
- Deba documentar soluciones de manera estructurada
- Tenga tareas pendientes que requieran seguimiento al día siguiente
- Necesite exportar o reportar actividades diarias a stakeholders
- El usuario pida "crear PRD diario", "registrar tareas de hoy", o "agregar tarea completada"

## Flujo de Trabajo

### Fase 1: Inicialización Diaria

Cuando sea la primera vez en el día:

1. **Verificar archivo existente**: Busca `PRD_YYYYMMDD.md` en la carpeta del proyecto
2. **Si existe**: Continúa a Fase 2
3. **Si no existe**: Crea nuevo PRD usando la plantilla de `assets/template.md`

### Fase 2: Registrar Tareas Realizadas

Para cada tarea completada:

1. **Obtener hora actual**: Usa `$(Get-Date -Format 'HH:mm')` en PowerShell
2. **Agregar fila a tabla**: Inserta en "Tareas Realizadas"
3. **Estructura de fila**: `| # | Nombre Tarea | Descripción Detallada | Solución/Resultado | Hora |`
4. **Descripción**: Incluye contexto, problema encontrado, origen de la solicitud
5. **Solución**: Explica qué se hizo, por qué, y resultado logrado

### Fase 3: Gestionar Tareas Pendientes

Para tareas incompletas:

1. **Crear sección "Tareas Pendientes"** (si aún no existe)
2. **Listar cada tarea pendiente** con contexto
3. **Al final del día**: Si hay tareas pendientes, generar PRD para mañana

### Fase 4: Crear PRD de Mañana (si aplica)

Si hay tareas pendientes:

1. **Crear archivo**: `PRD_YYYYMMDD_MAÑANA.md` (donde YYYYMMDD es el día siguiente)
2. **Usar estructura**:
   ```
   # PRD - [FECHA MAÑANA]
   
   ## Tareas Pendientes del Día Anterior
   
   [Copiar tareas de la sección Pendientes]
   
   ## Propias del Día
   
   [Espacio para nuevas tareas]
   ```

## Estructura Recomendada del PRD Diario

Ver [structure.md](references/structure.md) para detalles completos.

**Resumen rápido:**

```markdown
# PRD - DD de MMMM de YYYY

## Resumen Ejecutivo
Documento de registro de tareas realizadas con descripciones, soluciones y horas.

## Tareas Realizadas

| # | Tarea | Descripción | Solución | Hora |
|---|-------|-------------|----------|------|
| 1 | ... | ... | ... | HH:MM |

## Tareas Pendientes

| # | Tarea | Descripción | Estado |
|---|-------|-------------|--------|
| X | ... | ... | En curso / Bloqueado / En espera |

## Notas Adicionales
- Observaciones importantes
```

## Patrón de Uso - Paso a Paso

### Crear PRD Nuevo

```
Usuario: "Vamos a crear el PRD de hoy"
Claude: 
1. Obtiene fecha actual
2. Verifica si existe PRD_YYYYMMDD.md
3. Si no existe, crea usando template.md
4. Abre el archivo para edición
```

### Agregar Tarea Completada

```
Usuario: "Agregué completado: Revisar emails, tomó 30 min, completado a las 10:30"
Claude:
1. Calcula la fila: # = siguiente número
2. Obtiene hora = "10:30"
3. Genera fila con estructura completa
4. Inserta en tabla de Tareas Realizadas
5. Actualiza PRD en archivo
```

### Registrar Tarea Pendiente

```
Usuario: "Tenemos una tarea pendiente: Revisar servidor Proxmox"
Claude:
1. Agrega a sección Tareas Pendientes
2. Marca estado (En curso / Bloqueado / En espera)
3. Documenta contexto
```

## Integración con Skill PRD

Cuando el usuario solicite documentación más formal o análisis de requisitos complejos para una tarea diaria:

1. Usa el **skill PRD** para crear análisis profesional
2. Embebe los PRDs generados en el PRD Diario como referencias
3. Ejemplo: Si una tarea diaria es "Definir requisitos para nuevo módulo", usa PRD skill para análisis completo y resume en PRD diario

## Características Clave

✅ **Timestamps automáticos** - Registra hora exacta de cada tarea  
✅ **Estructura consistente** - Tabla Markdown reutilizable diariamente  
✅ **Rastreabilidad** - Cada tarea con descripción y solución  
✅ **Escalable** - Extensible para reportes y auditoría  
✅ **Git-friendly** - Markdown puro, fácil de versionear  
✅ **PRDs encadenados** - Soporte para tareas que se arrastran a días siguientes

## Ejemplos de Registros Reales

### Tarea Simple (Bug Fix)

```
| 2 | Corregir validación en formulario | Usuario reportó error en validación de email en formulario de contacto. Error: validación rechazaba emails válidos con subdominios | Se identificó regex incorrecto en campo email. Se actualizó patrón de validación a RFC 5322. Testeado con 50 casos. Desplegado en producción. | 11:15 |
```

### Tarea Compleja (Integración)

```
| 5 | Integración con API de pagos | Cliente solicita añadir nuevo proveedor de pagos (Stripe). Requerido conectar a sistema actual, modificar flujo de checkout y actualizar documentación | Se implementó cliente Stripe, se integraron webhooks para confirmación de pago, se actualizó checkout para soportar múltiples proveedores. Testing completado. Demo realizado con cliente. | 14:45 |
```

### Tarea Administrativa

```
| 7 | Preparación de backup de servidor | Mantenimiento preventivo del servidor principal. Requerido backup completo antes de actualización de SO | Se ejecutó backup completo (2.3TB). Se validó integridad. Se documentó procedimiento de restauración. Almacenado en servidor de backup externo. | 16:30 |
```

## Checklist de Completitud

Antes de terminar el día, verifica:

- [ ] ¿Todas las tareas realizadas tienen descripción clara?
- [ ] ¿Cada solución explica QUÉ se hizo y POR QUÉ?
- [ ] ¿Hay timestamps para cada tarea?
- [ ] ¿Las tareas pendientes están claramente listadas?
- [ ] ¿Si hay pendientes, se creó PRD para mañana?
- [ ] ¿El archivo está guardado en la carpeta correcta?
- [ ] ¿El nombre sigue formato PRD_YYYYMMDD.md?

## Referencias

- [Estructura Detallada](references/structure.md) - Detalles técnicos de cada sección
- [Plantilla](assets/template.md) - Plantilla lista para usar
- [Skill PRD](../prd/SKILL.md) - Para análisis profesionales profundos
