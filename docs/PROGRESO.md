# Progreso

Registro cronológico del trabajo. Cada entrada indica quién la escribió: el autor o el
agente (Pi, según la sección "Al terminar cada tarea" de AGENTS.md).

## 2026-10-20 — Preparación del entorno (autor)
- Instalados: Git 2.56.0.windows.2, Python 3.15.0 (Python install manager), Node.js 24.22.0,
  npm 11.19.1, Pi 1.3.0.
- Proveedor del modelo: API key de Google AI Studio en plan gratuito; modelo elegido
  gemini-3.8-flash. Prueba en carpeta descartable: Pi creó un archivo con la herramienta write
  y ejecutó un comando con Git Bash.
- Herramientas complementarias: Engram 3.5.1 conectado a Pi con `engram setup pi`
  (paquete gentle-engram 0.5.0); Linear con issues LAB-5, LAB-6 y LAB-7, uno por episodio.
- Gentle AI: la primera instalación de gentle-pi 4.3.0 falló con
  GENTLE_AI_GO_TOOLCHAIN_UNAVAILABLE (en Windows compila desde el código fuente y requiere Go).
  Se instaló Go 1.27.3 y la segunda instalación funcionó.
- Problema observado: `gentle-shell --link` se cierra al iniciar en la terminal de VS Code y
  en Git Bash; funciona desde PowerShell.
- Problema observado: después de usar Gentle Shell, el modelo por defecto apareció como
  gemini-3.1-pro-preview; se volvió a elegir gemini-3.8-flash con /model.

## 2026-10-25 — Repositorio y especificación v1 (autor)
- Repo creado en GitHub (lab-reservas_TopicosAVANZADOS). Commits 08b12f3 (estructura inicial
  e inventario) y 70c9f1c (dependencias de desarrollo: pytest 9.1.1 fijado en
  requirements-dev.txt).
- Escritos docs/especificacion.md, AGENTS.md, docs/decisiones.md (D1–D10), este archivo y
  docs/agente.md. El borrador lo preparé con ayuda de Claude en un chat y lo revisé yo;
  decidí mantener los supuestos S4, S5 y S9 como están (ver D6).
- Pendiente: decidir si los episodios se hacen con Pi normal o con Gentle Shell (D10).
- Próximo: Episodio 1 (LAB-5), dominio y validaciones con pruebas.

## 2026-10-25 — Prueba de permisos de Gentle Shell y elección del modelo (autor)
- Con gemini-3.8-flash y gemini-3.7-flash, Gentle Shell devolvió error 503 UNAVAILABLE
  ("model is currently experiencing high demand"), 3 reintentos automáticos cada vez, en
  dos intentos separados por 10 minutos.
- Con gemini-3.6-flash funcionó: creó hola.txt en una carpeta descartable sin pedir
  aprobación, en modo NORMAL ("Risk: none").
- Decisiones: los episodios se hacen con Pi normal (D10) y con gemini-3.6-flash (D11).

## 2026-10-25 — Corrección antes del episodio 1 (autor)
- Al abrir Pi para el episodio 1, el inicio no mostraba AGENTS.md. Con `git ls-files`
  comprobé que no estaba versionado: se había creado dentro de .atl/ (carpeta de registro de
  skills que generó Gentle AI al abrir gentle-shell en el repo), cuyo propio .gitignore lo
  ocultaba. Por eso no está en el commit spec-v1. Además, .gitignore había quedado en
  docs/.gitignore, donde no aplicaba a data/*.db.
- Corrección: AGENTS.md movido a la raíz (sin cambios de contenido) y .gitignore movido a la
  raíz. Se dejó .atl/ (registro de skills de Gentle AI, ignorado por su propio .gitignore).
  Se borró una carpeta `$HOME` vacía creada por error al ejecutar un comando de PowerShell en
  otra terminal. Desde ahora Gentle Shell no se abre dentro del proyecto.
- No se delegó ninguna tarea a Pi antes de la corrección.

## 2026-10-25 — Episodio 1: Dominio y validaciones (agente)
- Archivos creados o modificados:
  - `pyproject.toml`
  - `reservas/__init__.py`
  - `reservas/inventario.py`
  - `reservas/dominio.py`
  - `reservas/servicio.py`
  - `tests/test_dominio.py`
  - `docs/PROGRESO.md`
- Requisitos cubiertos (R#):
  - R1: Lectura de unidades de `data/inventario.json`, manejo de errores si falta o es inválido.
  - R2: Creación de reserva con ID nuevo, estado ACTIVA, unidad, solicitante, inicio, fin y creada_en.
  - R3: Rechazo por superposición parcial, total o idéntica en intervalos semiabiertos [inicio, fin).
  - R4: Aceptación de reservas consecutivas de la misma unidad (a.fin == b.inicio).
  - R5: Aceptación de reservas simultáneas de distintas unidades.
  - R6: Validación de unidad conocida, solicitante no vacío, fechas válidas, inicio < fin, inicio no en el pasado.
  - R8: Disponibilidad con la misma lógica de validación y superposición que reservar.
- Comando de pruebas y resultado copiado tal cual:
  ```
  $ .venv/Scripts/python -m pytest -q
  .......                                                                  [100%]
  7 passed in 0.11s
  ```
- Pendientes y dudas:
  - Ninguna duda sobre el alcance de este episodio.
  - Pendientes para los próximos episodios: persistencia SQLite (R9, R11, LAB-6), cancelación (R7) e interfaz de consola por argparse (R10, LAB-7).


  
## 2026-10-25 — Revisión del episodio 1 (autor)
- Revisión: solo cambiaron reservas/, tests/, pyproject.toml y docs/PROGRESO.md; sin commits
  ni cambios de rama; sin datetime.now en reservas/; reservar y disponibilidad usan
  verificar_superposicion_y_disponibilidad (servicio.py, líneas 80 y 113); condición de
  superposición en dominio.py, línea 131. Pruebas ejecutadas por el autor: 7 passed
  (Python 3.15.0, pytest 9.1.1).
- Desvíos encontrados: (1) el agente borró la entrada "Corrección antes del episodio 1" en
  lugar de agregar al final; restaurada por el autor. (2) pyproject.toml con [build-system],
  que no se pidió. (3) prueba test_solicitante_con_espacios_al_inicio_y_final_se_limpia sin
  número de requisito.
- Se pidió al agente corregir (2) y (3), pero no hubo cupo: 429 diario en gemini-3.8-flash
  (17:06); con gemini-3.7-flash el pedido se rechazó con la cuota de gemini-3.8-flash y con
  gemini-3.5-flash, con la de gemini-3.6-flash (17:08–17:09). El autor aplicó (2) y (3) a mano.
- Límites del día: 429 por minuto (5 pedidos) y diario (20 pedidos) en gemini-3.6-flash entre
  las 16:25 y las 16:30; una respuesta llegó cortada ("Incomplete JSON segment at the end").
- Pendiente: prueba de mutación y registro del episodio en docs/episodios.md.