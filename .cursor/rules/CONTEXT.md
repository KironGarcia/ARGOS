# CONTEXT.md — Estado Actual del Proyecto ARGOS

> Este archivo es actualizado por el usuario al final de cada sesión de trabajo.
> Es la memoria viva del proyecto. Léelo siempre al inicio.

---

## Última actualización
**Fecha:** 2026-03-06  
**Sesión:** Primer día de trabajo físico con **argos_alexa**. Hardware validado (micrófono INMP441, amplificador PAM8403 + altavoz 4Ω 3W, LEDs testados y removidos del proyecto). Arquitectura de comunicación completa definida: Edge Impulse (10 palabras clave en ESP32) + WiFi HTTP POST → Flask RPi → .wav en SD card → ESP8266Audio + DAC GPIO 25. Módulo SD confirmado como componente requerido. Próxima sesión: conectar SD, instalar ESP8266Audio, probar reproducción .wav desde SD.

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
| argos_alexa | ⏳ Stage 2 — hardware validado | ESP32 Dev Module + INMP441 (I2S: WS=D15, SCK=D14, SD=D13) + PAM8403 + altavoz 4Ω 3W (DAC=D25). Sin LEDs (removidos). Sketches de test en alexa-architecture/src/. Arquitectura de voz definida: Edge Impulse (10 keywords) + WiFi HTTP POST → Flask RPi → .wav en SD card → ESP8266Audio. Módulo SD requerido (CS=D5, SCK=D18, MISO=D19, MOSI=D23). Checkpoint_1 en zim/Development/. |

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
- argos_alexa: reproducción de audio por DAC (ESP8266Audio) aún no probada — primer paso crítico de la próxima sesión. Verificar conflicto de pines SD (D5/D18) antes de conectar módulo.

---

## Próximos pasos priorizados

1. **argos_alexa — próxima sesión:** Conectar módulo SD (D5/D18/D19/D23), instalar ESP8266Audio, probar reproducción de .wav desde SD por DAC GPIO 25 → PAM8403 → altavoz. Si funciona, seguir con Edge Impulse (entrenar 10 keywords) y luego Flask en RPi.
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
- **argos_alexa sin LEDs:** LEDs (GPIO 5 y 18) testados pero removidos del proyecto final por interferencia con el altavoz y complejidad innecesaria. Hardware final = ESP32 + INMP441 + PAM8403 + altavoz.
- **argos_alexa arquitectura de voz:** Edge Impulse (10 keywords locales en ESP32, sin internet) + WiFi HTTP POST al RPi + Flask server + .wav pre-grabados en SD card + ESP8266Audio para reproducción. Control del carro por voz incluido (misma arquitectura, intents distintos que lanzan comandos en la RPi).
