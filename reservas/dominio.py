from datetime import datetime, timezone, timedelta
from dataclasses import dataclass
from enum import Enum


# S1: Zona horaria única UTC−03:00 fija
TZ_ARG = timezone(timedelta(hours=-3))
FORMATO_FECHA = "%Y-%m-%d %H:%M"


class EstadoReserva(str, Enum):
    ACTIVA = "ACTIVA"
    CANCELADA = "CANCELADA"


class ErrorDominio(Exception):
    """Excepción base para errores de validación y reglas de negocio."""
    pass


def parsear_fecha(texto: str) -> datetime:
    """
    Parsea una fecha en formato AAAA-MM-DD HH:MM con zona UTC-03:00.
    Rechaza formatos inválidos, fechas inexistentes o fuera de rango.
    """
    if not isinstance(texto, str):
        raise ErrorDominio("La fecha debe ser una cadena de texto.")
    
    texto = texto.strip()
    try:
        dt = datetime.strptime(texto, FORMATO_FECHA)
    except ValueError as e:
        raise ErrorDominio(
            f"Formato de fecha u hora inválido o inexistente: '{texto}'. Debe ser AAAA-MM-DD HH:MM."
        ) from e
    
    # Asignar zona horaria UTC-03:00 fija
    return dt.replace(tzinfo=TZ_ARG)


def formatear_fecha(dt: datetime) -> str:
    """Devuelve la fecha en formato AAAA-MM-DD HH:MM en UTC-03:00."""
    return dt.astimezone(TZ_ARG).strftime(FORMATO_FECHA)


@dataclass(frozen=True)
class Reserva:
    id: int
    unidad: str
    solicitante: str
    inicio: datetime
    fin: datetime
    creada_en: datetime
    estado: EstadoReserva = EstadoReserva.ACTIVA
    cancelada_en: datetime | None = None


def validar_intervalo_y_solicitante(
    unidad_id: str,
    inicio: datetime,
    fin: datetime,
    ahora: datetime,
    unidades_validas: set[str],
    solicitante: str | None = None,
) -> str | None:
    """
    Valida las reglas de R6:
    - unidad conocida
    - solicitante no vacío ni solo espacios (si se proporciona)
    - inicio < fin
    - inicio no en el pasado respecto a 'ahora'
    
    Devuelve el solicitante sanitizado (strip) o None si solicitante era None.
    Lanza ErrorDominio si no cumple alguna validación.
    """
    if unidad_id not in unidades_validas:
        raise ErrorDominio(f"Unidad desconocida: '{unidad_id}'.")

    if solicitante is not None:
        solicitante_limpio = solicitante.strip()
        if not solicitante_limpio:
            raise ErrorDominio("El solicitante no puede estar vacío ni contener solo espacios.")
    else:
        solicitante_limpio = None

    if inicio >= fin:
        raise ErrorDominio("El horario de inicio debe ser anterior al horario de fin.")

    if inicio < ahora:
        raise ErrorDominio("El horario de inicio no puede ser en el pasado.")

    return solicitante_limpio


def verificar_superposicion_y_disponibilidad(
    unidad_id: str,
    inicio: datetime,
    fin: datetime,
    reservas_existentes: list[Reserva],
    ahora: datetime,
    unidades_validas: set[str],
) -> tuple[bool, list[Reserva]]:
    """
    Función única de dominio (Regla 3 de AGENTS.md / R3, R4, R5, R8).
    Valida el intervalo y unidad contra las reglas generales (R6) y luego
    determina si el intervalo [inicio, fin) para unidad_id está libre.
    
    Intervalo semiabierto [inicio, fin):
    Hay superposición si y solo si:
        existente.inicio < nueva.fin and nueva.inicio < existente.fin
    
    Solo bloquean reservas con estado ACTIVA (Regla 2 de AGENTS.md).
    Turnos consecutivos (existente.fin == nueva.inicio o nueva.fin == existente.inicio) NO se superponen (R4).
    Reservas de otra unidad NO interfieren (R5).
    
    Retorna: (disponible: bool, conflictos: list[Reserva])
    """
    validar_intervalo_y_solicitante(
        unidad_id=unidad_id,
        inicio=inicio,
        fin=fin,
        ahora=ahora,
        unidades_validas=unidades_validas,
        solicitante=None,
    )

    conflictos: list[Reserva] = []
    for r in reservas_existentes:
        if r.unidad == unidad_id and r.estado == EstadoReserva.ACTIVA:
            # Condición de superposición semiabierta [inicio, fin)
            if r.inicio < fin and inicio < r.fin:
                conflictos.append(r)

    disponible = len(conflictos) == 0
    return disponible, conflictos
