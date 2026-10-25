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



## 2026-10-25 — Cierre del episodio 1 (autor)
- Prueba de mutación en dominio.py:131: detectada por test_r4 (ver docs/verificacion.md).
- Registro en docs/episodios.md y extractos en docs/evidencia/episodio-1.md; nueva decisión D12.
- Decisión: episodio 1 aceptado con correcciones.


## 2026-10-25 — Cambio de agente para los episodios 2 y 3 (autor)
- Pruebas en carpetas descartables: DeepSeek → 402 "Insufficient Balance"; Mistral
  (Experiment) → 429 "Rate limit exceeded" en el primer pedido; gemini-3.1-pro → 429 con
  límite 0 en el plan gratuito. Se consideró Ollama (local) sin llegar a probarlo.
- Codex CLI 0.164.0 instalado con npm e iniciado con la cuenta de ChatGPT (plan Free); creó
  un archivo de prueba en una carpeta descartable.
- En el repo, Codex respondió que cargó
  C:\Users\<usuario>\Documents\lab-reservas_TopicosAVANZADOS\AGENTS.md, y /status mostró:
  modelo GPT-6-Luna (reasoning medium), Permissions: Workspace (Ask for approval),
  Agents.md: AGENTS.md, plan Free con límite mensual al 100 %.
- El primer /status se escribió como mensaje y Codex empezó a revisar el repo; se interrumpió
  y git status siguió limpio.
- Decisiones D13 (cambio de agente) y D14 (ajustes de AGENTS.md).

## 2026-10-25 — Episodio 2: Persistencia SQLite y cancelación (agente)
- Archivos creados o modificados:
  - `reservas/persistencia.py`
  - `reservas/servicio.py`
  - `tests/test_persistencia.py`
  - `docs/PROGRESO.md`
- Requisitos cubiertos (R#):
  - R7: Cancelar conserva los datos, registra `cancelada_en`, rechaza cancelaciones inválidas y libera el intervalo.
  - R9: SQLite mantiene reservas al abrir instancias nuevas; alta con verificación e inserción en `BEGIN IMMEDIATE`.
  - R10: El servicio lista todas las reservas o filtra por unidad, ordenando por inicio.
  - R11: El reinicio solo borra datos con `confirmar=True`.
- Comando de pruebas y resultado copiado tal cual:
  ```
  .venv\Scripts\python -m pytest -q
  ............                                                             [100%]
  =============================== warnings summary ===============================
  .venv\Lib\site-packages\_pytest\cacheprovider.py:469
    C:\Users\Usuario\Documents\lab-reservas_TopicosAVANZADOS\.venv\Lib\site-packages\_pytest\cacheprovider.py:469: PytestCacheWarning: could not create cache path C:\Users\Usuario\Documents\lab-reservas_TopicosAVANZADOS\.pytest_cache\v\cache\nodeids: [WinError 183] No se puede crear un archivo que ya existe: 'C:\\Users\\Usuario\\Documents\\lab-reservas_TopicosAVANZADOS\\.pytest_cache\\v\\cache'
      config.cache.set("cache/nodeids", sorted(self.cached_nodeids))

  -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
  12 passed, 1 warning in 0.13s
  ```
- Pendientes y dudas:
  - El repositorio SQLite recibe su ruta y queda listo para que la consola lo conecte en el episodio 3.
  - Pytest informó una advertencia de caché `.pytest_cache` (WinError 183); las 12 pruebas pasaron.


## 2026-10-25 — Revisión y cierre del episodio 2 (autor)
- Agente: Codex CLI 0.164.0 (GPT-6-Luna), sesión 01a17519-bdb1-7d83-8e31-10ab930130e0;
  trabajó 49 s; límite mensual 100 % → 99 %; no pidió aprobaciones.
- Revisión: solo tocó archivos permitidos; respetó la regla de D14 en este archivo;
  BEGIN IMMEDIATE con la función de dominio reutilizada; DELETE solo en el reinicio.
- Pruebas del autor: 7 passed y 5 errores por permisos de la carpeta temporal de pytest
  creada por el sandbox de Codex; con --basetemp=../pytest-tmp-lab, 12 passed.
- Prueba de mutación en dominio.py:129: detectada por test_r7_ca6.
- Decisión: episodio 2 aceptado sin correcciones de código (commit e3919cd).

## 2026-10-25 — Episodio 3a: Interfaz de consola (agente)
- Archivos creados o modificados:
  - `reservas/cli.py`
  - `reservas/__main__.py`
  - `tests/test_cli.py`
  - `docs/PROGRESO.md`
- Requisitos cubiertos (R#):
  - R1: `unidades` lista el inventario cargado desde `data/inventario.json`.
  - R7: `cancelar` actualiza la reserva usando el servicio existente.
  - R8: `disponibilidad` delega validación y conflictos al servicio de dominio.
  - R9: persistencia SQLite seleccionable con `--db`, `RESERVAS_DB` o la ruta predeterminada.
  - R10: `listar` muestra reservas activas y canceladas, con filtro opcional por unidad.
  - R11: `reiniciar-datos` solo borra reservas con `--confirmar`.
- Criterios cubiertos: CA8, CA9 y CA10; también códigos de salida 1 para entrada inválida y 2 para comando desconocido.
- Comando de pruebas y resultado copiado tal cual:
  ```
  .venv\Scripts\python -m pytest -q
  .................                                                        [100%]
  =============================== warnings summary ===============================
  .venv\Lib\site-packages\_pytest\cacheprovider.py:469
    C:\Users\Usuario\Documents\lab-reservas_TopicosAVANZADOS\.venv\Lib\site-packages\_pytest\cacheprovider.py:469: PytestCacheWarning: could not create cache path C:\Users\Usuario\Documents\lab-reservas_TopicosAVANZADOS\.pytest_cache\v\cache\nodeids: [WinError 183] No se puede crear un archivo que ya existe: 'C:\\Users\\Usuario\\Documents\\lab-reservas_TopicosAVANZADOS\\.pytest_cache\\v\\cache'
      config.cache.set("cache/nodeids", sorted(self.cached_nodeids))

  -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
  17 passed, 1 warning in 1.09s
  ```
- Pendientes y dudas:
  - Ninguna duda funcional del episodio. Pytest pasó; permanece la advertencia de caché `.pytest_cache` (WinError 183).

## 2026-10-25 — Convención de nombres de pruebas CLI (agente)
- Archivos modificados: `tests/test_cli.py`, `docs/PROGRESO.md`.
- Corrección: nombres con `test_r<n>_` y CA correspondiente conservada en el nombre.
- Pruebas: `.venv\Scripts\python -m pytest -q`
  ```
  .................                                                        [100%]
  =============================== warnings summary ===============================
  .venv\Lib\site-packages\_pytest\cacheprovider.py:469
    C:\Users\Usuario\Documents\lab-reservas_TopicosAVANZADOS\.venv\Lib\site-packages\_pytest\cacheprovider.py:469: PytestCacheWarning: could not create cache path C:\Users\Usuario\Documents\lab-reservas_TopicosAVANZADOS\.pytest_cache\v\cache\nodeids: [WinError 183] No se puede crear un archivo que ya existe: 'C:\\Users\\Usuario\\Documents\\lab-reservas_TopicosAVANZADOS\\.pytest_cache\\v\\cache'
      config.cache.set("cache/nodeids", sorted(self.cached_nodeids))

  -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
  17 passed, 1 warning in 1.09s
  ```

## 2026-10-25 — Episodio 3c: Correcciones de auditoría (agente)
- Archivos creados o modificados: `reservas/dominio.py`, `reservas/servicio.py`, `tests/test_dominio.py`, `docs/PROGRESO.md`.
- Requisitos cubiertos: S2 (rechazo de fechas con espacios externos), S8 (IDs en memoria no reutilizados tras reiniciar datos); pruebas asociadas a R6 y R11.
- Comando de pruebas y resultado copiado tal cual:
  ```
  .venv\Scripts\python -m pytest -q
  ...................                                                      [100%]
  =============================== warnings summary ===============================
  .venv\Lib\site-packages\_pytest\cacheprovider.py:469
    C:\Users\Usuario\Documents\lab-reservas_TopicosAVANZADOS\.venv\Lib\site-packages\_pytest\cacheprovider.py:469: PytestCacheWarning: could not create cache path C:\Users\Usuario\Documents\lab-reservas_TopicosAVANZADOS\.pytest_cache\v\cache\nodeids: [WinError 183] No se puede crear un archivo que ya existe: 'C:\\Users\\Usuario\\Documents\\lab-reservas_TopicosAVANZADOS\\.pytest_cache\\v\\cache'
      config.cache.set("cache/nodeids", sorted(self.cached_nodeids))

  -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
  19 passed, 1 warning in 1.07s
  ```
- Pendientes y dudas: ninguna. Permanece el aviso de caché `.pytest_cache` de pytest (WinError 183).


## 2026-10-25 — Revisión y cierre del episodio 3 (autor)
- 3a (Codex, sesión 01a17535-…): consola y pruebas entre procesos. El autor pidió renombrar 5
  pruebas sin número de requisito y el agente lo corrigió en la misma sesión (commit 3346f5c).
- 3b (Codex en solo lectura, sesión 01a17545-…): CA1 a CA10 cubiertos y tres hallazgos;
  git status limpio después.
- Verificación del autor: S2 confirmado; S8 confirmado solo en el repositorio en memoria
  (SQLite no reutiliza ID); regla 3 confirmada en la forma, sin impacto (D15).
- 3c (Codex, sesión 01a1754c-…): S2 y S8 corregidos (commit 5b9cf8d); 19 passed del autor.
- Decisión: episodio 3 aceptado.


## 2026-10-25 — Verificación final (autor)
- Clon limpio del commit b66d5b8: instalación con requirements-dev.txt y 19 passed
  (Python 3.15.0, pytest 9.1.1), sin usar ninguna cuenta de modelo.
- Persistencia tras reiniciar comprobada con la consola: se conservaron las reservas activas
  y canceladas, y la cancelada liberó el horario. Detalle en docs/verificacion.md.
- Próximo: README en cuatro secciones y revisión contra la rúbrica.