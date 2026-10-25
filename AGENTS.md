# Instrucciones para el agente

## Proyecto
App de consola para reservar unidades de equipos de laboratorio.
La fuente de verdad es docs/especificacion.md. Si algo no está especificado, no lo
inventes: cerrá la tarea con una sección "Dudas" proponiendo la decisión.
Estas instrucciones las usan Pi (episodio 1) y Codex (episodios 2 y 3).

## Entorno
- Windows. Entorno virtual en .venv.
- Pruebas en Git Bash: .venv/Scripts/python -m pytest -q
- Pruebas en PowerShell: .venv\Scripts\python -m pytest -q

## Stack
- Python 3.12+. En ejecución, solo biblioteca estándar (sqlite3, argparse, datetime, json).
- pytest ya está instalado (versión fijada en requirements-dev.txt). No agregues dependencias.
- Código en el paquete reservas/ en la raíz: `python -m reservas` debe funcionar desde la
  raíz sin instalar nada. Pruebas en tests/.

## Reglas de dominio
1. Intervalos semiabiertos [inicio, fin). Hay superposición si
   a.inicio < b.fin and b.inicio < a.fin. Turnos consecutivos (a.fin == b.inicio)
   NO se superponen y deben aceptarse.
2. Solo bloquean las reservas ACTIVA. Una CANCELADA nunca bloquea.
3. Validación y superposición viven en UNA función de dominio que usan reservar y
   disponibilidad. No dupliques esa lógica.
4. Hora fija UTC−03:00, formato AAAA-MM-DD HH:MM. El dominio no llama a
   datetime.now(): recibe un reloj inyectable.
5. Cancelar = estado CANCELADA + cancelada_en. Nunca borres filas de reservas.

## Procedimiento de persistencia
- SQLite en la ruta de --db o RESERVAS_DB; por defecto data/reservas.db.
- Esquema con CREATE TABLE IF NOT EXISTS. Iniciar la app nunca borra ni recrea datos.
- Verificar superposición e insertar en la misma transacción (BEGIN IMMEDIATE).
- Pruebas de persistencia con base temporal (tmp_path), reabriendo con una instancia
  nueva; la prueba de reinicio ejecuta la consola en procesos separados (subprocess).

## Pruebas
- Nombre con el requisito: test_r3_rechaza_superposicion_parcial. CA en el docstring.
- Dominio y persistencia: reloj fijo 2026-11-01 08:00 -03:00, inyectado.
- Consola por subprocess: fechas de 2099, para no depender del día de ejecución.
- Antes de terminar, ejecutá las pruebas y copiá el resumen real.
  Si no pudiste ejecutarlas, decilo explícitamente.

## Límites
- No hagas git commit, push, reset, checkout ni cambies de rama: el autor revisa y commitea.
- No modifiques docs/especificacion.md, docs/decisiones.md, docs/prompts/ ni este archivo;
  proponé los cambios en tu respuesta.
- No instales nada ni uses la red.
- Solo creás o modificás archivos en reservas/, tests/, pyproject.toml y docs/PROGRESO.md.
  No crees documentos de tarea, planes ni archivos auxiliares fuera de esas rutas.
- Si tenés herramientas de memoria (Engram), podés usarlas, pero el registro oficial del
  progreso es docs/PROGRESO.md.

## Uso eficiente del modelo
- Escribí cada archivo completo en una sola operación.
- No vuelvas a leer archivos que ya leíste en la misma tarea.
- Ejecutá las pruebas una vez al final; repetí solo si fallan.

## Al terminar cada tarea
Agregá AL FINAL de docs/PROGRESO.md una entrada nueva. No borres, reordenes ni modifiques
las entradas existentes, en especial las marcadas "(autor)".

### AAAA-MM-DD — <tarea> (agente)
- Archivos creados o modificados
- Requisitos cubiertos (R#)
- Comando de pruebas y resultado copiado tal cual
- Pendientes y dudas