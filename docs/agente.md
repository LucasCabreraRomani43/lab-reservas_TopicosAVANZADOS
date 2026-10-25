# Preparación del agente

## Entorno y modelo
| Dato | Valor | Cómo se obtuvo |
| --- | --- | --- |
| Sistema | Windows <versión> | winver |
| Git / terminal | Git 2.56.0.windows.2, Git Bash | git --version |
| Agente (harness) | Pi 1.3.0 | pi --version |
| Proveedor | Google Gemini, API key de AI Studio en plan gratuito | /login → Sign in with an API key → Google |
| Modelo | gemini-3.8-flash | barra inferior de Pi y /model |
| Node.js / npm | 24.22.0 / 11.19.1 | node --version, npm --version |
| Python / pytest | 3.15.0 / 9.1.1 | python --version, python -m pytest --version |

Función: Pi lee el repositorio, crea y edita archivos y ejecuta las pruebas dentro de la carpeta
del proyecto. Motivo de la elección: D1 en docs/decisiones.md.

## Instrucciones y configuración
- De proyecto: AGENTS.md (versionado en la raíz). Pi lo carga al iniciar en la carpeta.
- Globales (~/.pi/agent/AGENTS.md): <no se usaron / extracto saneado>.
- Paquetes de Pi a nivel de usuario: gentle-engram 0.5.0, instalado por `engram setup pi`
  (salida de `pi list`).
- Configuración externa (~/.pi/agent/settings.json): <extracto saneado>.
- Credenciales: ~/.pi/agent/auth.json, excluido y nunca copiado al repo.
- Prompt de cada episodio: docs/prompts/.

## Contexto
- Suministrado: AGENTS.md, docs/especificacion.md, data/inventario.json y el prompt del episodio.
- Excluido: .venv/, data/*.db, credenciales y conversaciones privadas completas.
- Datos: solo solicitantes ficticios; en el plan gratuito Google puede usar lo enviado (D8).
- Asistencia previa: el borrador de la especificación, de AGENTS.md y de las decisiones se
  preparó con Claude en un chat y lo revisó el autor.

## Herramientas, permisos y controles
Harness usado en los episodios: <Pi normal / Gentle Shell> (D10).

| Episodio | Herramientas | Controles aplicados |
| --- | --- | --- |
| 1, 2, 3a | read, bash, edit, write (por defecto) | Rama propia, reglas de AGENTS.md, revisión del diff y pruebas corridas por el autor antes de cada commit |
| 3b | read, grep, find, ls (--tools) | Sin escritura ni comandos; el autor verificó cada hallazgo |

Pi no pide aprobación antes de cada herramienta; las reglas de AGENTS.md son instrucciones,
no un bloqueo técnico. Qué se revisó antes de aceptar cada resultado: docs/episodios.md.

## Adaptación específica y evidencia de uso
| Adaptación (AGENTS.md) | Evidencia en el repo |
| --- | --- |
| Turnos consecutivos: condición estricta y una sola función | <archivo y línea>, <prueba test_r4_…> |
| Procedimiento de persistencia | <BEGIN IMMEDIATE: archivo y línea>, <prueba test_r9_…> |
| Nombres de prueba con el requisito | <salida de pytest -v en docs/verificacion.md> |
| Registro de progreso del agente | <entradas "(agente)" en docs/PROGRESO.md> |

## Retención del progreso
- docs/PROGRESO.md (versionado): lo escriben el agente al cerrar cada tarea y el autor.
- Engram: proyecto detectado como lab-reservas_topicosavanzados; extractos en
  docs/evidencia/engram.md <completar>.

## Herramientas opcionales
| Herramienta | ¿Se usó? | Versión | Para qué |
| --- | --- | --- | --- |
| Orca | <sí/no> | | |
| Engram | Sí | 3.5.1 | Memoria del agente entre sesiones |
| Gentle AI | Instalado | gentle-pi 4.3.0 | <completar según D10> |
| Linear | Sí | Plan gratuito | Issues LAB-5, LAB-6 y LAB-7, uno por episodio |
| Go | Sí | 1.27.3 | Requisito para instalar Gentle AI en Windows |