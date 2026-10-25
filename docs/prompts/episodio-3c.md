# Episodio 3c — Correcciones de la auditoría (LAB-7)

La auditoría en solo lectura (episodio 3b) encontró dos desvíos que el autor confirmó.
Corregí solo esto. Seguí AGENTS.md.

1. S2: reservas/dominio.py, línea 29, hace texto.strip() antes de parsear, por lo que acepta
   fechas con espacios al inicio o al final. S2 dice que cualquier otro formato se rechaza.
   Quitá ese strip para que esas entradas se rechacen y agregá una prueba test_r6_… que lo
   verifique.
2. S8: en reservas/servicio.py, RepositorioEnMemoria.reiniciar_datos vuelve _proximo_id a 1
   y permite reutilizar ID. Hacé que no lo reinicie, como el repositorio SQLite (que usa
   AUTOINCREMENT), y agregá una prueba test_r11_s8_… que lo verifique.

No cambies nada más. Ejecutá todas las pruebas y agregá tu entrada al final de
docs/PROGRESO.md.