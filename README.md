# Reservas de equipos del laboratorio

Aplicación de consola en Python para consultar disponibilidad, reservar y cancelar unidades
de equipos de un laboratorio sin perder el historial. La construyeron agentes de programación
bajo revisión humana: Pi en el episodio 1 y Codex en los episodios 2 y 3.

<<<<<<< HEAD
=======
![Pruebas](https://github.com/LucasCabreraRomani43/lab-reservas_TopicosAVANZADOS/actions/workflows/pruebas.yml/badge.svg)
>>>>>>> c0df6b8 (docs: insignia del estado de las pruebas en el README (posterior a la entrega))

## 1. Especificación

**Problema.** La coordinación de un laboratorio registraba pedidos en mensajes y una planilla:
se confirmaban unidades para horarios superpuestos y algunas cancelaciones seguían bloqueando
el horario.

**Alcance.** Lectura del inventario precargado, consulta de disponibilidad por unidad e
intervalo, creación y cancelación de reservas, historial y persistencia local. Fuera de
alcance: administración del inventario, autenticación, notificaciones, pagos, integraciones,
interfaz gráfica y concurrencia entre procesos.

**Reglas principales**
- Intervalos semiabiertos [inicio, fin): los turnos consecutivos se aceptan.
- Solo las reservas ACTIVA bloquean; una CANCELADA libera el horario y conserva sus datos.
- Se rechazan: unidad desconocida, solicitante vacío o solo espacios, fechas inválidas,
  inicio igual o posterior al fin, e inicio en el pasado.
- La disponibilidad usa las mismas reglas que la reserva.

**Supuestos:** hora de Argentina UTC−03:00 fija; formato `AAAA-MM-DD HH:MM`; sin límites de
duración ni anticipación; los ID nunca se reutilizan; un solo proceso a la vez.

**Detalle completo:** requisitos R1–R11, supuestos S1–S10 y criterios de aceptación CA1–CA10
en [docs/especificacion.md](docs/especificacion.md).

**Evolución.** La versión inicial es el tag `spec-v1` (commit 1ea943c). La especificación no
cambió después; los ajustes posteriores (instrucciones del agente, modelos, agentes y
hallazgos de la auditoría) están en [docs/decisiones.md](docs/decisiones.md), D1 a D15.

## 2. Solución

### Estructura
```text
reservas/              paquete de la aplicación
  dominio.py           fechas, validaciones y regla de superposición
  servicio.py          casos de uso y repositorio en memoria (para pruebas)
  persistencia.py      repositorio SQLite
  inventario.py        lectura de data/inventario.json
  cli.py, __main__.py  interfaz de consola
tests/                 pruebas automáticas (dominio, persistencia y consola)
data/inventario.json   inventario precargado
docs/                  especificación, decisiones, episodios, verificación y evidencia
AGENTS.md              instrucciones para los agentes
```

### Decisiones técnicas
Python con biblioteca estándar (D2), SQLite local con verificación e inserción en una sola
transacción `BEGIN IMMEDIATE` (D3), hora UTC−03:00 fija (D4) y una única función de dominio
para la superposición (D5). Ver [docs/decisiones.md](docs/decisiones.md).

### Requisitos previos y versiones
- Python 3.12 o superior (probado con 3.15.0) y Git.
- Única dependencia: pytest 9.1.1, fijada con sus dependencias en `requirements-dev.txt`.
- No hace falta ninguna cuenta de modelo de IA.

### Instalación
```bash
git clone https://github.com/LucasCabreraRomani43/lab-reservas_TopicosAVANZADOS.git
cd lab-reservas_TopicosAVANZADOS
python -m venv .venv
source .venv/Scripts/activate        # Windows, Git Bash
# .venv\Scripts\Activate.ps1         # Windows, PowerShell
# source .venv/bin/activate          # Linux o macOS
python -m pip install -r requirements-dev.txt
```

### Datos
- **Carga inicial:** el inventario de 5 unidades está precargado en `data/inventario.json`
  y se lee en cada ejecución.
- **Dónde persisten las reservas:** en `data/reservas.db` (SQLite), o en la ruta indicada con
  `--db` o con la variable `RESERVAS_DB`. Se crea sola y no se versiona.
- **Reinicio de datos:** `python -m reservas reiniciar-datos --confirmar`.
  **Atención: borra todas las reservas**, activas y canceladas. Sin `--confirmar` no borra
  nada. Los ID nuevos continúan la numeración. Para empezar desde cero también se puede
  borrar el archivo `data/reservas.db`.

### Comandos
```bash
python -m reservas unidades
python -m reservas disponibilidad --unidad MIC-01 --inicio "2099-11-03 10:00" --fin "2099-11-03 11:00"
python -m reservas reservar --unidad MIC-01 --solicitante "Ana Pérez" --inicio "2099-11-03 10:00" --fin "2099-11-03 11:00"
python -m reservas cancelar --id 1
python -m reservas listar
python -m reservas listar --unidad MIC-01
python -m reservas reiniciar-datos --confirmar
python -m reservas --db otra-base.db listar
```
Códigos de salida: 0 éxito, 1 rechazo por regla o validación, 2 uso incorrecto.

### Ejemplo de entrada y salida
Salida real de la verificación final ([docs/verificacion.md](docs/verificacion.md)):

```text
$ python -m reservas reservar --unidad MIC-01 --solicitante "Ana Pérez" --inicio "2099-11-03 10:00" --fin "2099-11-03 11:00"
Reserva creada con ID 1.
$ python -m reservas reservar --unidad MIC-01 --solicitante "Bruno Díaz" --inicio "2099-11-03 11:00" --fin "2099-11-03 12:00"
Reserva creada con ID 2.
$ python -m reservas cancelar --id 2
Reserva 2 cancelada.
$ python -m reservas disponibilidad --unidad MIC-01 --inicio "2099-11-03 10:30" --fin "2099-11-03 11:30"
La unidad no está disponible. Reservas en conflicto:
ID: 1 | Unidad: MIC-01 | Solicitante: Ana Pérez | Inicio: 2099-11-03 10:00 | Fin: 2099-11-03 11:00 | Estado: ACTIVA
$ python -m reservas listar
ID: 1 | Unidad: MIC-01 | Solicitante: Ana Pérez | Inicio: 2099-11-03 10:00 | Fin: 2099-11-03 11:00 | Estado: ACTIVA
ID: 2 | Unidad: MIC-01 | Solicitante: Bruno Díaz | Inicio: 2099-11-03 11:00 | Fin: 2099-11-03 12:00 | Estado: CANCELADA
```

### Pruebas
```bash
python -m pytest -v
```
Resultado en un clon limpio: **19 passed** (Python 3.15.0, pytest 9.1.1). Cubren creación
válida, superposiciones, turnos consecutivos, unidades distintas simultáneas, entradas
inválidas, cancelación que conserva el registro y libera el horario, y persistencia entre
procesos. Detalle, pruebas de mutación y procedimiento manual de reinicio en
[docs/verificacion.md](docs/verificacion.md).

En el equipo del autor, el sandbox de Codex dejó la carpeta temporal de pytest con permisos
que el usuario no puede leer, por lo que allí se usa
`python -m pytest -v --basetemp=../pytest-tmp-lab`. En otro equipo no hace falta.

### Pendientes y limitaciones
- Un solo proceso a la vez (S10); no hay concurrencia entre procesos ni equipos.
- Hora fija UTC−03:00 (D4); si cambiara la política horaria habría que usar `zoneinfo`.
- Sin límites de duración ni de anticipación (S5), y se puede cancelar una reserva activa
  aunque ya haya pasado (S9).
- Las pruebas de consola usan fechas de 2099 (D7); el rechazo de fechas pasadas se prueba en
  el dominio.
- `reservar` valida con dos funciones del dominio antes de verificar la superposición: la
  regla de una sola función se cumple en su objetivo, pero no en su letra (D15).
- R10 (orden por inicio y filtro por unidad) no tiene una prueba automática dedicada; se
  verificó a mano (docs/verificacion.md).

## 3. Preparación del agente

| | Episodio 1 | Episodios 2 y 3 |
| --- | --- | --- |
| Agente (harness) | Pi 1.3.0 | Codex CLI 0.164.0 |
| Modelo | gemini-3.6-flash y gemini-3.8-flash (API de Gemini, plan gratuito) | GPT-6-Luna, reasoning medium (ChatGPT, plan Free) |
| Permisos | Herramientas por defecto (read, bash, edit, write); sin aprobaciones | Workspace (Ask for approval); auditoría 3b en Read Only (never) |
| Instrucciones | [AGENTS.md](AGENTS.md), cargado automáticamente | El mismo AGENTS.md, leído de forma nativa |

- **Por qué cambió el agente:** el plan gratuito de Gemini cortó el episodio 1 por su límite
  diario; se probaron DeepSeek, Mistral y Codex (D11 a D13).
- **Contexto suministrado:** AGENTS.md, la especificación, el inventario y un prompt por
  episodio ([docs/prompts/](docs/prompts/)). Excluido: credenciales, `.venv`, bases de datos
  y conversaciones completas. El borrador de la especificación y de AGENTS.md se preparó con
  ayuda de Claude en un chat y lo revisó el autor.
- **Adaptación específica con evidencia:** regla de turnos consecutivos, procedimiento de
  persistencia, nombres de prueba con el requisito y, después del episodio 1, la regla de
  agregar al final de PROGRESO.md sin borrar (D14), que el agente respetó en los episodios 2
  y 3.
- **Configuración externa:** bloque `retry` de Pi en `~/.pi/agent/settings.json` (extracto en
  [docs/agente.md](docs/agente.md)).
- **Retención del progreso:** [docs/PROGRESO.md](docs/PROGRESO.md), versionado, con entradas
  del autor y del agente; Engram como memoria auxiliar en el episodio 1.

Detalle y enlaces a la evidencia en [docs/agente.md](docs/agente.md) y
[docs/evidencia/](docs/evidencia/).

## 4. Registro de decisiones y delegación

**Decisiones:** D1 a D15 en [docs/decisiones.md](docs/decisiones.md), con alternativas y
consecuencias (lenguaje, almacenamiento, zona horaria, reglas, modelos, agentes y hallazgos de
la auditoría).

**Episodios de delegación** (detalle completo en [docs/episodios.md](docs/episodios.md)):

| Episodio | Agente | Requisitos | Revisión y decisión | Commits (prompt → resultado) |
| --- | --- | --- | --- | --- |
| 1. Dominio y validaciones | Pi + Gemini | R1–R6, R8 | El agente borró una entrada del autor y se desvió en dos detalles; corregido por el autor. Mutación detectada. Aceptado con correcciones | fb73ab0 → c4f4724 |
| 2. Persistencia y cancelación | Codex | R7, R9–R11 | Sin correcciones; diferencia entre lo informado y lo comprobado por permisos del sandbox. Mutación detectada. Aceptado | 59c8826 → e3919cd |
| 3. Consola, auditoría y correcciones | Codex | Sección 5, CA8–CA10 | 3a: nombres corregidos por el agente a pedido del autor. 3b: auditoría en solo lectura, dos hallazgos confirmados. 3c: correcciones verificadas. Aceptado | 4f6ff62 → 3346f5c; 8a2fd0d; b5bc6fb → 5b9cf8d |

Verificación humana de cada episodio: [docs/verificacion.md](docs/verificacion.md). Extractos
de las sesiones: [docs/evidencia/](docs/evidencia/). Seguimiento de tareas en Linear:
[docs/evidencia/linear.md](docs/evidencia/linear.md).
