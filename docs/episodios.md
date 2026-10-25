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



## Episodio 2 — Persistencia SQLite y cancelación (LAB-6)

| Campo | Registro |
| --- | --- |
| Objetivo y requisitos | R7, R9, R10 y R11: persistencia SQLite, cancelación, listado e reinicio de datos. |
| Contexto suministrado | AGENTS.md ajustado por D14 (Codex lo cargó: /status muestra "Agents.md: AGENTS.md"), docs/especificacion.md, el código del episodio 1 y el prompt. |
| Instrucción | docs/prompts/episodio-2.md (commit 59c8826). Extracto: "Verificación de superposición e inserción dentro de una sola transacción BEGIN IMMEDIATE, reutilizando la función de dominio existente". |
| Agente y sesión | Codex CLI 0.164.0, GPT-6-Luna (reasoning medium), plan Free; sesión 01a17519-bdb1-7d83-8e31-10ab930130e0; trabajó 49 s; límite mensual 100 % → 99 %. Permisos: Workspace (Ask for approval). |
| Acción y resultado del agente | Leyó el prompt, la especificación, PROGRESO.md, el código y AGENTS.md; editó reservas/servicio.py; creó reservas/persistencia.py y tests/test_persistencia.py; corrió las pruebas dos veces (11 y 12 passed, con una advertencia de caché); agregó su entrada al final de PROGRESO.md. No pidió aprobaciones: todo quedó dentro del modo Workspace. |
| Revisión humana | git status (solo archivos permitidos); diff de PROGRESO.md (no borró entradas del autor: regla de D14 respetada); BEGIN IMMEDIATE y función de dominio reutilizada; DELETE solo en el reinicio; sin datetime.now; pruebas propias; prueba de mutación. Detalle en docs/verificacion.md. |
| Diferencia entre lo informado y lo comprobado | El agente informó 12 passed. El autor obtuvo 7 passed y 5 errores por permisos de la carpeta temporal de pytest creada por el sandbox de Codex; con --basetemp fuera del repo, 12 passed. |
| Corrección | No hubo correcciones de código. |
| Decisión | Aceptado. Cumple R7 y R9–R11, el procedimiento de persistencia y la regla de una sola función; la diferencia en las pruebas era del entorno (permisos del sandbox), no del código. |
| Evidencia | Commit e3919cd; reservas/persistencia.py; tests/test_persistencia.py; docs/verificacion.md; docs/evidencia/episodio-2.md. |


## Episodio 3 — Consola, auditoría en solo lectura y correcciones (LAB-7)

### 3a — Interfaz de consola

| Campo | Registro |
| --- | --- |
| Objetivo y requisitos | Sección 5 de la especificación (consola) y CA8, CA9 y CA10 en procesos separados. |
| Contexto suministrado | AGENTS.md (/status: "Agents.md: AGENTS.md"), la especificación y el código de los episodios 1 y 2. |
| Instrucción | docs/prompts/episodio-3a.md (commit 4f6ff62). Extracto: "un proceso crea dos reservas, otro proceso cancela una, y un tercer proceso nuevo ejecuta listar". |
| Agente y sesión | Codex CLI 0.164.0, GPT-6-Luna; sesión 01a17535-ab83-7121-ac3d-e421e0679d9f; 55 s; modo Workspace (Ask for approval); no pidió aprobaciones. |
| Acción y resultado del agente | Creó reservas/__main__.py, reservas/cli.py y tests/test_cli.py; tras la primera ejecución releyó CA8 y ajustó la prueba para que las dos reservas se creen en el mismo proceso; informó 17 passed; agregó su entrada en PROGRESO.md. |
| Revisión humana | 17 passed propias; datetime.now solo en cli.py:73 (fuera del dominio); prueba manual de la consola con códigos de salida 0, 1 y 2; PROGRESO.md sin borrados. |
| Corrección | Las 5 pruebas nuevas no empezaban con test_r…, como pide AGENTS.md. El autor se lo pidió al agente en la misma sesión y Codex las renombró; 17 passed. |
| Decisión | Aceptado con corrección. |
| Evidencia | Commit 3346f5c; tests/test_cli.py; docs/verificacion.md; docs/evidencia/episodio-3.md. |

### 3b — Auditoría de cobertura en solo lectura

| Campo | Registro |
| --- | --- |
| Objetivo | Contrastar la especificación y AGENTS.md con las pruebas y el código, sin modificar archivos. |
| Instrucción | docs/prompts/episodio-3b.md (commit 8a2fd0d). |
| Agente y sesión | Codex con --sandbox read-only --ask-for-approval never; /status: "Permissions: Read Only (never)"; sesión 01a17545-7d05-70b2-a5c8-79e609e2d866; 21 s. |
| Resultado del agente | CA1 a CA10 con cobertura. Tres hallazgos: S2 (acepta fechas con espacios externos), S8 (el repositorio en memoria reutiliza ID tras reiniciar) y regla 3 (validación repartida en dos funciones). |
| Revisión humana | git status limpio tras la auditoría; S2 confirmado con python -c; S8 confirmado solo en el repositorio en memoria (en la consola con SQLite el ID siguiente fue 2, por AUTOINCREMENT); regla 3 confirmada en la forma y sin impacto. |
| Decisión | Corregir S2 y S8 (parte 3c); mantener la regla 3 como está (D15). |
| Evidencia | docs/evidencia/episodio-3.md; docs/verificacion.md. |

### 3c — Correcciones de la auditoría

| Campo | Registro |
| --- | --- |
| Instrucción | docs/prompts/episodio-3c.md (commit b5bc6fb). |
| Agente y sesión | Codex, modo Workspace (Ask for approval); sesión 01a1754c-d883-70a1-95d9-79184adf72f9; aprobaciones: no se registró. |
| Acción y resultado del agente | Quitó el strip de parsear_fecha; el repositorio en memoria ya no reinicia el contador de ID; agregó test_r6_rechaza_fechas_con_espacios_externos y test_r11_s8_reinicio_memoria_no_reutiliza_id; agregó su entrada en PROGRESO.md. |
| Revisión humana | 19 passed propias; la fecha con espacios ahora da ErrorDominio; PROGRESO.md con +17 y sin borrados. |
| Decisión | Aceptado. |
| Evidencia | Commit 5b9cf8d; tests/test_dominio.py; docs/verificacion.md. |