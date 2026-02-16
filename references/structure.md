# Estructura Detallada del PRD Diario

## Tabla de Contenidos

1. [Encabezado](#encabezado)
2. [Resumen Ejecutivo](#resumen-ejecutivo)
3. [Tareas Realizadas](#tareas-realizadas)
4. [Tareas Pendientes](#tareas-pendientes)
5. [Notas Adicionales](#notas-adicionales)
6. [Columnas Especiales](#columnas-especiales)

---

## Encabezado

```markdown
# PRD - [DD de MMMM de YYYY]
```

**Propósito**: Identificar el documento y la fecha de forma clara

**Formato**:
- Fecha completa en español
- Ejemplo: `# PRD - 16 de febrero de 2026`

**Notas**: 
- Usar siempre el mismo formato para consistencia
- Facilita búsqueda en el repositorio

---

## Resumen Ejecutivo

```markdown
## Resumen Ejecutivo

Documento de registro de tareas realizadas durante el día con descripciones, soluciones y horas de ejecución.
```

**Propósito**: Contexto rápido del documento

**Qué incluir**:
- Una línea de descripción del propósito
- Total de tareas realizadas (opcional pero recomendado)
- Métricas de productividad (opcional)

**Ejemplo mejorado**:
```markdown
## Resumen Ejecutivo

Documento de registro de tareas realizadas el 16 de febrero de 2026.
- **Tareas completadas**: 7
- **Tareas pendientes**: 2
- **Horas productivas**: 8.5 horas
```

---

## Tareas Realizadas

### Estructura de Tabla

```markdown
| # | Tarea | Descripción | Solución | Hora |
|---|-------|-------------|----------|------|
| 1 | ... | ... | ... | HH:MM |
```

### Columna: #

**Propósito**: Índice secuencial de tareas

**Reglas**:
- Comenzar en 1
- Incrementar secuencialmente
- Útil para referencias cruzadas

**Ejemplo**: `1`, `2`, `3`, ...

---

### Columna: Tarea

**Propósito**: Nombre corto y descriptivo de la tarea

**Características**:
- Máximo 50 caracteres (idealmente)
- Usar sustantivo + verbo o sustantivo compuesto
- Ser específico pero conciso

**Buenos ejemplos**:
- ✅ "Revisar tareas en Trello"
- ✅ "Solucionar importación de pagos en Access"
- ✅ "Correo a Rottmann sobre Canon"
- ❌ "Trabajo" (muy vago)
- ❌ "Hacer todo lo del proyecto" (muy amplio)

---

### Columna: Descripción

**Propósito**: Contexto completo de la tarea

**Qué incluir**:
1. **Origen**: ¿Quién solicitó? ¿De dónde vino?
2. **Problema**: ¿Cuál era el estado antes?
3. **Complejidad**: ¿Requería investigación? ¿Fue rutinaria?
4. **Dependencias**: ¿Bloqueaba algo más?
5. **Contexto**: ¿Por qué era importante?

**Extensión**: 1-3 oraciones (máximo 150 caracteres)

**Ejemplo detallado**:
```
Importación de pagos desde Excel del gestor a ERP Fidas fallaba. 
Alexandra requería solución urgente para continuar con reconciliación.
```

**Estructura sugerida**:
```
[PROBLEMA INICIAL]. [QUIÉN/QUÉ SOLICITÓ]. [IMPACTO SI NO SE RESOLVÍA].
```

---

### Columna: Solución

**Propósito**: Explicar QUÉ se hizo, POR QUÉ y RESULTADO

**Componentes obligatorios**:
1. **Causa identificada** (si aplicable): ¿Cuál era la raíz del problema?
2. **Acción realizada**: ¿Qué se hizo exactamente?
3. **Validación**: ¿Cómo se verificó que funciona?
4. **Resultado**: ¿Cuál es el estado actual?

**Extensión**: 1-2 oraciones (máximo 200 caracteres)

**Estructura sugerida**:
```
[CAUSA] → [ACCIÓN] → [VALIDACIÓN] → [RESULTADO]
```

**Ejemplos**:

```
Causa: Fidas había escrito mal el nombre de la hoja y 2 campos.
Se corrigieron los nombres coincidentes. Se realizó importación exitosa.
```

```
Se envió correo al proveedor Rottmann solicitando información sobre 
compatibilidad ARM64. Pendiente respuesta.
```

```
Se identificó regex incorrecto. Actualizado a RFC 5322. Testeado 
con 50 casos. Desplegado en producción. Validado por usuario.
```

---

### Columna: Hora

**Propósito**: Timestamp exacto de completitud

**Formato**: `HH:MM` (formato 24 horas)

**Reglas**:
- Usar hora de conclusión (no inicio)
- Ser lo más preciso posible
- Útil para análisis de productividad

**Ejemplos**: `09:00`, `11:15`, `14:45`, `16:30`

**Cómo obtener automáticamente** (PowerShell):
```powershell
Get-Date -Format "HH:mm"
```

---

## Tareas Pendientes

### Estructura

```markdown
## Tareas Pendientes

| # | Tarea | Descripción | Estado |
|---|-------|-------------|--------|
| X | ... | ... | En curso / Bloqueado / En espera |
```

### Columna: Estado

**Valores permitidos**:
- **En curso**: Iniciada, trabajo activo
- **Bloqueado**: Esperando información/aprobación/recursos
- **En espera**: Pendiente de fecha futura o tercero
- **Pendiente**: Aún no iniciada

**Ejemplo de sección**:

```markdown
## Tareas Pendientes

| # | Tarea | Descripción | Estado |
|---|-------|-------------|--------|
| 5 | Preparar apagado de Proxmox | Servidor funcionando lentamente. Requerida parada controlada para mantenimiento. | En curso - Próximos pasos a definir |
| 6 | Respuesta de Rottmann | Esperando respuesta del proveedor sobre compatibilidad Canon. | En espera |
```

---

## Notas Adicionales

**Propósito**: Información contextual, observaciones, o decisiones importantes

**Qué incluir**:
- Reflexiones sobre el día
- Patrones observados
- Decisiones tomadas
- Próximos pasos generales
- Links a documentación relevante

**Formato**: Lista con puntos o párrafos

**Ejemplo**:

```markdown
## Notas Adicionales

- Servidor Proxmox requiere auditoría completa de VMs antes de apagado
- Necesario crear procedimiento documentado para futuros mantenimientos
- Canon/Rottmann: Posible incompatibilidad con procesadores ARM64
- Implementación de importaciones Access funcionando correctamente
- PRD diario establecido como rutina para gestión de tareas
```

---

## Columnas Especiales

### Categorización Opcional

Si deseas categorizar tareas, agrega estructura:

```markdown
| # | Categoría | Tarea | Descripción | Solución | Hora |
|---|-----------|-------|-------------|----------|------|
| 1 | Bug Fix | ... | ... | ... | 10:00 |
| 2 | Integración | ... | ... | ... | 11:30 |
| 3 | Admin | ... | ... | ... | 14:00 |
```

**Categorías recomendadas**:
- Bug Fix
- Feature
- Integración
- Investigación
- Admin
- Soporte
- Mantenimiento

### Duración Estimada (Opcional)

Útil para análisis de productividad:

```markdown
| # | Tarea | Descripción | Solución | Hora | Duración |
|---|-------|-------------|----------|------|----------|
| 1 | ... | ... | ... | 10:00 | 30 min |
```

---

## Mejores Prácticas

1. **Sé específico**: Evita términos vagos como "trabajar en proyecto"
2. **Documenta la causa**: No solo QUÉ, sino POR QUÉ y CÓMO
3. **Timestamps precisos**: Ayuda a análisis de productividad
4. **Pendientes claras**: Evita que se pierdan tareas
5. **Revision diaria**: Antes de terminar el día, revisa y completa
6. **Usa Markdown**: Facilita versionaje y búsqueda
7. **Nombres consistentes**: `PRD_YYYYMMDD.md` siempre

---

## Ejemplos Completos

### Día Asignado a Resolución de Bugs

```markdown
# PRD - 16 de febrero de 2026

## Resumen Ejecutivo
Día enfocado en resolución de bugs críticos y soporte técnico.
- **Tareas completadas**: 5
- **Tareas pendientes**: 1

## Tareas Realizadas

| # | Tarea | Descripción | Solución | Hora |
|---|-------|-------------|----------|------|
| 1 | Bug: Login no funciona | Usuario no puede ingresar desde Firefox. Error: token JWT inválido. Afectaba 15% de usuarios. | Se identificó incompatibilidad con caché del navegador. Se actualizó lógica de token. Validado en FF, Chrome, Safari. | 09:15 |
| 2 | Bug: Dashboard lento | Dashboard tardaba 8+ segundos en cargar. Usuarios se quejaban de experiencia pobre. | Se optimizaron queries N+1. Se añadió indexado a DB. Tiempo de carga: 1.2s. | 11:45 |
| 3 | Soporte: Cliente XYZ | Cliente reportó error en reporte de ventas. Reporte mostraba datos incorrectos. | Se encontró bug en fecha de filtro. Se corrigió lógica de comparación. Datos ahora correctos. | 14:00 |

## Tareas Pendientes

| # | Tarea | Descripción | Estado |
|---|-------|-------------|--------|
| 4 | Tests para login | Escribir tests automatizados para evitar regresión | En curso |

## Notas Adicionales
- Necesario establecer proceso de testing antes de deploy
- Considerar agregar monitoring para detectar bugs como el del login temprano
```

---

## Validación del Documento

Antes de finalizar el día, valida que:

- [ ] Todas las tareas tienen descripción clara
- [ ] Soluciones explican CAUSA → ACCIÓN → VALIDACIÓN
- [ ] Timestamps son consistentes y en orden
- [ ] Tareas pendientes son específicas y accionables
- [ ] Nombres de archivo siguen `PRD_YYYYMMDD.md`
- [ ] Markdown está bien formado (sin errores de sintaxis)
