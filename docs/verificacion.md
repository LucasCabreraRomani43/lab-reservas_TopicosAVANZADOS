# Verificación humana

Comprobaciones ejecutadas por el autor, separadas de lo que informó el agente.

## Entorno
Windows <versión> · Git Bash · Python 3.15.0 · pytest 9.1.1 · Pi 1.3.0

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