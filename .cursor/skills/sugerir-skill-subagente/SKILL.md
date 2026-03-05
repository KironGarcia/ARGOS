---
name: sugerir-skill-subagente
description: Detecta tarea o secuencia recurrente con un subagente o con el orquestrador (Zeus) y sugiere al usuario crear una skill. Aplica a Apolo, Afrodite, Atena, Loki, Era, Hermes y también a Zeus. Si el usuario aprueba, crea la skill y actualiza rules/agents para que se invoque cuando corresponda.
---

# Sugerir skill para subagente (o para Zeus)

Aplica a **todos los agentes**: subagentes (Apolo, Afrodite, Atena, Loki, Era, Hermes) **y al orquestrador (Zeus)**. Si detectas que le pides a Zeus cosas que se repiten y podrían volverse una skill para él mismo, también aplica.

## Cuándo sugerir

- **Recurrente:** La misma tarea o la misma secuencia de pasos/comandos con el mismo agente (subagente o Zeus), por ejemplo 2 o más veces en la sesión, o un patrón claro (ej. "cada vez que depuramos backend hacemos los mismos comandos").
- **Momento:** Sugiere después de completar esa tarea o cuando el usuario pregunte "¿algo más?" o cierre un tema. No interrumpas a mitad de tarea.

## Cómo formular la sugerencia

Redacta un mensaje al usuario en este estilo:

- Si es para un **subagente:** "Vi que con [nombre] repetimos [descripción breve]. ¿Te parece si te propongo una skill para [nombre] para esto? Así no tendrías que dar las mismas instrucciones cada vez."
- Si es para **Zeus:** "Vi que me pides [X] a menudo. ¿Te parece si te propongo una skill para mí (Zeus) para esto? Así podríamos automatizarlo cuando haga falta."

No crees ni escribas la skill todavía. Solo propón y espera la respuesta del usuario.

## Si el usuario aprueba

1. **Crear la skill:** Crea el archivo de la nueva skill en el lugar correcto:
   - Si es para un **subagente:** `.cursor/skills/[nombre-descriptivo]/SKILL.md` (ej. `debug-backend-apolo`, `build-frontend-atenea`). El contenido de SKILL.md debe tener frontmatter (name, description) e instrucciones claras del "cómo" para esa tarea recurrente.
   - Si es para **Zeus:** `.cursor/skills/[nombre-descriptivo]/SKILL.md` (ej. `resumen-diario-zeus`). Mismo formato.

2. **Actualizar rules o agents para invocar la skill:** Garantiza que el agente que usará la skill sepa cuándo invocarla:
   - Si la skill es para un **subagente:** Actualiza la regla del sector en `.cursor/rules/` (ej. `backend.md` para Apolo) añadiendo una línea o sección que indique: "Cuando [situación X], invoca la skill [nombre-de-la-skill]." Así Apolo (y su regla) saben que en esa situación deben usar la skill.
   - Si la skill es para **Zeus:** Actualiza `.cursor/rules/orquestrador.md` añadiendo en la sección de palabras clave o triggers algo como: "Cuando [situación X], invoca la skill [nombre-de-la-skill]."

Así no solo se crea el archivo de la skill: los archivos de rules (y agents si aplica) quedan actualizados para que el agente correspondiente haga la llamada a esta skill cuando la situación se dé.

3. **Confirmar al usuario:** Indica que la skill fue creada y que la regla/agente correspondiente ya está actualizado para invocarla cuando corresponda.
