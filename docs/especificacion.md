# Especificación — Reservas de equipos del laboratorio

Versión 1 (2026-10-25, tag spec-v1). Los cambios posteriores quedan en Git y en docs/decisiones.md.

## 1. Problema
La coordinación de un laboratorio registra pedidos en mensajes y una planilla. Hubo unidades
confirmadas para horarios superpuestos y cancelaciones que seguían bloqueando el horario.
Se necesita una herramienta local para consultar disponibilidad, reservar y cancelar sin
perder el historial.

## 2. Alcance
Incluye: lectura del inventario precargado (data/inventario.json), consulta de disponibilidad
por unidad e intervalo, creación y cancelación de reservas, listado del historial y
persistencia local.

Excluye: administración del inventario, autenticación y roles, notificaciones, pagos,
integraciones externas, interfaz gráfica, despliegue y concurrencia entre procesos o equipos.

## 3. Supuestos
| ID  | Supuesto |
|-----|----------|
| S1  | Zona horaria única: hora de Argentina, UTC−03:00 fija (sin horario de verano). |
| S2  | Formato AAAA-MM-DD HH:MM, 24 h. Ej.: 2026-11-03 10:00. Otro formato se rechaza. |
| S3  | Intervalos semiabiertos [inicio, fin): una reserva de 10:00 a 11:00 libera la unidad a las 11:00. |
| S4  | No se aceptan intervalos que empiecen antes del momento actual, ni para reservar ni para consultar. El historial sí puede tener reservas pasadas. |
| S5  | Sin límite de duración ni de anticipación; una reserva puede abarcar varios días. |
| S6  | El solicitante se guarda sin espacios al inicio ni al final. Es ficticio; no se valida identidad. |
| S7  | Los ID de unidad se comparan exactamente como en el inventario (MIC-01, no mic-01). |
| S8  | Los ID de reserva son enteros crecientes y nunca se reutilizan. |
| S9  | La cancelación es definitiva. Se puede cancelar cualquier reserva activa, aunque su horario ya haya pasado. |
| S10 | La aplicación la usa un solo proceso a la vez en una sola computadora. |

## 4. Requisitos
| ID  | Requisito verificable |
|-----|-----------------------|
| R1  | Al iniciar se leen las 5 unidades de data/inventario.json; `unidades` las lista con ID y equipo. Si el archivo falta o es inválido, error claro. |
| R2  | Una reserva con unidad conocida, solicitante válido, fechas válidas, inicio < fin, inicio no pasado y sin conflicto recibe un ID nuevo y queda ACTIVA con unidad, solicitante, inicio, fin y fecha de creación. |
| R3  | Se rechaza si existe otra reserva ACTIVA de la misma unidad con existente.inicio < nueva.fin y nueva.inicio < existente.fin. |
| R4  | Se aceptan reservas consecutivas de la misma unidad (fin de una = inicio de otra). |
| R5  | Se aceptan reservas simultáneas de unidades distintas. |
| R6  | Se rechaza, sin crear nada y con un mensaje que indica el motivo: unidad desconocida; solicitante vacío o solo espacios; fecha u hora mal formada o inexistente (2026-02-30 10:00, 2026-11-03 25:00); inicio igual o posterior al fin; inicio en el pasado. |
| R7  | Cancelar una reserva ACTIVA la pasa a CANCELADA, conserva ID y datos, registra la fecha de cancelación y libera el intervalo. Cancelar una inexistente o ya cancelada es error y no modifica nada. |
| R8  | La disponibilidad (unidad, inicio, fin) usa las mismas validaciones (salvo solicitante) y la misma regla de R3. Informa disponible o no y lista las reservas activas en conflicto. Invariante: disponible ⇔ una reserva válida en ese intervalo sería aceptada. |
| R9  | Reservas activas y canceladas, con su estado, se conservan al cerrar y volver a ejecutar en otro proceso. Iniciar la app nunca borra datos. |
| R10 | `listar` muestra todas las reservas (activas y canceladas), opcionalmente por unidad, ordenadas por inicio. |
| R11 | El reinicio de datos borra todas las reservas solo con --confirmar. |

## 5. Interfaz (consola)
    python -m reservas unidades
    python -m reservas disponibilidad --unidad MIC-01 --inicio "2026-11-03 10:00" --fin "2026-11-03 11:00"
    python -m reservas reservar --unidad MIC-01 --solicitante "Ana Pérez" --inicio "2026-11-03 10:00" --fin "2026-11-03 11:00"
    python -m reservas cancelar --id 1
    python -m reservas listar [--unidad MIC-01]
    python -m reservas reiniciar-datos --confirmar

Opción global --db RUTA (o variable RESERVAS_DB); por defecto data/reservas.db.
Códigos de salida: 0 éxito, 1 rechazo por regla o validación, 2 uso incorrecto.

## 6. Criterios de aceptación
Reloj de referencia en pruebas de dominio y persistencia: 2026-11-01 08:00 −03:00.
Las pruebas de consola en procesos separados usan fechas de 2099 (ver D7).

| CA   | Req | Dado / cuando / entonces |
|------|-----|--------------------------|
| CA1  | R2  | Sin reservas: MIC-01, "Ana Pérez", 2026-11-03 10:00–11:00 → aceptada, ID 1, ACTIVA. |
| CA2  | R3  | Con CA1: MIC-01 10:30–11:30, 09:30–10:30, 09:00–12:00, 10:15–10:45 y 10:00–11:00 → todas rechazadas. |
| CA3  | R4  | Con CA1: MIC-01 11:00–12:00 y 09:00–10:00 → aceptadas. |
| CA4  | R5  | Con CA1: MIC-02 10:00–11:00 → aceptada. |
| CA5  | R6  | Cada entrada inválida de R6 → rechazada; la cantidad de reservas no cambia. |
| CA6  | R7  | Con CA1, cancelar ID 1 → listar la muestra CANCELADA con los mismos datos; luego MIC-01 10:30–11:30 → aceptada. Cancelar ID 1 otra vez o ID 99 → error. |
| CA7  | R8  | La disponibilidad coincide con el resultado de reservar en todos los casos de CA2–CA4 y CA6. |
| CA8  | R9  | Crear una reserva y cancelar otra; terminar el proceso; listar en un proceso nuevo con la misma base → ambas con su estado. |
| CA9  | R1  | `unidades` lista exactamente los 5 ID del inventario. |
| CA10 | R11 | `reiniciar-datos` sin --confirmar no borra nada. |