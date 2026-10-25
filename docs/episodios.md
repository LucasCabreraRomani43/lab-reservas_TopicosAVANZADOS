# Episodios de delegación

Cada episodio registra: objetivo y requisitos → contexto e instrucción → acción del agente →
revisión y decisión humana → evidencia verificable.

## Episodio 1 — Dominio y validaciones (LAB-5)

| Campo | Registro |
| --- | --- |
| Objetivo y requisitos | Implementar R1–R6 y R8 (inventario, validaciones, superposición y disponibilidad), sin base de datos ni consola. |
| Contexto suministrado | AGENTS.md (Pi confirmó haberlo cargado, ver docs/evidencia/episodio-1.md), docs/especificacion.md (tag spec-v1), data/inventario.json y el prompt del episodio. |
| Instrucción | docs/prompts/episodio-1.md (commit fb73ab0). Extracto: "UNA función que decide si un intervalo es reservable para una unidad, dada la lista de reservas (R3, R4, R5)". |
| Intervención del autor | Al agotarse el cupo diario de gemini-3.6-flash, cambio a gemini-3.8-flash y pedido de ahorrar llamadas ("escribí cada archivo completo en una sola operación…"). |
| Sesión | Pi 1.3.0, sesión "episodio-1" (ID 01a1747e-6417-771d-be36-b3c799aac21c): 9 mensajes del autor, 18 llamadas a herramientas, modelos gemini-3.6-flash y gemini-3.8-flash. |
| Acción y resultado del agente | Creó pyproject.toml, reservas/__init__.py, inventario.py, dominio.py, servicio.py y tests/test_dominio.py; informó "7 passed"; agregó su entrada en PROGRESO.md; guardó una memoria en Engram. |
| Revisión humana | git status y diff (solo archivos permitidos, sin commits); grep sin datetime.now en reservas/; una sola función de superposición usada por reservar y disponibilidad; lectura de test_r3 y test_r6; pytest -v propio (7 passed); prueba de mutación. Detalle en docs/verificacion.md. |
| Corrección | (1) Borró la entrada "Corrección antes del episodio 1" de PROGRESO.md en vez de agregar al final; (2) agregó [build-system] a pyproject.toml sin que se pidiera; (3) una prueba sin número de requisito. Se pidió al agente corregir (2) y (3), pero no había cupo diario en ningún modelo Flash; el autor aplicó las tres correcciones a mano. |
| Decisión | Aceptado con correcciones. Las reglas de dominio, las validaciones y las pruebas cumplen la especificación y AGENTS.md; los desvíos eran de forma y quedaron corregidos. |
| Evidencia | Commit c4f4724 ("feat(dominio): validaciones y regla de superposición (episodio 1, LAB-5)"); tests/test_dominio.py; reservas/dominio.py línea 131; docs/verificacion.md; docs/evidencia/episodio-1.md. |