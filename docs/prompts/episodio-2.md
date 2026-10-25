# Episodio 2 — Persistencia SQLite y cancelación (LAB-6)

Objetivo: R7, R9, R10 y R11 de docs/especificacion.md. Seguí AGENTS.md en todo momento.

Contexto: el episodio 1 dejó reservas/dominio.py (verificar_superposicion_y_disponibilidad),
reservas/servicio.py (ServicioReservas y RepositorioEnMemoria) y tests/test_dominio.py
(7 pruebas que pasan). No cambies la regla de superposición ni rompas esas pruebas.

1. reservas/persistencia.py: repositorio SQLite con la misma interfaz que
   RepositorioEnMemoria. Esquema con CREATE TABLE IF NOT EXISTS (id, unidad, solicitante,
   inicio, fin, estado, creada_en, cancelada_en). Recibe la ruta de la base como parámetro
   (la consola la tomará de --db o RESERVAS_DB en el episodio 3).
2. Verificación de superposición e inserción dentro de una sola transacción
   BEGIN IMMEDIATE, reutilizando la función de dominio existente.
3. En el servicio: cancelar(id) (R7), listar(unidad=None) ordenado por inicio (R10) y
   reiniciar_datos(confirmar) (R11).
4. tests/test_persistencia.py: CA6; CA8 reabriendo una instancia nueva sobre el mismo
   archivo en tmp_path; CA10; y que abrir una base existente no borre datos (R9).
5. Ejecutá todas las pruebas (las 7 del episodio 1 y las nuevas) y agregá tu entrada
   al final de docs/PROGRESO.md.