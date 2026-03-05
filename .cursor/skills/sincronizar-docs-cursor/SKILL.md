---
name: sincronizar-docs-cursor
description: Sincroniza la documentación de .cursor/rules (y agents) con el estado real del proyecto ARGOS. Aplica cambios técnicos directamente y reporta en una frase. Invocar cuando el usuario pida "sincronizar documentación .cursor" durante el trabajo, o como parte del cierre del día (skill cierre-del-dia).
---

# Sincronizar documentación .cursor

Objetivo: que toda la documentación en `.cursor/rules/` (y, si aplica, `.cursor/agents/`) refleje el estado actual del proyecto ARGOS. No pedir aprobación para estas actualizaciones técnicas; aplicarlas de forma autónoma y solo informar al usuario cuando termines.

**Uso:** Durante el trabajo cuando el usuario lo pida explícitamente, o al final del día como paso de la skill cierre-del-dia.

## Procedimiento

1. **Revisa el estado real del proyecto:**
   - `argos-app/back/requirements.txt` y dependencias principales del backend
   - `argos-app/front/package.json` (dependencias, scripts) y estructura de `app/` y `src/`
   - `argos-car/argos-architecture/src/` (lenguaje, librerías, pines si hay cambios relevantes)
   - `argos_alexa/` (estructura y docs)

2. **Compara con lo documentado en:**
   - `GLOBAL.md` — "Stack general del proyecto" y "Reglas universales de código"
   - `CONTEXT.md` — estado de módulos, próximos pasos, obstáculos
   - Cada regla de sector: `backend.md`, `frontend.md`, `ia-engineer.md`, `games.md`, `business.md`, `mecatronica.md` (stack, convenciones, [COMPLETAR] que ya se puedan rellenar con datos actuales)

3. **Para cada desfase detectado:** Escribe directamente la actualización en el archivo correspondiente. Solo información técnica: stack, dependencias, estructura, estado de módulos. No cambies filosofía, nombres de agentes ni flujos de trabajo.

4. **Al terminar:** Informa al usuario en una sola frase, por ejemplo: "Listo. Actualicé los archivos de .cursor con la información técnica actual del proyecto."
