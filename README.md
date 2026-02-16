# PRD Diario - GitHub Copilot Skill

Skill para GitHub Copilot que gestiona tareas diarias creando PRDs estructurados con tabla de tareas realizadas, pendientes y soluciones.

## 🎯 Características

✅ **Registro automático de tareas** - Con timestamps precisos  
✅ **Estructura consistente** - Tabla Markdown reutilizable diariamente  
✅ **Rastreabilidad completa** - Cada tarea con descripción y solución  
✅ **Gestión de pendientes** - Seguimiento de tareas incompletas  
✅ **Git-friendly** - Markdown puro, fácil de versionear  
✅ **Integración PRD** - Usa el skill PRD para análisis profesionales  
✅ **Scripts reutilizables** - Python y PowerShell para automatización  

## 📦 Contenido

```
prd-diario/
├── SKILL.md                      # Documentación principal
├── scripts/
│   ├── create_daily_prd.py      # Script Python para crear PRDs
│   └── create_daily_prd.ps1     # Script PowerShell para crear PRDs
├── references/
│   └── structure.md             # Documentación detallada de estructura
└── assets/
    └── template.md              # Plantilla base para nuevos PRDs
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
Copy-Item -R . "$env:USERPROFILE\.copilot\skills\prd-diario" -Force
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

```
"Crear PRD de hoy"
"Agregué completado: Revisar emails, completado a las 10:30"
"Tenemos una tarea pendiente: Revisar servidor Proxmox"
```

### Scripts Directos

#### Python
```bash
# Crear PRD de hoy
python scripts/create_daily_prd.py

# Crear PRD para fecha específica
python scripts/create_daily_prd.py --date 20260217

# Especificar carpeta de salida
python scripts/create_daily_prd.py --path ./PRD
```

#### PowerShell
```powershell
# Crear PRD de hoy
.\scripts\create_daily_prd.ps1

# Crear PRD para fecha específica
.\scripts\create_daily_prd.ps1 -Date "20260217"

# Especificar carpeta de salida
.\scripts\create_daily_prd.ps1 -Path "C:\My\PRD"
```

## 📋 Estructura del PRD Diario

```markdown
# PRD - 16 de febrero de 2026

## Resumen Ejecutivo
Documento de registro de tareas realizadas durante el día...

## Tareas Realizadas

| # | Tarea | Descripción | Solución | Hora |
|---|-------|-------------|----------|------|
| 1 | Revisar tareas en Trello | ... | ... | 09:00 |
| 2 | Solucionar bug Access | ... | ... | 11:15 |

## Tareas Pendientes

| # | Tarea | Descripción | Estado |
|---|-------|-------------|--------|
| 3 | Apagado Proxmox | ... | En curso |

## Notas Adicionales
- Observaciones importantes
```

Ver [references/structure.md](references/structure.md) para documentación completa.

## 🔗 Integración con Otros Skills

Este skill puede trabajar junto con:
- **Skill PRD** - Para análisis profesionales complejos incorporados en PRDs diarios
- **Git Commit** - Para versionear PRDs diarios automáticamente

## 📚 Ejemplos

### Tarea Simple (Bug Fix)
```
| 2 | Corregir validación email | Usuario reportó error en validación. Error: regex incorrecto | Se identificó regex incorrecto. Actualizado a RFC 5322. Testeado. Desplegado. | 11:15 |
```

### Tarea Compleja (Integración)
```
| 5 | Integración API pagos | Cliente solicita nuevo proveedor. Requiere actualizar checkout. | Se implementó cliente Stripe, webhooks, y actualización de checkout. Testing completado. | 14:45 |
```

## 🛠️ Mejor Práctica

1. **Crea PRD cada mañana** - Usa uno de los scripts o pide a Claude
2. **Registra tareas completadas** - Con descripción y hora
3. **Documenta soluciones** - Explica QUÉ, POR QUÉ y RESULTADO
4. **Marca pendientes** - Al final del día, lista lo incompleto
5. **Revisa diariamente** - Antes de terminar, valida completitud

## 📖 Documentación

- [SKILL.md](SKILL.md) - Documentación principal del skill
- [references/structure.md](references/structure.md) - Detalles técnicos y mejores prácticas
- [assets/template.md](assets/template.md) - Plantilla lista para usar

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit los cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo licencia MIT. Ver [LICENSE.txt](LICENSE.txt) para detalles.

## 👤 Autor

Desarrollado por **Juan José Luna** (@lunasoft2001) para **Luna-Soft**

## 🙋 Soporte

Si tienes preguntas o problemas:

1. Revisa [references/structure.md](references/structure.md)
2. Mira ejemplos en [SKILL.md](SKILL.md)
3. Abre un Issue en GitHub

## 📅 Historial

- **v1.0** (16 de febrero de 2026) - Versión inicial
  - Skill completo con documentación
  - Scripts Python y PowerShell
  - Plantilla y referencias

---

**Última actualización**: 16 de febrero de 2026
