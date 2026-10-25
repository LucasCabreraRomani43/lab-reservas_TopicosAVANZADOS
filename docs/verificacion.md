# Verificación humana

Comprobaciones ejecutadas por el autor, separadas de lo que informó el agente.

## Entorno
Windows 10, versión 22H2· Git Bash · Python 3.15.0 · pytest 9.1.1 · Pi 1.3.0

## Episodio 1 — Dominio y validaciones

### Pruebas automáticas ejecutadas por el autor
| Fecha | Código | Comando | Resultado |
| --- | --- | --- | --- |
| 2026-10-25 | Tal como lo entregó el agente | python -m pytest -v | 7 passed |
| 2026-10-25 | Commit c4f4724, con correcciones del autor | python -m pytest -v | 7 passed |

Pruebas: test_r1_ca9_carga_inventario, test_r2_ca1_crear_primera_reserva,
test_r3_r8_ca2_ca7_rechaza_superposiciones, test_r4_r8_ca3_ca7_acepta_consecutivas,
test_r5_r8_ca4_ca7_acepta_simultaneas_distintas_unidades, test_r6_ca5_rechaza_entradas_invalidas,
test_r2_s6_solicitante_se_guarda_sin_espacios.

### Controles sobre el código
| Control | Cómo | Resultado |
| --- | --- | --- |
| Pi cargó AGENTS.md | Pregunta a Pi sin herramientas | Respondió con la ruta del AGENTS.md del proyecto |
| Sin reloj real en el dominio | grep -rn "datetime.now" reservas/ | Sin resultados |
| Una sola función de superposición | grep -n "verificar_superposicion_y_disponibilidad" reservas/*.py | Definida en dominio.py:95; usada en servicio.py:80 y :113 |
| Cobertura de CA2 y CA5 | Lectura de test_r3 y test_r6 | Los 5 intervalos de CA2; unidad desconocida, solicitante vacío y con espacios, 5 fechas inválidas, inicio ≥ fin e inicio pasado |

### Prueba de mutación
| Cambio | Comando | Esperado | Observado |
| --- | --- | --- | --- |
| dominio.py:131, `r.inicio < fin` por `r.inicio <= fin` | python -m pytest -q | Falla la prueba de turnos consecutivos (R4) | Primer intento: 7 passed, porque el cambio no estaba guardado (error del autor). Con el cambio guardado: 1 failed, 6 passed; falló test_r4_r8_ca3_ca7_acepta_consecutivas (línea 160). |
| Mutación descartada con git checkout | python -m pytest -q | 7 passed | 7 passed |

### Informado por el agente vs. comprobado por el autor
| El agente informó | El autor obtuvo | ¿Coincide? |
| --- | --- | --- |
| "7 passed in 0.11s" | 7 passed (pytest -v) | Sí |
| pyproject.toml descripto como configuración de pytest | Tenía además [build-system] | No (corregido) |
| Agregó su entrada en PROGRESO.md | La agregó, pero borró una entrada del autor | No (corregido) |

### Pasos bloqueados
- El agente no pudo aplicar la corrección de pyproject.toml y del nombre de la prueba: 429 por
  límite diario en gemini-3.8-flash; con gemini-3.7-flash y gemini-3.5-flash los pedidos se
  rechazaron con las cuotas de 3.8 y 3.6. La aplicó el autor.

  
## Episodio 2 — Persistencia SQLite y cancelación

### Pruebas automáticas ejecutadas por el autor
| Fecha | Código | Comando | Resultado |
| --- | --- | --- | --- |
| 2026-10-25 | Commit e3919cd (tal como lo entregó el agente) | python -m pytest -v | 7 passed, 5 errors: PermissionError [WinError 5] en la carpeta temporal de pytest (C:\Users\<usuario>\AppData\Local\Temp\pytest-of-<usuario>) |
| 2026-10-25 | Commit e3919cd | python -m pytest -v --basetemp=../pytest-tmp-lab | 12 passed |

Causa: el sandbox de Codex creó la carpeta temporal de pytest con permisos que el usuario
normal no puede leer. Fallaron solo las 5 pruebas que usan tmp_path; las 7 del episodio 1
pasaron. Mientras se trabaje con Codex, el autor verifica con --basetemp fuera del repo.

Pruebas nuevas: test_r7_ca6_cancelar_libera_intervalo_y_conserva_historial,
test_r9_ca8_reabrir_instancia_conserva_activas_y_canceladas,
test_r11_ca10_reinicio_sin_confirmar_no_borra_y_confirmado_borra,
test_r9_abrir_base_existente_no_borra_datos, test_r3_rechaza_superposicion_parcial.

### Controles sobre el código
| Control | Cómo | Resultado |
| --- | --- | --- |
| Codex cargó AGENTS.md | /status | "Agents.md: AGENTS.md" |
| Archivos tocados | git status | servicio.py, persistencia.py, test_persistencia.py y PROGRESO.md |
| Regla de D14 (agregar al final) | git diff docs/PROGRESO.md | Solo agregó; la única línea con "-" es el salto de línea final, que vuelve con "+" |
| Transacción | grep "BEGIN IMMEDIATE" | persistencia.py:57 y :100 |
| Función de dominio reutilizada | grep "verificar_superposicion_y_disponibilidad" | Definida en dominio.py:95; usada en persistencia.py:61 y servicio.py:47, :109 y :146 |
| Sin borrado al cancelar | grep "DELETE" | Solo persistencia.py:128 (reinicio de datos) |
| Sin reloj real | grep -rn "datetime.now" reservas/ | Sin resultados |

### Prueba de mutación
| Cambio | Comando | Esperado | Observado |
| --- | --- | --- | --- |
| dominio.py:129, se quitó `and r.estado == EstadoReserva.ACTIVA` (las canceladas pasan a bloquear) | python -m pytest -q --basetemp=../pytest-tmp-lab | Falla la prueba de CA6 | 1 failed, 11 passed; falló test_r7_ca6_cancelar_libera_intervalo_y_conserva_historial (línea 42: la reserva 10:30–11:30 fue rechazada por la cancelada) |
| Mutación descartada con git checkout | python -m pytest -q --basetemp=../pytest-tmp-lab | 12 passed | 12 passed |

El primer intento de reemplazar la línea completa dio error; se rehízo borrando solo el
fragmento.

### Informado por el agente vs. comprobado por el autor
| El agente informó | El autor obtuvo | ¿Coincide? |
| --- | --- | --- |
| "12 passed, 1 warning" | 7 passed y 5 errors sin --basetemp; 12 passed con --basetemp | No, por el entorno |
| Agregó su entrada al final de PROGRESO.md | Confirmado con git diff | Sí |
| Verificación e inserción dentro de BEGIN IMMEDIATE | Confirmado (persistencia.py:57–61) | Sí |


## Episodio 3 — Consola, auditoría y correcciones

### Pruebas automáticas ejecutadas por el autor
| Fecha | Código | Comando | Resultado |
| --- | --- | --- | --- |
| 2026-10-25 | Parte 3a, antes de la corrección de nombres | python -m pytest -v --basetemp=../pytest-tmp-lab | 17 passed; las 5 pruebas de test_cli.py sin número de requisito |
| 2026-10-25 | Commit 3346f5c | python -m pytest -v --basetemp=../pytest-tmp-lab | 17 passed |
| 2026-10-25 | Commit 5b9cf8d | python -m pytest -v --basetemp=../pytest-tmp-lab | 19 passed |

### Prueba manual de la consola (3a)
Base de prueba fuera del repo (RESERVAS_DB=../prueba-cli.db), borrada al terminar.

| Comando | Esperado | Observado |
| --- | --- | --- |
| unidades | Las 5 unidades del inventario | MIC-01, MIC-02, OSC-01, MUL-01 y FUE-01 con su equipo |
| reservar MIC-01, 2099-11-03 10:00–11:00 | Aceptada, código 0 | "Reserva creada con ID 1.", código 0 |
| reservar MIC-01, 2099-11-03 10:30–11:30 | Rechazada por superposición, código 1 | "Error: La unidad 'MIC-01' no está disponible en el intervalo indicado…", código 1 |
| listar | La reserva 1 activa | "ID: 1 \| Unidad: MIC-01 \| Solicitante: Ana Pérez \| … \| Estado: ACTIVA" |
| comando-que-no-existe | Uso incorrecto, código 2 | Mensaje de uso de argparse, código 2 |

Control adicional: grep -rn "datetime.now" reservas/ → solo reservas/cli.py:73 (capa de
consola; el dominio sigue recibiendo un reloj inyectable).

### Verificación de la auditoría (3b)
| Hallazgo del agente | Comprobación del autor | Veredicto |
| --- | --- | --- |
| S2: dominio.py:29 acepta fechas con espacios externos | python -c con parsear_fecha(' 2026-11-03 10:00 ') devolvió 2026-11-03 10:00:00-03:00 | Confirmado |
| S8: servicio.py:71-73 reinicia el contador de ID | El repositorio en memoria vuelve _proximo_id a 1. En la consola con SQLite: reservar → ID 1; reiniciar-datos --confirmar; reservar → ID 2 (AUTOINCREMENT en persistencia.py:24) | Confirmado solo en el repositorio en memoria |
| Regla 3: validación en dos funciones | servicio.py:125-145 llama a validar_intervalo_y_solicitante (dominio.py:58) y luego a verificar_superposicion_y_disponibilidad (dominio.py:95) | Confirmado en la forma, sin impacto (D15) |

Después de la auditoría, git status: working tree clean (no modificó archivos).

### Verificación de las correcciones (3c)
| Corrección | Comprobación | Resultado |
| --- | --- | --- |
| S2 | El mismo python -c | ErrorDominio: "Formato de fecha u hora inválido o inexistente" |
| S8 | test_r11_s8_reinicio_memoria_no_reutiliza_id | passed |
| Regla de D14 | git diff --stat docs/PROGRESO.md | +17, sin borrados |

### Informado por el agente vs. comprobado por el autor
| El agente informó | El autor obtuvo | ¿Coincide? |
| --- | --- | --- |
| 3a: "17 passed" | 17 passed con --basetemp | Sí |
| 3b: los 10 criterios con cobertura | Las pruebas citadas existen y pasan (pytest -v) | Sí |
| 3b: tres desvíos | Dos confirmados (S2; S8 solo en memoria) y uno sin impacto (regla 3) | Parcial |
| 3c: correcciones aplicadas | 19 passed y la fecha con espacios rechazada | Sí |