"""Pruebas de persistencia SQLite para CA6, CA8 y CA10."""

from datetime import datetime

import pytest

from reservas.dominio import ErrorDominio, EstadoReserva, TZ_ARG
from reservas.inventario import Inventario
from reservas.persistencia import RepositorioSQLite
from reservas.servicio import ServicioReservas


@pytest.fixture
def inventario():
    return Inventario.cargar_desde_archivo("data/inventario.json")


@pytest.fixture
def reloj():
    return lambda: datetime(2026, 11, 1, 8, 0, tzinfo=TZ_ARG)


def servicio(ruta, inventario, reloj):
    return ServicioReservas(inventario, RepositorioSQLite(ruta), reloj)


def crear(servicio, unidad="MIC-01", inicio="2026-11-03 10:00", fin="2026-11-03 11:00"):
    return servicio.reservar(unidad, "Ana Pérez", inicio, fin)


def test_r7_ca6_cancelar_libera_intervalo_y_conserva_historial(tmp_path, inventario, reloj):
    app = servicio(tmp_path / "reservas.db", inventario, reloj)
    original = crear(app)

    cancelada = app.cancelar(original.id)
    assert cancelada.estado == EstadoReserva.CANCELADA
    assert cancelada.cancelada_en == reloj()
    assert (cancelada.unidad, cancelada.solicitante, cancelada.inicio, cancelada.fin) == (
        original.unidad, original.solicitante, original.inicio, original.fin
    )
    assert app.listar() == [cancelada]
    assert crear(app, inicio="2026-11-03 10:30", fin="2026-11-03 11:30").id == 2
    with pytest.raises(ErrorDominio):
        app.cancelar(original.id)
    with pytest.raises(ErrorDominio):
        app.cancelar(99)


def test_r9_ca8_reabrir_instancia_conserva_activas_y_canceladas(tmp_path, inventario, reloj):
    ruta = tmp_path / "reservas.db"
    primera = servicio(ruta, inventario, reloj)
    activa = crear(primera)
    cancelada = crear(primera, unidad="MIC-02")
    primera.cancelar(cancelada.id)

    segunda = servicio(ruta, inventario, reloj)
    reservas = segunda.listar()
    assert [reserva.id for reserva in reservas] == [activa.id, cancelada.id]
    assert [reserva.estado for reserva in reservas] == [EstadoReserva.ACTIVA, EstadoReserva.CANCELADA]


def test_r11_ca10_reinicio_sin_confirmar_no_borra_y_confirmado_borra(tmp_path, inventario, reloj):
    app = servicio(tmp_path / "reservas.db", inventario, reloj)
    crear(app)
    app.reiniciar_datos()
    assert len(app.listar()) == 1
    app.reiniciar_datos(confirmar=True)
    assert app.listar() == []


def test_r9_abrir_base_existente_no_borra_datos(tmp_path, inventario, reloj):
    ruta = tmp_path / "reservas.db"
    primero = servicio(ruta, inventario, reloj)
    esperada = crear(primero)

    repositorio_nuevo = RepositorioSQLite(ruta)
    assert repositorio_nuevo.obtener_todas() == [esperada]


def test_r3_rechaza_superposicion_parcial(tmp_path, inventario, reloj):
    """CA2 / R3: SQLite rechaza una superposición parcial dentro de la transacción."""
    app = servicio(tmp_path / "reservas.db", inventario, reloj)
    crear(app)
    with pytest.raises(ErrorDominio, match="no está disponible"):
        crear(app, inicio="2026-11-03 10:30", fin="2026-11-03 11:30")
    assert len(app.listar()) == 1
