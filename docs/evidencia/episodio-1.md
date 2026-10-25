# Evidencia — Episodio 1 (LAB-5)

Extractos saneados de la sesión de Pi. La transcripción completa no se incluye en el repo;
se conserva fuera de él (pi-episodio-1.html).

## Sesión
- Pi 1.3.0 · sesión "episodio-1" · ID 01a1747e-6417-771d-be36-b3c799aac21c · 2026-10-25
- 58 mensajes (9 del autor, 30 del asistente), 18 llamadas a herramientas
- Modelos: gemini-3.6-flash (190k tokens) y gemini-3.8-flash (177k tokens). Costo estimado
  por Pi: USD 0,231, no cobrado (plan gratuito).

## Carga de AGENTS.md (antes de delegar)
- Autor: "Sin usar herramientas: ¿qué archivos de instrucciones (AGENTS.md o CLAUDE.md)
  cargaste al iniciar? Respondé solo con la ruta de cada uno."
- Pi (gemini-3.6-flash): C:\Users\<usuario>\Documents\lab-reservas_TopicosAVANZADOS\AGENTS.md

## Instrucción
- "@docs/prompts/episodio-1.md Seguí estas instrucciones."

## Intervención del autor por el límite diario
- "Continuá con la tarea. Para ahorrar pedidos al modelo: escribí cada archivo completo en una
  sola operación, no vuelvas a leer archivos que ya leíste, y ejecutá las pruebas una vez al
  final (repetí solo si fallan)."

## Acciones del agente
- write: pyproject.toml, reservas/__init__.py, reservas/inventario.py, reservas/dominio.py,
  reservas/servicio.py, tests/test_dominio.py
- bash: .venv/Scripts/python -m pytest -q → "7 passed in 0.11s"
- edit: docs/PROGRESO.md (agregó su entrada y borró una del autor; restaurada)
- Engram: search "episodio 1 dominio validaciones" (0 resultados); save (memoria #1)

## Errores del proveedor
- 429, gemini-3.6-flash: límite de 5 pedidos por minuto del plan gratuito.
- Respuesta cortada: "Error: Incomplete JSON segment at the end".
- 503 UNAVAILABLE: "This model is currently experiencing high demand".
- 429, gemini-3.6-flash: límite de 20 pedidos por día.
- 429, gemini-3.8-flash: límite de 20 pedidos por día (17:06). Con gemini-3.7-flash y
  gemini-3.5-flash, rechazados con las cuotas de 3.8 y 3.6.