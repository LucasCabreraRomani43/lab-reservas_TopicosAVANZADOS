# Episodio 3a — Interfaz de consola (LAB-7)

Objetivo: sección 5 de docs/especificacion.md y los criterios CA8, CA9 y CA10 en procesos
separados. Seguí AGENTS.md en todo momento.

Contexto: ya existen reservas/dominio.py, reservas/servicio.py (ServicioReservas),
reservas/persistencia.py (repositorio SQLite) y 12 pruebas que pasan. La consola no debe
repetir reglas: usa el servicio existente.

1. reservas/__main__.py y reservas/cli.py con argparse: unidades, disponibilidad,
   reservar, cancelar, listar (con --unidad opcional) y reiniciar-datos (con --confirmar);
   opción global --db y variable de entorno RESERVAS_DB; por defecto data/reservas.db.
   Códigos de salida: 0 éxito, 1 rechazo por regla o validación, 2 uso incorrecto.
2. Mensajes en español. listar muestra una línea por reserva con ID, unidad, solicitante,
   inicio, fin y estado.
3. tests/test_cli.py: ejecutar `python -m reservas` con subprocess (sys.executable, cwd en
   la raíz del repo, base de datos en tmp_path, fechas de 2099):
   - CA8: un proceso crea dos reservas, otro proceso cancela una, y un tercer proceso nuevo
     ejecuta listar y ve una ACTIVA y una CANCELADA.
   - CA9: unidades lista exactamente los 5 ID del inventario.
   - CA10: reiniciar-datos sin --confirmar no borra nada.
   - Una entrada inválida devuelve código de salida 1 y un comando mal escrito, código 2.
4. Ejecutá todas las pruebas y agregá tu entrada al final de docs/PROGRESO.md.