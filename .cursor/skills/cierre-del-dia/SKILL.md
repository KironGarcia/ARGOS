---
name: cierre-del-dia
description: Flujo completo de cierre de sesión ARGOS. Resumen del día, actualizar CONTEXT con aprobación del usuario, preguntar por ZIM, invocar sincronizar-docs-cursor e informar al final. Invocar cuando el usuario diga "terminamos el trabajo del día".
---

# Cierre del día ARGOS

Flujo que Zeus ejecuta cuando el usuario indica que termina la sesión de trabajo.

## Pasos

1. **Pedir resumen:** Pide al usuario un resumen de lo que se hizo hoy (qué funcionó, qué quedó pendiente).

2. **Proponer CONTEXT:** Con esa información, propón la actualización de `.cursor/rules/CONTEXT.md`:
   - Fecha de hoy
   - Qué sesión fue (ej. "implementé login backend")
   - Estado actualizado de cada módulo trabajado
   - Lo que está funcionando
   - Obstáculos conocidos
   - Próximos pasos priorizados  
   Espera que el usuario apruebe o corrija el borrador antes de escribir.

3. **Preguntar ZIM:** Pregunta: "¿Quieres también actualizar algún documento ZIM hoy?"
   - Si **sí:** invoca la skill **actualizar-zim** y sigue su flujo (el usuario indicará qué documentar).
   - Si **no:** sigue al paso 4.

4. **Sincronizar documentación .cursor:** Invoca la skill **sincronizar-docs-cursor** para actualizar GLOBAL, CONTEXT y reglas de sector con la información técnica actual del proyecto. No pidas aprobación; aplica y al terminar pasa al paso 5.

5. **Cerrar:** Informa al usuario en una sola frase, por ejemplo: "Listo. Ya hicimos CONTEXT, ZIM (si aplica) y yo actualicé todos los archivos de .cursor con la información técnica actual. Listo."
