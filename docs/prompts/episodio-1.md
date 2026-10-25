# Episodio 1 — Dominio y validaciones (LAB-5)

Objetivo: implementar R1–R6 y R8 de docs/especificacion.md, sin base de datos ni consola.
Seguí AGENTS.md en todo momento.

1. reservas/__init__.py y reservas/inventario.py: leer data/inventario.json (R1); error
   claro si falta o es inválido.
2. reservas/dominio.py: parseo de fechas (S1, S2), modelo de reserva con estados ACTIVA y
   CANCELADA, validaciones de R6 y UNA función que decide si un intervalo es reservable
   para una unidad, dada la lista de reservas (R3, R4, R5).
3. reservas/servicio.py: reservar() y disponibilidad() (R2, R8) que usan esa función,
   con un repositorio en memoria y un reloj inyectable.
4. pyproject.toml solo con la configuración de pytest (testpaths = ["tests"],
   pythonpath = ["."]); sin dependencias nuevas.
5. tests/test_dominio.py: CA1–CA5, la carga del inventario de CA9 y CA7 para los casos
   de CA2–CA4.

No implementes SQLite, cancelación ni consola: son de los episodios siguientes.
Al terminar: ejecutá las pruebas, pegá el resumen real y agregá tu entrada en
docs/PROGRESO.md.