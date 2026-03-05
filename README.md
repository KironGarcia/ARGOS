# ARGOS

**Carta de apresentação do projeto**

---

## O que é o ARGOS

O ARGOS é uma proposta de **proteção IoT doméstica** com foco em **educação** e **relacionamento com o usuário**. Em vez de ser só um bloqueador de ataques, atua como um **modelo educacional**: o usuário aprende a viver seguro em um mundo conectado, com o ArgosBot como guia e com **gamificação** para engajar sem perder o foco em segurança.

> **Nota:** Essa abordagem (educação + gamificação como núcleo do relacionamento) está em **estudo e validação**. As hipóteses de público e valor vêm de pesquisa e marco zero documentados no repositório; seguimos refinando com dados e feedback.

---

## Como nos organizamos: orquestração por regras e skills

Implementamos um **modelo de projeto** em que a rotina de desenvolvimento é guiada por **automação de tarefas**, **subagentes** (especialistas por área) e um sistema de **rules** e **skills** dentro do Cursor. O orquestrador (Zeus) centraliza o fluxo do dia; as reglas carregam contexto por setor (backend, frontend, IA, mecatrónica, negócios, games); as skills encapsulam procedimentos repetíveis (cierre del día, actualizar ZIM, coordinar varios sectores, etc.). Assim conseguimos um **novo modo de trabalho** — consistente, documentado e escalable — sem depender de um único “monólito” de instruções.

Estrutura principal (onde isso vive no repositório):

```
ARGOS/
├── .cursor/
│   ├── rules/           # Contexto por setor + estado vivo do projeto
│   │   ├── GLOBAL.md     # Cerebro global, palabras clave, filosofia
│   │   ├── orquestrador.md
│   │   ├── CONTEXT.md    # Memoria viva, última sesión, próximos pasos
│   │   ├── backend.md, frontend.md, ia-engineer.md, mecatronica.md, games.md, business.md
│   ├── skills/          # Procedimientos reutilizables (cierre del día, ZIM, multi-sector, etc.)
│   │   ├── cierre-del-dia/
│   │   ├── actualizar-zim/
│   │   ├── sincronizar-docs-cursor/
│   │   ├── coordinar-multi-sector/
│   │   └── sugerir-skill-subagente/
│   └── agents/          # Definición de subagentes (Apolo, Afrodite, Atena, Hermes, etc.)
├── zim/                 # Documentación general del proyecto (Zim wiki)
│   ├── ARGOS-STARTUP.txt # Descripción, propuesta de valor, canvas, estado
│   └── Technical_info_about_ARGOS.txt
├── argos-app/           # App: backend (FastAPI, auth, IoT, IA) + frontend (React Native/Expo)
├── argos-car/           # Carro autónomo (Raspberry Pi, motores, sensores) + zim
├── argos_alexa/         # Dispositivo “Alexa China” (ESP32, voz, demo de ataque) + zim
└── pesquisa-viabilidad/ # Pesquisa, marco zero, validação de produto
    └── marco-zero/
```

Cada setor tem sua regra (e, quando aplicável, seu agente); o CONTEXT mantém o estado atual; o ZIM guarda la narrativa y los avances en formato wiki.

---

## Documentação no Zim: dia a dia e descobertas

Toda a evolução do projeto — cada día de trabajo, avances técnicos y descubrimientos — fica registrada em **Zim** (formato wiki). Há ZIMs por subsistema: raiz (`zim/`), carro (`argos-car/zim/`), Alexa (`argos_alexa/zim/`), app (`argos-app/zim/`). Neles documentamos checkpoints, decisões de hardware, problemas resolvidos e o estado de cada fase. O **ARGOS-STARTUP** (em `zim/ARGOS-STARTUP.txt`) concentra a descrição geral, proposta de valor, canvas e roadmap; os demais entram em detalhe por domínio.

---

## Demonstração: do backdoor na “Alexa China” ao acidente simulado

A ideia de **apresentação** do ARGOS é mostrar um risco real através de uma **simulação controlada**: um atacante explora um **backdoor** (ou vulnerabilidades típicas) em um dispositivo tipo “Alexa China” (barato e inseguro). A partir daí, a invasão **escala lateralmente** até um **veículo autónomo** (o carro ARGOS), que recebe comandos maliciosos e pode ser levado a um **acidente simulado**. O ARGOS (app + lógica de proteção) **detecta e bloqueia** a escalada, exibindo em tempo real a diferença entre “atacado” e “protegido”. O objetivo é fixar na memória do público que o perigo é concreto e que a proteção ponta a ponta — do dispositivo em casa até o veículo — é o que estamos a construir.

---

## Impacto em construção: ponta a ponta nas nossas mãos

Todo esse ecossistema — **app**, **hardware** (carro e Alexa China), **documentação** (Zim e .cursor), e em breve **estudos e propostas de negócio** — está a ser construído **de ponta a ponta** pelas nossas mãos. Ainda não temos no README a parte formal de business (canvas de negócio, métricas, pitch); isso será adicionado quando avançarmos nessa frente. Por agora, este README serve como **carta de apresentação**: o que somos, como nos organizamos, onde está a documentação e qual história queremos contar na demo.

---

*Última atualização relevante: estrutura e carta de apresentação — março 2026.*
