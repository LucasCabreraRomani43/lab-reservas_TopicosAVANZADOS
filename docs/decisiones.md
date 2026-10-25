# Registro de decisiones

Formato: decisión → alternativas → motivo → consecuencias.
Las decisiones D1 a D10 son las iniciales (tag spec-v1, 2026-10-25). Las nuevas se agregan
al final con fecha y commit.

## D1 — Agente de programación: Pi
- Decisión: usar Pi 1.3.0 como harness que actúa sobre el repositorio.
- Alternativas: Claude Code, Codex.
- Motivo: es el agente propuesto en la demo; trabaja con varios proveedores de modelos,
  lee AGENTS.md y permite restringir herramientas con --tools.
- Consecuencias: Pi no pide aprobación antes de cada herramienta. Controles: rama por
  episodio, reglas en AGENTS.md, modo solo lectura para auditar y diff revisado por el
  autor antes de cada commit.

## D2 — Python con biblioteca estándar y paquete en la raíz
- Alternativas: Node.js (node:test), Java (Maven + JUnit); estructura src/.
- Motivo: sqlite3, datetime y argparse vienen incluidos; con el paquete en la raíz,
  `python -m reservas` funciona sin instalar nada.
- Consecuencias: requiere Python 3.12+ (probado con 3.15.0); la única dependencia es pytest
  (9.1.1), fijada en requirements-dev.txt.

## D3 — Almacenamiento en SQLite local
- Alternativas: archivo JSON o CSV.
- Motivo: transacción atómica para verificar e insertar; consultas por unidad e intervalo.
- Consecuencias: el .db no se versiona; el README documenta su ruta y el reinicio.

## D4 — Hora UTC−03:00 fija
- Alternativa: zoneinfo("America/Argentina/Buenos_Aires").
- Motivo: Argentina no aplica horario de verano y zoneinfo en Windows exige instalar tzdata.
- Consecuencias: si cambiara la política horaria, habría que migrar a zoneinfo.

## D5 — Intervalos semiabiertos y una sola función de superposición
- Alternativa: intervalos cerrados [inicio, fin] con lógica separada por operación.
- Motivo: los límites consecutivos son válidos por definición, y reserva y disponibilidad
  no pueden divergir.
- Consecuencias: cualquier cambio de regla se hace en un solo lugar.

## D6 — Fechas pasadas, límites y cancelación (S4, S5, S9)
- Decisión: rechazar intervalos que empiecen en el pasado; sin límites de duración ni de
  anticipación; se puede cancelar cualquier reserva activa.
- Alternativas: permitir carga retroactiva; máximos de 8 h o 90 días; cancelar solo
  reservas no terminadas.
- Motivo: la consigna no fija límites y no hay necesidad de negocio para inventarlos;
  reservar algo que ya ocurrió no tiene sentido operativo.
- Consecuencias: reloj inyectable para probar; no hay carga retroactiva; la app no
  distingue reservas "cumplidas".

## D7 — Fechas de 2099 en las pruebas de consola
- Alternativa: una variable de entorno para fijar el reloj de la consola.
- Motivo: las pruebas por subprocess usan el reloj real; fechas lejanas evitan que fallen
  con el paso del tiempo sin agregar un mecanismo solo para pruebas.
- Consecuencias: esas pruebas no cubren el rechazo de fechas pasadas; lo cubren las de dominio.

## D8 — Modelo: gemini-3.8-flash en el plan gratuito de la API de Gemini
- Alternativas: GitHub Copilot (altas de Copilot Student pausadas; plan Free con cupo
  mensual chico); suscripciones pagas.
- Motivo: gratis, sin tarjeta; de los modelos Flash disponibles es el más reciente.
- Consecuencias: límites por minuto y por día (el diario se renueva a la medianoche del
  Pacífico); si un límite corta el trabajo, se registra en PROGRESO.md. En el plan gratuito
  Google puede usar el contenido enviado, por lo que solo se usan datos ficticios.

## D9 — Engram y Linear como apoyo, con el registro oficial en el repo
- Decisión: Engram 3.5.1 (paquete gentle-engram 0.5.0 en Pi) para memoria del agente y
  Linear (issues LAB-5, LAB-6 y LAB-7, uno por episodio) para seguimiento.
- Alternativa: no usarlos (la consigna no los exige).
- Motivo: son herramientas de la demo y permiten trazar episodios y decisiones.
- Consecuencias: la memoria de Engram y los issues de Linear viven fuera del repo; el
  registro oficial es docs/PROGRESO.md y se incluyen extractos en docs/evidencia/.

## D10 — Gentle AI instalado como lanzador separado
- Decisión: instalar gentle-pi 4.3.0 con npm y abrirlo con `gentle-shell --link`, sin
  instalarlo dentro de Pi.
- Alternativa: instalarlo dentro de Pi (pi install) más gentle-ai sync, que modifica el Pi
  normal y requiere otro binario.
- Motivo: deja el Pi normal sin cambios y permite comparar.
- Consecuencias: en Windows requirió instalar Go 1.27.3 (sin Go falló con
  GENTLE_AI_GO_TOOLCHAIN_UNAVAILABLE); solo funciona desde PowerShell (en la terminal de
  VS Code y en Git Bash se cierra al iniciar); agrega 10 agentes, 12 skills y 56
  herramientas, lo que aumenta el consumo de cuota.
- Uso en los episodios: no se usa. En la prueba del 2026-10-25, en modo NORMAL, Gentle Shell
  creó un archivo sin pedir aprobación (evaluó "Risk: none"), por lo que no aporta
  aprobaciones humanas en escrituras comunes y suma contexto y consumo de cuota. Los episodios
  se hacen con Pi normal.

## D11 — Cambio de modelo a gemini-3.6-flash (2026-10-25)
- Contexto: gemini-3.8-flash y gemini-3.7-flash devolvieron error 503 UNAVAILABLE ("model is
  currently experiencing high demand") en varios intentos separados por 10 minutos.
- Decisión: usar gemini-3.6-flash, que respondió bien en la misma prueba.
- Alternativas: esperar a que se normalice 3.8; conectar GitHub Copilot.
- Consecuencias: reemplaza el modelo elegido en D8. Si en algún episodio se usa otro modelo,
  se registra en docs/episodios.md.