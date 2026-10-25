# Evidencia — Episodio 3 (LAB-7)

Extractos saneados de las sesiones de Codex. Las transcripciones completas quedan fuera del
repo (~/.codex/sessions).

## Sesiones
| Parte | Sesión | Permisos (/status) | Duración |
| --- | --- | --- | --- |
| 3a — Consola | 01a17535-ab83-7121-ac3d-e421e0679d9f | Workspace (Ask for approval) | 55 s, más la corrección de nombres |
| 3b — Auditoría | 01a17545-7d05-70b2-a5c8-79e609e2d866 | Read Only (never) | 21 s |
| 3c — Correcciones | 01a1754c-d883-70a1-95d9-79184adf72f9 | Workspace (Ask for approval) | <completar> |

Codex CLI 0.164.0 · GPT-6-Luna (reasoning medium) · plan Free.

## 3a — Interfaz de consola
- Instrucción: "Leé docs/prompts/episodio-3a.md y seguí esas instrucciones."
- Acciones: creó reservas/__main__.py (+5), reservas/cli.py (+110) y tests/test_cli.py (+90);
  pytest: 17 passed; ajustó la prueba de CA8 (+12 −9) después de releer el criterio; pytest:
  17 passed; agregó su entrada en PROGRESO.md; ejecutó git status y git diff (solo lectura).
- Corrección pedida por el autor en la misma sesión: renombrar las 5 pruebas de test_cli.py con
  el número de requisito, como pide AGENTS.md.

## 3b — Auditoría en solo lectura
- Inicio: codex --sandbox read-only --ask-for-approval never
- Instrucción: "Leé docs/prompts/episodio-3b.md y respondé según esas instrucciones."
- Respuesta del agente, resumida:
  - Cobertura: CA1 a CA10 con al menos una prueba cada uno.
  - S2: reservas/dominio.py:29 elimina espacios alrededor de la fecha antes de parsearla.
  - S8: reservas/servicio.py:71-73 reinicia el contador de ID del repositorio en memoria.
  - Regla 3: reservas/servicio.py:131-139 valida por separado antes de la verificación
    unificada.
- Después: git status → working tree clean.

## 3c — Correcciones
- Instrucción: "Leé docs/prompts/episodio-3c.md y seguí esas instrucciones."
- Resultado: dominio.py, servicio.py y tests/test_dominio.py modificados; dos pruebas nuevas;
  entrada agregada en PROGRESO.md.
- Aprobaciones: <completar>.