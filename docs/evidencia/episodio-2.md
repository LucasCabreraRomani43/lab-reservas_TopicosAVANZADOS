# Evidencia — Episodio 2 (LAB-6)

Extractos saneados de la sesión de Codex. La transcripción completa queda fuera del repo
(~/.codex/sessions).

## Sesión
- Codex CLI 0.164.0 · GPT-6-Luna (reasoning medium) · plan Free · 2026-10-25
- Sesión 01a17519-bdb1-7d83-8e31-10ab930130e0 · trabajó 49 s
- Límite mensual: 100 % antes y 99 % después

## Configuración al iniciar (/status)
- "Permissions: Workspace (Ask for approval)"
- "Agents.md: AGENTS.md"

## Instrucción
- "Leé docs/prompts/episodio-2.md y seguí esas instrucciones."

## Acciones del agente
- Leyó docs/prompts/episodio-2.md, docs/especificacion.md, docs/PROGRESO.md,
  reservas/servicio.py, reservas/dominio.py, tests/test_dominio.py, pyproject.toml y AGENTS.md.
- Editó reservas/servicio.py (+49 −11); creó reservas/persistencia.py (+128) y
  tests/test_persistencia.py (+77 y luego +9).
- Ejecutó .venv\Scripts\python -m pytest -q: 11 passed y, tras agregar una prueba, 12 passed
  (con una PytestCacheWarning, WinError 183).
- Editó docs/PROGRESO.md (+28 −1): agregó su entrada al final.
- No pidió aprobaciones.

## Uso explícito de AGENTS.md
- El agente escribió que agregaba una prueba "con el nombre requerido por AGENTS.md"
  (test_r3_rechaza_superposicion_parcial).