# CONTEXT.md — Estado Actual del Proyecto ARGOS

> Este archivo es actualizado por el usuario al final de cada sesión de trabajo.
> Es la memoria viva del proyecto. Léelo siempre al inicio.

---

## Última actualización
**Fecha:** 2026-03-04  
**Sesión:** Creación del ZIM **ARGOS-STARTUP** en `zim/ARGOS-STARTUP.txt`. Descripción general del proyecto en inglés: propuesta de valor, experiencia, jobs to be done, públicos (B2C/B2B), resumen de modelo de negocio, estrategia de demo (Car + Alexa China), estado actual de app/carro/Alexa, e ideas nuevas (mecatrónica: dual-brain, personalidad, pivot Alexa China; .cursor: orquestrador, documentación). CONTEXT sigue como memoria viva; el ZIM se actualiza solo cuando lo pidas.

---

## Estado del sistema de trabajo (.cursor)

| Elemento | Estado | Notas |
|----------|--------|-------|
| GLOBAL.md | ✅ listo | Cerebro global, stack del proyecto, reglas universales, palabras clave. AlwaysApply + carga automática de orquestrador |
| Orquestrador (Zeus) | ✅ listo | Rule liviana; delega a 5 skills. Nombres del equipo: Zeus, Apolo, Afrodite, Atena, Loki, Era, Hermes |
| Skills | ✅ listo | cierre-del-dia, sincronizar-docs-cursor, actualizar-zim, coordinar-multi-sector, sugerir-skill-subagente |
| Subagentes (.cursor/agents/) | ✅ listo | backend, frontend, ia-engineer, games, business, mecatronica — cada uno con nombre y referencia a su regla |
| Reglas por sector | ✅ 4 rellenadas | backend.md, frontend.md, mecatronica.md, ia-engineer.md con stack, BD, endpoints, pines, intents, etc. |
| Reglas pendientes de rellenar | ⏳ cuando avance el proyecto | games.md, business.md — se completan cuando haya avance en juego y negocio |

---

## Estado del APP (producto)

| Módulo | Estado | Notas |
|--------|--------|-------|
| Backend - Auth | ⏳ en progreso | JWT, 2FA, TOTP, registro, login, refresh |
| Backend - IoT endpoints | ⏳ en progreso | devices, command, logs, alertas, Bluetooth |
| Frontend - Login / Auth | ⏳ en progreso | AuthContext, login, 2FA, verify-email, totp-setup |
| Frontend - Home / Dashboard | ⏳ en progreso | home, devices, logs, advanced-logs, argos-bot, new-device |
| Chatbot IA | ⏳ en progreso | Asistente Argos, intents, LLM opcional, endpoints /ai/* |
| Gamificación | 🔴 no iniciado | White Hat Wizard — pendiente |

## Estado del CARRO / Alexa (mecatrónica)

| Módulo | Estado | Notas |
|--------|--------|-------|
| argos-car | ⏳ Stage 1 | RPi Zero W, L298N, JGA25 12V, tracción diferencial, HC-SR04. Código en argos-architecture/src. Checkpoint actualizado |
| argos_alexa | 🔴 documentación / plan | Stage 2 en Zim; ESP32 como “Alexa china”; integración y voz por hacer |

---

## Lo que está funcionando

- **Sistema de trabajo:** Apertura de Cursor → carga GLOBAL → carga orquestrador (Zeus). Puedes decir "Zeus, hoy necesito tu ayuda" o usar palabras clave (HOY TRABAJAMOS EN BACKEND, etc.). Cierre del día con "terminamos el trabajo del día" actualiza CONTEXT, pregunta por ZIM y sincroniza documentación .cursor. Skills disponibles para coordinar varios sectores y para sugerir nuevas skills cuando detectes tareas recurrentes.
- **Reglas con datos reales:** Backend (stack, BD, endpoints), frontend (stack, tema, componentes, ApiConfig), mecatrónica (pines, checkpoints, Alexa), ia-engineer (stack, intents, personalidad Argos, integración LLM).
- **Producto (app):** Auth, dispositivos, comandos, logs, alertas, chatbot de seguridad y Bluetooth en desarrollo; validar en entorno real según corresponda.

---

## Obstáculos conocidos

- Games y business: sin avance aún en producto, por eso sus reglas siguen con [COMPLETAR].
- Mecatrónica: sensor HC-SR04 en pines que pueden interferir con SPI; monitorear si se usa SPI. Comunicación app ↔ carro cuando el carro esté registrado como dispositivo (según backend).

---

## Próximos pasos priorizados

1. Usar el orquestrador en el día a día (Zeus + palabras clave + cierre del día) para afianzar el flujo.
2. Avanzar en el proyecto (app, carro o Alexa) según prioridad; con eso se podrán rellenar games.md y business.md cuando haya contenido.
3. Al cerrar sesiones futuras, seguir actualizando CONTEXT (y ZIM solo si tú lo pides).

---

## Decisiones importantes ya tomadas

- **Orquestrador y skills:** Las reglas del orquestrador son livianas (solo triggers); los procedimientos largos viven en skills (cierre del día, sincronizar docs, actualizar ZIM, coordinar multi-sector, sugerir skill). Así no se sobrecarga el contexto.
- **Carga automática:** GLOBAL se carga siempre (alwaysApply); la primera instrucción de GLOBAL es leer orquestrador y actuar como Zeus desde el inicio. No hace falta decir "HOY TRABAJO CON EL ORQUESTRADOR".
- **Nombres por agente:** Zeus (orquestrador), Apolo (backend), Afrodite (frontend), Atena (IA), Loki (games), Era (empresa), Hermes (mecatrónica). Para delegar por nombre ("dile a Apolo que...").
- **Sincronización .cursor:** Al decir "terminamos el trabajo del día", Zeus actualiza CONTEXT (con tu aprobación), pregunta por ZIM y luego sincroniza automáticamente la documentación técnica de .cursor (sin pedir aprobación por cada cambio técnico).
- **ZIM:** Solo se actualiza cuando tú lo pides explícitamente; siempre en inglés y siguiendo el patrón existente.
- **Comentarios y strings en código:** Portugués (Brasil) en todo el proyecto ARGOS.
