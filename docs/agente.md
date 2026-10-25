# Preparación del agente

## Entorno y modelo
| Dato | Valor | Cómo se obtuvo |
| --- | --- | --- |
| Sistema | Windows (versión no registrada) | winver |
| Git / terminal | Git 2.56.0.windows.2, Git Bash | git --version |
| Agente (harness) | Pi 1.3.0 | pi --version |
| Proveedor | Google Gemini, API key de AI Studio en plan gratuito | /login → Sign in with an API key → Google |
| Modelo | gemini-3.6-flash (D11) y gemini-3.8-flash por límite diario (D12); antes gemini-3.8-flash (D8) | barra inferior de Pi, /model y /session |
| Node.js / npm | 24.22.0 / 11.19.1 | node --version, npm --version |
| Python / pytest | 3.15.0 / 9.1.1 | python --version, python -m pytest --version |

Función: Pi lee el repositorio, crea y edita archivos y ejecuta las pruebas dentro de la carpeta
del proyecto. Motivo de la elección: D1 en docs/decisiones.md.

## Instrucciones y configuración
- De proyecto: AGENTS.md (versionado en la raíz). Pi lo carga al iniciar en la carpeta; se
  verificó antes del episodio 1 (docs/evidencia/episodio-1.md).
- Globales (~/.pi/agent/AGENTS.md): no se registró.
- Paquetes de Pi a nivel de usuario: gentle-engram 0.5.0, instalado por `engram setup pi`
  (salida de `pi list`).
- Configuración externa (~/.pi/agent/settings.json), aplicada el 2026-10-25 con un script de
  Python por los límites del plan gratuito. Extracto:

      "retry": { "enabled": true, "maxRetries": 6, "baseDelayMs": 5000 }

  Efecto: ante errores transitorios, Pi reintenta con esperas de 5, 10, 20, 40, 80 y 160 s;
  si el proveedor pide esperar horas (límite diario), falla de inmediato.
- Credenciales: ~/.pi/agent/auth.json, excluido y nunca copiado al repo.
- Prompt de cada episodio: docs/prompts/.

## Contexto
- Suministrado: AGENTS.md, docs/especificacion.md, data/inventario.json y el prompt del episodio.
- Excluido: .venv/, data/*.db, credenciales y conversaciones privadas completas.
- Datos: solo solicitantes ficticios; en el plan gratuito Google puede usar lo enviado (D8).
- Asistencia previa: el borrador de la especificación, de AGENTS.md y de las decisiones se
  preparó con Claude en un chat y lo revisó el autor.

## Herramientas, permisos y controles
Harness usado: Pi en el episodio 1 (D10) y Codex en los episodios 2 y 3 (D13).

| Episodio | Agente y herramientas | Controles aplicados |
| --- | --- | --- |
| 1 | Pi: read, bash, edit, write (por defecto) | Rama propia, reglas de AGENTS.md, revisión del diff y pruebas corridas por el autor antes de cada commit |
| 2, 3a, 3c | Codex, modo Workspace (Ask for approval) | Rama propia, reglas de AGENTS.md, aprobación de Codex para acciones fuera del espacio de trabajo, revisión del diff y pruebas corridas por el autor |
| 3b | Codex en modo de solo lectura | Sin escritura; el autor verificó cada hallazgo |

Pi no pide aprobación antes de cada herramienta; las reglas de AGENTS.md son instrucciones,
no un bloqueo técnico. En el episodio 1 el agente respetó los límites de commits, ramas y
archivos protegidos, pero borró una entrada de PROGRESO.md (corregido; ver docs/episodios.md).

## Adaptación específica y evidencia de uso
| Adaptación (AGENTS.md) | Evidencia en el repo |
| --- | --- |
| Turnos consecutivos con condición estricta | reservas/dominio.py:131 (`r.inicio < fin and inicio < r.fin`); test_r4_r8_ca3_ca7_acepta_consecutivas; prueba de mutación en docs/verificacion.md |
| Una sola función de superposición | verificar_superposicion_y_disponibilidad (dominio.py:95), usada en servicio.py:47, :109 y :146 y en persistencia.py:61; observación de la auditoría sobre la validación previa en D15 |
| Reloj inyectable en el dominio | Sin datetime.now en dominio.py, servicio.py ni persistencia.py; solo la consola usa el reloj real (cli.py:73); reloj fijo 2026-11-01 08:00 en las pruebas |
| Procedimiento de persistencia | reservas/persistencia.py:57–65 (BEGIN IMMEDIATE y función de dominio dentro de la transacción); test_r9_ca8_reabrir_instancia_conserva_activas_y_canceladas; mutación del episodio 2 en docs/verificacion.md |
| Nombres de prueba con el requisito | Salida de pytest -v en docs/verificacion.md. Episodio 1: 6 de 7 correctos (la séptima la corrigió el autor). Episodio 3a: 0 de 5 correctos (los corrigió el agente a pedido del autor) |
| Registro de progreso del agente | Entradas "(agente)" de los episodios 1, 2, 3a y 3c en docs/PROGRESO.md |
| Agregar al final de PROGRESO.md sin borrar (ajuste D14) | Episodio 1: el agente borró una entrada del autor. Después del ajuste, episodios 2 y 3: solo agregados al final (git diff en docs/verificacion.md) |

## Retención del progreso
- docs/PROGRESO.md (versionado): lo escriben el agente al cerrar cada tarea y el autor.
- Engram: proyecto detectado como lab-reservas_topicosavanzados; en el episodio 1 el agente
  hizo un search (0 resultados) y guardó la memoria #1 (docs/evidencia/episodio-1.md).

## Herramientas opcionales
| Herramienta | ¿Se usó? | Versión | Para qué |
| --- | --- | --- | --- |
| Orca | No | — | No se usó |
| Engram | Sí | 3.5.1 | Memoria del agente entre sesiones |
| Gentle AI | Instalado y probado; no usado en los episodios | gentle-pi 4.3.0 | Ver D10 |
| Linear | Sí | Plan gratuito | Issues LAB-5, LAB-6 y LAB-7, uno por episodio |
| Go | Sí | 1.27.3 | Requisito para instalar Gentle AI en Windows |


## Episodios 2 y 3: Codex (D13)
| Dato | Valor | Cómo se obtuvo |
| --- | --- | --- |
| Agente (harness) | Codex CLI 0.164.0 | codex --version |
| Cuenta | ChatGPT, plan Free (límite mensual) | /status |
| Modelo | GPT-6-Luna (reasoning medium) | /status |
| Permisos | Workspace (Ask for approval): edita dentro del repo y pide aprobación para lo que sale de ese límite | /status |
| Instrucciones | AGENTS.md, leído de forma nativa; confirmado con /status y con una pregunta sin herramientas | /status y pregunta |
| Auditoría 3b | codex --sandbox read-only --ask-for-approval never; /status mostró "Permissions: Read Only (never)"; git status limpio después de la auditoría (episodio 3b) | /status y git status |

Datos: los pedidos van a OpenAI bajo los términos de ChatGPT; solo se usan datos ficticios.
Engram no está conectado a Codex.

### Uso en el episodio 2
- Codex no pidió aprobaciones: leyó, editó y corrió las pruebas dentro del modo Workspace.
- La regla de D14 (agregar al final de PROGRESO.md sin borrar) se respetó; ver
  docs/verificacion.md.
- El sandbox de Codex creó la carpeta temporal de pytest con permisos que el usuario no puede
  leer; el autor verifica con --basetemp fuera del repo.
- Límite mensual: 100 % antes y 99 % después del episodio.

### Uso en el episodio 3
- 3a y 3c en modo Workspace (Ask for approval); 3b en solo lectura (Read Only, never).
- En 3a y 3b Codex no pidió aprobaciones; en 3c: no se registró.
- La regla de D14 se respetó en las tres partes: PROGRESO.md solo recibió agregados al final.
- Límite mensual: 99 % después de 3a y 98 % después de 3b; después de 3c: no se registró.