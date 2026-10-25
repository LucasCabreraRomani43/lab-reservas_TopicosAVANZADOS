import pytest
from datetime import datetime
from reservas.inventario import Inventario, ErrorInventario
from reservas.dominio import (
    ErrorDominio,
    EstadoReserva,
    TZ_ARG,
    parsear_fecha,
)
from reservas.servicio import ServicioReservas, RepositorioEnMemoria


@pytest.fixture
def reloj_fijo():
    """Reloj de referencia fijado en 2026-11-01 08:00 -03:00 según AGENTS.md y especificación."""
    return lambda: datetime(2026, 11, 1, 8, 0, tzinfo=TZ_ARG)


@pytest.fixture
def inventario_real():
    return Inventario.cargar_desde_archivo("data/inventario.json")


@pytest.fixture
def servicio(inventario_real, reloj_fijo):
    repo = RepositorioEnMemoria()
    return ServicioReservas(inventario=inventario_real, repositorio=repo, reloj=reloj_fijo)


def test_r1_ca9_carga_inventario():
    """
    CA9 / R1: Al iniciar se leen las 5 unidades de data/inventario.json;
    `unidades` las lista con ID y equipo. Si el archivo falta o es inválido, error claro.
    """
    inv = Inventario.cargar_desde_archivo("data/inventario.json")
    unidades = inv.listar()
    assert len(unidades) == 5
    ids = {u.id for u in unidades}
    assert ids == {"MIC-01", "MIC-02", "OSC-01", "MUL-01", "FUE-01"}

    # Error claro si el archivo no existe
    with pytest.raises(ErrorInventario) as exc_info:
        Inventario.cargar_desde_archivo("data/archivo_inexistente.json")
    assert "No se encontró el archivo de inventario" in str(exc_info.value)

    # Error claro si el archivo es JSON inválido
    import tempfile
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False) as f:
        f.write("{invalido json")
        temp_name = f.name
    with pytest.raises(ErrorInventario) as exc_info:
        Inventario.cargar_desde_archivo(temp_name)
    assert "no es un JSON válido" in str(exc_info.value)

    # Error claro si la estructura no es una lista
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False) as f:
        f.write('{"id": "MIC-01"}')
        temp_name2 = f.name
    with pytest.raises(ErrorInventario) as exc_info:
        Inventario.cargar_desde_archivo(temp_name2)
    assert "debe contener una lista de unidades" in str(exc_info.value)


def test_r2_ca1_crear_primera_reserva(servicio):
    """
    CA1 / R2: Sin reservas: MIC-01, 'Ana Pérez', 2026-11-03 10:00–11:00 -> aceptada, ID 1, ACTIVA.
    """
    reserva = servicio.reservar(
        unidad_id="MIC-01",
        solicitante="Ana Pérez",
        inicio_str="2026-11-03 10:00",
        fin_str="2026-11-03 11:00",
    )
    assert reserva.id == 1
    assert reserva.unidad == "MIC-01"
    assert reserva.solicitante == "Ana Pérez"
    assert reserva.inicio == parsear_fecha("2026-11-03 10:00")
    assert reserva.fin == parsear_fecha("2026-11-03 11:00")
    assert reserva.estado == EstadoReserva.ACTIVA
    assert reserva.creada_en == datetime(2026, 11, 1, 8, 0, tzinfo=TZ_ARG)


def test_r3_r8_ca2_ca7_rechaza_superposiciones(servicio):
    """
    CA2 / R3 y CA7 / R8:
    Con CA1 existente (MIC-01 10:00-11:00):
    - 10:30–11:30 (superposición fin)
    - 09:30–10:30 (superposición inicio)
    - 09:00–12:00 (contiene a la existente)
    - 10:15–10:45 (contenida en la existente)
    - 10:00–11:00 (exactamente igual)
    Todas rechazadas.
    La disponibilidad coincide en todos los casos (CA7).
    """
    # Establecer CA1
    servicio.reservar(
        unidad_id="MIC-01",
        solicitante="Ana Pérez",
        inicio_str="2026-11-03 10:00",
        fin_str="2026-11-03 11:00",
    )

    intervalos_conflicto = [
        ("2026-11-03 10:30", "2026-11-03 11:30"),
        ("2026-11-03 09:30", "2026-11-03 10:30"),
        ("2026-11-03 09:00", "2026-11-03 12:00"),
        ("2026-11-03 10:15", "2026-11-03 10:45"),
        ("2026-11-03 10:00", "2026-11-03 11:00"),
    ]

    for ini, fin in intervalos_conflicto:
        # Verificar CA7: disponibilidad es False y lista la reserva en conflicto
        disp, conflictos = servicio.disponibilidad("MIC-01", ini, fin)
        assert disp is False
        assert len(conflictos) == 1
        assert conflictos[0].id == 1

        # Verificar CA2: intentar reservar falla con ErrorDominio
        with pytest.raises(ErrorDominio):
            servicio.reservar(
                unidad_id="MIC-01",
                solicitante="Otro Usuario",
                inicio_str=ini,
                fin_str=fin,
            )


def test_r4_r8_ca3_ca7_acepta_consecutivas(servicio):
    """
    CA3 / R4 y CA7 / R8:
    Con CA1 (MIC-01 10:00–11:00):
    - MIC-01 11:00–12:00 (consecutiva posterior)
    - MIC-01 09:00–10:00 (consecutiva anterior)
    Ambas aceptadas. Turnos consecutivos NO se superponen.
    La disponibilidad coincide (CA7).
    """
    servicio.reservar(
        unidad_id="MIC-01",
        solicitante="Ana Pérez",
        inicio_str="2026-11-03 10:00",
        fin_str="2026-11-03 11:00",
    )

    # 1. Consecutiva posterior (11:00 - 12:00)
    disp_post, conf_post = servicio.disponibilidad("MIC-01", "2026-11-03 11:00", "2026-11-03 12:00")
    assert disp_post is True
    assert len(conf_post) == 0

    r2 = servicio.reservar(
        unidad_id="MIC-01",
        solicitante="Carlos Gómez",
        inicio_str="2026-11-03 11:00",
        fin_str="2026-11-03 12:00",
    )
    assert r2.id == 2
    assert r2.estado == EstadoReserva.ACTIVA

    # 2. Consecutiva anterior (09:00 - 10:00)
    disp_ant, conf_ant = servicio.disponibilidad("MIC-01", "2026-11-03 09:00", "2026-11-03 10:00")
    assert disp_ant is True
    assert len(conf_ant) == 0

    r3 = servicio.reservar(
        unidad_id="MIC-01",
        solicitante="Lucía Méndez",
        inicio_str="2026-11-03 09:00",
        fin_str="2026-11-03 10:00",
    )
    assert r3.id == 3
    assert r3.estado == EstadoReserva.ACTIVA


def test_r5_r8_ca4_ca7_acepta_simultaneas_distintas_unidades(servicio):
    """
    CA4 / R5 y CA7 / R8:
    Con CA1 (MIC-01 10:00–11:00):
    - MIC-02 10:00–11:00 -> aceptada.
    La disponibilidad coincide (CA7).
    """
    servicio.reservar(
        unidad_id="MIC-01",
        solicitante="Ana Pérez",
        inicio_str="2026-11-03 10:00",
        fin_str="2026-11-03 11:00",
    )

    disp, conflictos = servicio.disponibilidad("MIC-02", "2026-11-03 10:00", "2026-11-03 11:00")
    assert disp is True
    assert len(conflictos) == 0

    r2 = servicio.reservar(
        unidad_id="MIC-02",
        solicitante="Esteban Ruiz",
        inicio_str="2026-11-03 10:00",
        fin_str="2026-11-03 11:00",
    )
    assert r2.id == 2
    assert r2.unidad == "MIC-02"
    assert r2.estado == EstadoReserva.ACTIVA


def test_r6_ca5_rechaza_entradas_invalidas(servicio):
    """
    CA5 / R6:
    Cada entrada inválida de R6 -> rechazada; la cantidad de reservas no cambia.
    - unidad desconocida
    - solicitante vacío o solo espacios
    - fecha u hora mal formada o inexistente (2026-02-30 10:00, 2026-11-03 25:00)
    - inicio igual o posterior al fin
    - inicio en el pasado respecto al reloj
    """
    # Estado inicial: 0 reservas
    assert len(servicio.repo.obtener_todas()) == 0

    # 1. Unidad desconocida
    with pytest.raises(ErrorDominio) as exc:
        servicio.reservar("NO-EXISTE", "Ana", "2026-11-03 10:00", "2026-11-03 11:00")
    assert "Unidad desconocida" in str(exc.value)

    # 2. Solicitante vacío o solo espacios
    for sol in ["", "   ", "\t\n"]:
        with pytest.raises(ErrorDominio) as exc:
            servicio.reservar("MIC-01", sol, "2026-11-03 10:00", "2026-11-03 11:00")
        assert "solicitante no puede estar vacío" in str(exc.value)

    # 3. Fecha u hora mal formada o inexistente
    casos_fechas_malformadas = [
        ("2026-02-30 10:00", "2026-02-30 11:00"),  # 30 de febrero no existe
        ("2026-11-03 25:00", "2026-11-03 26:00"),  # hora 25 no existe
        ("2026-11-03 10:65", "2026-11-03 11:00"),  # minuto 65 no existe
        ("texto-invalido", "2026-11-03 11:00"),    # formato no datetime
        ("03/11/2026 10:00", "03/11/2026 11:00"),  # formato dd/mm/aaaa no permitido
    ]
    for ini, fin in casos_fechas_malformadas:
        with pytest.raises(ErrorDominio) as exc:
            servicio.reservar("MIC-01", "Ana", ini, fin)
        assert "inválido o inexistente" in str(exc.value)

    # 4. Inicio igual o posterior a fin
    with pytest.raises(ErrorDominio) as exc:
        servicio.reservar("MIC-01", "Ana", "2026-11-03 10:00", "2026-11-03 10:00")
    assert "anterior al horario de fin" in str(exc.value)

    with pytest.raises(ErrorDominio) as exc:
        servicio.reservar("MIC-01", "Ana", "2026-11-03 11:00", "2026-11-03 10:00")
    assert "anterior al horario de fin" in str(exc.value)

    # 5. Inicio en el pasado (reloj está en 2026-11-01 08:00)
    with pytest.raises(ErrorDominio) as exc:
        servicio.reservar("MIC-01", "Ana", "2026-11-01 07:59", "2026-11-01 09:00")
    assert "en el pasado" in str(exc.value)

    # También verificar que disponibilidad rechaza inicio en el pasado y unidad desconocida
    with pytest.raises(ErrorDominio):
        servicio.disponibilidad("MIC-01", "2026-11-01 07:59", "2026-11-01 09:00")
    with pytest.raises(ErrorDominio):
        servicio.disponibilidad("NO-EXISTE", "2026-11-03 10:00", "2026-11-03 11:00")

    # Invariante: no se creó ninguna reserva
    assert len(servicio.repo.obtener_todas()) == 0


def test_r2_s6_solicitante_se_guarda_sin_espacios(servicio):
    """S6: El solicitante se guarda sin espacios al inicio ni al final."""
    reserva = servicio.reservar(
        unidad_id="MIC-01",
        solicitante="   Ana María Pérez   ",
        inicio_str="2026-11-03 10:00",
        fin_str="2026-11-03 11:00",
    )
    assert reserva.solicitante == "Ana María Pérez"
