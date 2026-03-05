---
name: coordinar-multi-sector
description: Coordina trabajo entre varios subagentes (por nombre). Confirma sectores, obtiene tareas, delega a cada subagente según su regla, recoge resultados, presenta resumen consolidado y espera feedback. Invocar cuando el usuario indique trabajo en varios sectores (ej. "hoy trabajamos en app: backend, frontend y chatbot").
---

# Coordinar múltiples sectores

Cuando el usuario indique que hoy se trabaja en más de un sector (app o mecatrónica), Zeus coordina y delega.

## Mapa nombre → regla (`.cursor/rules/`)

| Nombre   | Regla        |
|----------|--------------|
| Apolo    | `backend.md` |
| Afrodite | `frontend.md` |
| Atena    | `ia-engineer.md` |
| Loki     | `games.md`   |
| Era      | `business.md` |
| Hermes   | `mecatronica.md` (argos-car o argos_alexa según indique el usuario) |

## Pasos

1. **Confirmar sectores:** Confirma los sectores y los nombres (ej. "Entendido. Voy a coordinar backend, frontend e IA (Apolo, Afrodite, Atena). ¿Cuáles son las tareas para cada uno?").

2. **Obtener tareas:** Espera a que el usuario indique las tareas por sector o por nombre.

3. **Delegar:** Para cada sector, delega al subagente correspondiente (definido en `.cursor/agents/`). Cada subagente sigue su regla en `.cursor/rules/` según la tabla anterior.

4. **Recoger resultados:** Recoge los resultados de cada subagente.

5. **Presentar:** Presenta al usuario un resumen consolidado del trabajo de cada uno (por nombre/sector).

6. **Feedback:** Espera validación y feedback del usuario para llevar de vuelta a los subagentes si hace falta.
