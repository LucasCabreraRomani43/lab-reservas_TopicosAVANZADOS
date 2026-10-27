# Retrospectiva

## Qué se hizo
- Tres episodios de delegación: Pi + Gemini (1) y Codex (2 y 3), con 19 pruebas al momento
  de la entrega y verificación humana en cada uno.

## Qué funcionó
- Commitear el prompt antes de cada tarea dejó trazado qué recibió el agente.
- Las pruebas de mutación demostraron que las pruebas protegen las reglas clave.
- Ajustar AGENTS.md después del episodio 1 (D14) cambió el comportamiento del agente.
- funciono la mayoria de cosas

## Qué no funcionó
- El plan gratuito de Gemini (20 pedidos diarios por modelo) cortó el episodio 1.
- El sandbox de Codex dejó la carpeta temporal de pytest con permisos que el usuario no podía
  leer, y eso generó una diferencia entre lo informado y lo comprobado.
- AGENTS.md quedó guardado en una carpeta equivocada (.atl/) y no entró en spec-v1.
- hubo algunas fallas en algunos test

## Pi frente a Codex
- bastante veloz para las tareas en 20-40 segundos realizaba los test

