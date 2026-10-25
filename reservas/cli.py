"""Interfaz de consola para gestionar reservas del laboratorio."""

import argparse
import os
import sys
from datetime import datetime
from pathlib import Path

from reservas.dominio import ErrorDominio, TZ_ARG, formatear_fecha
from reservas.inventario import ErrorInventario, Inventario
from reservas.persistencia import RepositorioSQLite
from reservas.servicio import ServicioReservas


def _crear_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="python -m reservas", description="Gestión de reservas del laboratorio.")
    parser.add_argument("--db", default=os.environ.get("RESERVAS_DB", "data/reservas.db"), help="ruta de la base SQLite")
    comandos = parser.add_subparsers(dest="comando", required=True)

    comandos.add_parser("unidades", help="listar unidades del inventario")

    disponibilidad = comandos.add_parser("disponibilidad", help="consultar disponibilidad")
    _agregar_intervalo(disponibilidad)

    reservar = comandos.add_parser("reservar", help="crear una reserva")
    _agregar_intervalo(reservar)
    reservar.add_argument("--solicitante", required=True, help="nombre del solicitante")

    cancelar = comandos.add_parser("cancelar", help="cancelar una reserva activa")
    cancelar.add_argument("--id", type=int, required=True, help="ID de la reserva")

    listar = comandos.add_parser("listar", help="listar reservas")
    listar.add_argument("--unidad", help="filtrar por ID de unidad")

    reiniciar = comandos.add_parser("reiniciar-datos", help="borrar todas las reservas")
    reiniciar.add_argument("--confirmar", action="store_true", help="confirmar el borrado")
    return parser


def _agregar_intervalo(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--unidad", required=True, help="ID exacto de la unidad")
    parser.add_argument("--inicio", required=True, help="inicio (AAAA-MM-DD HH:MM)")
    parser.add_argument("--fin", required=True, help="fin (AAAA-MM-DD HH:MM)")


def _ruta_inventario() -> Path:
    return Path(__file__).resolve().parent.parent / "data" / "inventario.json"


def _imprimir_reserva(reserva) -> None:
    print(
        f"ID: {reserva.id} | Unidad: {reserva.unidad} | Solicitante: {reserva.solicitante} | "
        f"Inicio: {formatear_fecha(reserva.inicio)} | Fin: {formatear_fecha(reserva.fin)} | "
        f"Estado: {reserva.estado.value}"
    )


def main(argv: list[str] | None = None) -> int:
    parser = _crear_parser()
    args = parser.parse_args(argv)

    try:
        inventario = Inventario.cargar_desde_archivo(_ruta_inventario())
        if args.comando == "unidades":
            for unidad in inventario.listar():
                print(f"{unidad.id} | {unidad.equipo}")
            return 0

        repo = RepositorioSQLite(args.db)
        servicio = ServicioReservas(
            inventario,
            repo,
            reloj=lambda: datetime.now(TZ_ARG),
        )

        if args.comando == "disponibilidad":
            disponible, conflictos = servicio.disponibilidad(args.unidad, args.inicio, args.fin)
            if disponible:
                print("La unidad está disponible.")
                return 0
            print("La unidad no está disponible. Reservas en conflicto:")
            for reserva in conflictos:
                _imprimir_reserva(reserva)
            return 1
        if args.comando == "reservar":
            reserva = servicio.reservar(args.unidad, args.solicitante, args.inicio, args.fin)
            print(f"Reserva creada con ID {reserva.id}.")
            return 0
        if args.comando == "cancelar":
            reserva = servicio.cancelar(args.id)
            print(f"Reserva {reserva.id} cancelada.")
            return 0
        if args.comando == "listar":
            for reserva in servicio.listar(args.unidad):
                _imprimir_reserva(reserva)
            return 0
        if args.comando == "reiniciar-datos":
            if not args.confirmar:
                print("No se borraron datos. Para confirmar, use --confirmar.")
                return 0
            servicio.reiniciar_datos(confirmar=True)
            print("Se borraron todas las reservas.")
            return 0
    except (ErrorDominio, ErrorInventario) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    except (OSError, ValueError) as error:
        print(f"Error al acceder a los datos: {error}", file=sys.stderr)
        return 1
    return 0
