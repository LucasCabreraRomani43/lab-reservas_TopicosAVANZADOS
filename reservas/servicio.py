from datetime import datetime
from typing import Callable

from reservas.dominio import (
    Reserva,
    EstadoReserva,
    ErrorDominio,
    parsear_fecha,
    validar_intervalo_y_solicitante,
    verificar_superposicion_y_disponibilidad,
)
from reservas.inventario import Inventario


class RepositorioEnMemoria:
    """Repositorio en memoria de reservas para pruebas y desacoplamiento."""

    def __init__(self):
        self._reservas: list[Reserva] = []
        self._proximo_id = 1

    def obtener_todas(self) -> list[Reserva]:
        return list(self._reservas)

    def agregar(
        self,
        unidad: str,
        solicitante: str,
        inicio: datetime,
        fin: datetime,
        creada_en: datetime,
    ) -> Reserva:
        reserva = Reserva(
            id=self._proximo_id,
            unidad=unidad,
            solicitante=solicitante,
            inicio=inicio,
            fin=fin,
            creada_en=creada_en,
            estado=EstadoReserva.ACTIVA,
        )
        self._proximo_id += 1
        self._reservas.append(reserva)
        return reserva


class ServicioReservas:
    """
    Servicio de aplicación para gestionar reservas y consultas de disponibilidad.
    Recibe un reloj inyectable (Callable[[], datetime]) y un inventario.
    """

    def __init__(
        self,
        inventario: Inventario,
        repositorio: RepositorioEnMemoria | None = None,
        reloj: Callable[[], datetime] | None = None,
    ):
        self.inventario = inventario
        self.repo = repositorio if repositorio is not None else RepositorioEnMemoria()
        self.reloj = reloj

    def _obtener_ahora(self) -> datetime:
        if self.reloj is not None:
            return self.reloj()
        raise RuntimeError("No se ha configurado un reloj inyectable.")

    def disponibilidad(
        self, unidad_id: str, inicio_str: str, fin_str: str
    ) -> tuple[bool, list[Reserva]]:
        """
        Consulta la disponibilidad de una unidad en un intervalo [inicio, fin) (R8).
        Retorna (disponible, lista_conflictos).
        """
        ahora = self._obtener_ahora()
        inicio = parsear_fecha(inicio_str)
        fin = parsear_fecha(fin_str)

        unidades_validas = self.inventario.ids()
        return verificar_superposicion_y_disponibilidad(
            unidad_id=unidad_id,
            inicio=inicio,
            fin=fin,
            reservas_existentes=self.repo.obtener_todas(),
            ahora=ahora,
            unidades_validas=unidades_validas,
        )

    def reservar(
        self, unidad_id: str, solicitante: str, inicio_str: str, fin_str: str
    ) -> Reserva:
        """
        Crea una nueva reserva si se cumplen todas las reglas y no hay conflicto (R2).
        Retorna la Reserva creada con estado ACTIVA.
        """
        ahora = self._obtener_ahora()
        inicio = parsear_fecha(inicio_str)
        fin = parsear_fecha(fin_str)

        unidades_validas = self.inventario.ids()

        # Valida unidad, inicio < fin, inicio >= ahora y solicitante
        solicitante_limpio = validar_intervalo_y_solicitante(
            unidad_id=unidad_id,
            inicio=inicio,
            fin=fin,
            ahora=ahora,
            unidades_validas=unidades_validas,
            solicitante=solicitante,
        )

        # Chequea disponibilidad usando la función única de dominio
        disponible, conflictos = verificar_superposicion_y_disponibilidad(
            unidad_id=unidad_id,
            inicio=inicio,
            fin=fin,
            reservas_existentes=self.repo.obtener_todas(),
            ahora=ahora,
            unidades_validas=unidades_validas,
        )

        if not disponible:
            raise ErrorDominio(
                f"La unidad '{unidad_id}' no está disponible en el intervalo indicado. "
                f"Existe(n) {len(conflictos)} reserva(s) en conflicto."
            )

        assert solicitante_limpio is not None
        return self.repo.agregar(
            unidad=unidad_id,
            solicitante=solicitante_limpio,
            inicio=inicio,
            fin=fin,
            creada_en=ahora,
        )
