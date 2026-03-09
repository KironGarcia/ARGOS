# CONTEXT.md — Estado Actual del Proyecto ARGOS

> Este archivo es actualizado por el usuario al final de cada sesión de trabajo.
> Es la memoria viva del proyecto. Léelo siempre al inicio.

---

## Última actualización
**Fecha:** 2026-03-07  
**Sesión:** Trabajo con **mecatrónica (Hermes)**. Ultrasonic HC-SR04 alimentado directo desde la Pi (GND Pin 9). OTA configurado en ESP32 (sketch ota_wifi). Módulo SD definido (MOSI 23, MISO 19, SCK 4, CS 22; D5/D18 ocupados por LEDs). LEDs reintroducidos — dos amarillos, alimentación por cable USB cortado (evitar interferencia en altavoz). Checkpoint 2 (argos_alexa) y Checkpoint 4 (argos-car) creados. Audios de voz en ''argos_alexa/audio/''; mapa frase disparadora → audio → acción documentado en Checkpoint 2 (iniciar demo, nombre ARGOS, piada, voice control, tocar música). Límite seguro de keywords: 10–12. Pilhas AA removidas del carro; dos fuentes (batería motores + powerbank Pi). ZIM actualizado con Hermes. Pendiente: script presentación del carro en RPi; integrar SD y reproducción .wav en sketch único ESP32; entrenar modelo con frases.

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
| argos-car | ⏳ Stage 1 | RPi Zero W, L298N, JGA25 12V, HC-SR04 alimentado desde Pi (GND Pin 9). Checkpoint 4: ultrasonic en Pi, dos fuentes (batería + powerbank), sin pilhas AA. Código en argos-architecture/src. |
| argos_alexa | ⏳ Stage 2 | ESP32 + INMP441 + PAM8403 + altavoz 4Ω 3W. LEDs (D5, D18) reintroducidos, alimentación por cable USB cortado. OTA (ota_wifi) y SD (SCK=4, CS=22) definidos. Audios en audio/; mapa frase→audio en Checkpoint_2. Checkpoint_1 y Checkpoint_2 en zim/Development/. |

---

## Lo que está funcionando

- **Sistema de trabajo:** Apertura de Cursor → carga GLOBAL → carga orquestrador (Zeus). Puedes decir "Zeus, hoy necesito tu ayuda" o usar palabras clave (HOY TRABAJAMOS EN BACKEND, etc.). Cierre del día con "terminamos el trabajo del día" actualiza CONTEXT, pregunta por ZIM y sincroniza documentación .cursor. Skills disponibles para coordinar varios sectores y para sugerir nuevas skills cuando detectes tareas recurrentes.
- **Reglas con datos reales:** Backend (stack, BD, endpoints), frontend (stack, tema, componentes, ApiConfig), mecatrónica (pines, checkpoints, Alexa), ia-engineer (stack, intents, personalidad Argos, integración LLM).
- **Producto (app):** Auth, dispositivos, comandos, logs, alertas, chatbot de seguridad y Bluetooth en desarrollo; validar en entorno real según corresponda.
- **argos_alexa hardware:** INMP441 + PAM8403 + altavoz validados. Sketches de test funcionales. Arquitectura Edge Impulse + WiFi + Flask + SD card definida y documentada en Checkpoint_1.

---

## Obstáculos conocidos

- Games y business: sin avance aún en producto, por eso sus reglas siguen con [COMPLETAR].
- Mecatrónica: sensor HC-SR04 en pines que pueden interferir con SPI; monitorear si se usa SPI. Comunicación app ↔ carro cuando el carro esté registrado como dispositivo (según backend).
- argos_alexa: reproducción de audio por DAC desde SD aún por integrar en sketch único; pines SD ya definidos (D4, D22 para SCK/CS; D5/D18 para LEDs).

---

## Próximos pasos priorizados

1. **argos_alexa:** Integrar en sketch único: SD (SCK=4, CS=22), reproducción .wav desde ''audio/'', luego Edge Impulse (frases disparadoras) y Flask en RPi. Crear script de presentación del carro en RPi.
2. Avanzar en el proyecto (app, carro o Alexa) según prioridad; con eso se podrán rellenar games.md y business.md cuando haya contenido.
3. Al cerrar sesiones futuras, seguir actualizando CONTEXT (y ZIM solo si tú lo pides).

---

## Decisiones importantes ya tomadas

- **Orquestrador y skills:** Las reglas del orquestrador son livianas (solo triggers); los procedimientos largos viven en skills (cierre del día, sincronizar docs, actualizar ZIM, coordinar multi-sector, sugerir skill). Así no se sobrecarga el contexto.
- **Carga automática:** GLOBAL se carga siempre (alwaysApply); la primera instrucción de GLOBAL es leer orquestrador y actuar como Zeus desde el inicio. No hace falta decir "HOY TRABAJO CON EL ORQUESTRADOR".
- **Nombres por agente:** Zeus (orquestrador), Apolo (backend), Afrodite (frontend), Atena (IA), Loki (games), Era (empresa), Hermes (mecatrónica). Para delegar por nombre ("dile a Apolo que...").
- **Sincronización .cursor:** Al decir "terminamos el trabajo del día", Zeus actualiza CONTEXT (con tu aprobación), pregunta por ZIM y luego sincroniza automáticamente la documentación técnica de .cursor (sin pedir aprobación por cada cambio técnico).
- **ZIM:** Solo se actualiza cuando tú lo pides explícitamente; siempre en inglés y siguiendo el patrón existente.
- **Idiomas:** Conversación contigo = español; código, comentarios, strings, contexto ARGOS = portugués (Brasil); documentación ZIM = inglés.
- **argos_alexa LEDs:** Dos LEDs amarillos reintroducidos (D5, D18), alimentación por cable USB cortado para evitar interferencia en altavoz. Hardware = ESP32 + INMP441 + PAM8403 + altavoz + LEDs.
- **argos_alexa arquitectura de voz:** Edge Impulse (10 keywords locales en ESP32, sin internet) + WiFi HTTP POST al RPi + Flask server + .wav pre-grabados en SD card + ESP8266Audio para reproducción. Control del carro por voz incluido (misma arquitectura, intents distintos que lanzan comandos en la RPi).
