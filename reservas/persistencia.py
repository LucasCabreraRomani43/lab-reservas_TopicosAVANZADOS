"""Repositorio de reservas persistido en SQLite."""

import sqlite3
from datetime import datetime
from pathlib import Path

from reservas.dominio import (
    ErrorDominio,
    EstadoReserva,
    Reserva,
    formatear_fecha,
    parsear_fecha,
    verificar_superposicion_y_disponibilidad,
)


class RepositorioSQLite:
    def __init__(self, ruta: str | Path):
        self.ruta = str(ruta)
        Path(self.ruta).parent.mkdir(parents=True, exist_ok=True)
        with self._conexion() as conexion:
            conexion.execute(
                """CREATE TABLE IF NOT EXISTS reservas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    unidad TEXT NOT NULL,
                    solicitante TEXT NOT NULL,
                    inicio TEXT NOT NULL,
                    fin TEXT NOT NULL,
                    estado TEXT NOT NULL,
                    creada_en TEXT NOT NULL,
                    cancelada_en TEXT
                )"""
            )

    def _conexion(self):
        return sqlite3.connect(self.ruta, isolation_level=None)

    @staticmethod
    def _desde_fila(fila) -> Reserva:
        return Reserva(
            id=fila[0], unidad=fila[1], solicitante=fila[2],
            inicio=parsear_fecha(fila[3]), fin=parsear_fecha(fila[4]),
            estado=EstadoReserva(fila[5]), creada_en=parsear_fecha(fila[6]),
            cancelada_en=parsear_fecha(fila[7]) if fila[7] else None,
        )

    def obtener_todas(self) -> list[Reserva]:
        with self._conexion() as conexion:
            filas = conexion.execute(
                "SELECT id, unidad, solicitante, inicio, fin, estado, creada_en, cancelada_en FROM reservas ORDER BY id"
            ).fetchall()
        return [self._desde_fila(fila) for fila in filas]

    def reservar_si_disponible(self, unidad, solicitante, inicio, fin, creada_en, ahora, unidades_validas):
        conexion = self._conexion()
        try:
            conexion.execute("BEGIN IMMEDIATE")
            reservas = [self._desde_fila(fila) for fila in conexion.execute(
                "SELECT id, unidad, solicitante, inicio, fin, estado, creada_en, cancelada_en FROM reservas"
            ).fetchall()]
            disponible, conflictos = verificar_superposicion_y_disponibilidad(
                unidad, inicio, fin, reservas, ahora, unidades_validas
            )
            if not disponible:
                raise ErrorDominio(
                    f"La unidad '{unidad}' no está disponible en el intervalo indicado. "
                    f"Existe(n) {len(conflictos)} reserva(s) en conflicto."
                )
            cursor = conexion.execute(
                "INSERT INTO reservas (unidad, solicitante, inicio, fin, estado, creada_en, cancelada_en) VALUES (?, ?, ?, ?, ?, ?, NULL)",
                (unidad, solicitante, formatear_fecha(inicio), formatear_fecha(fin),
                 EstadoReserva.ACTIVA.value, formatear_fecha(creada_en)),
            )
            reserva = Reserva(cursor.lastrowid, unidad, solicitante, inicio, fin, creada_en)
            conexion.execute("COMMIT")
            return reserva
        except Exception:
            if conexion.in_transaction:
                conexion.execute("ROLLBACK")
            raise
        finally:
            conexion.close()

    def agregar(self, unidad, solicitante, inicio, fin, creada_en) -> Reserva:
        """Interfaz de repositorio compatible; el servicio usa reservar_si_disponible."""
        conexion = self._conexion()
        try:
            cursor = conexion.execute(
                "INSERT INTO reservas (unidad, solicitante, inicio, fin, estado, creada_en, cancelada_en) VALUES (?, ?, ?, ?, ?, ?, NULL)",
                (unidad, solicitante, formatear_fecha(inicio), formatear_fecha(fin),
                 EstadoReserva.ACTIVA.value, formatear_fecha(creada_en)),
            )
            return Reserva(cursor.lastrowid, unidad, solicitante, inicio, fin, creada_en)
        finally:
            conexion.close()

    def cancelar(self, reserva_id: int, cancelada_en: datetime) -> Reserva:
        conexion = self._conexion()
        try:
            conexion.execute("BEGIN IMMEDIATE")
            fila = conexion.execute(
                "SELECT id, unidad, solicitante, inicio, fin, estado, creada_en, cancelada_en FROM reservas WHERE id = ?",
                (reserva_id,),
            ).fetchone()
            if fila is None:
                raise ErrorDominio(f"No existe la reserva {reserva_id}.")
            reserva = self._desde_fila(fila)
            if reserva.estado != EstadoReserva.ACTIVA:
                raise ErrorDominio(f"La reserva {reserva_id} ya está cancelada.")
            conexion.execute(
                "UPDATE reservas SET estado = ?, cancelada_en = ? WHERE id = ?",
                (EstadoReserva.CANCELADA.value, formatear_fecha(cancelada_en), reserva_id),
            )
            conexion.execute("COMMIT")
            return Reserva(
                reserva.id, reserva.unidad, reserva.solicitante, reserva.inicio, reserva.fin,
                reserva.creada_en, EstadoReserva.CANCELADA, cancelada_en,
            )
        except Exception:
            if conexion.in_transaction:
                conexion.execute("ROLLBACK")
            raise
        finally:
            conexion.close()

    def reiniciar_datos(self) -> None:
        with self._conexion() as conexion:
            conexion.execute("DELETE FROM reservas")
