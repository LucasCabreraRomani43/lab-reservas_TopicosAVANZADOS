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