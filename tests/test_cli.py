"""CA8, CA9 y CA10: interfaz de consola en procesos separados."""

import os
import subprocess
import sys
from pathlib import Path


RAIZ = Path(__file__).resolve().parents[1]


def ejecutar(db: Path, *argumentos: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "reservas", "--db", str(db), *argumentos],
        cwd=RAIZ,
        text=True,
        capture_output=True,
        check=False,
    )


def test_r9_ca8_persistencia_entre_procesos_con_cancelacion(tmp_path):
    db = tmp_path / "reservas.db"
    crear_dos = subprocess.run(
        [
            sys.executable, "-c",
            "from reservas.cli import main; "
            "raise SystemExit(max(main(['--db', r'" + str(db) + "', 'reservar', '--unidad', 'MIC-01', '--solicitante', 'Ana Pérez', '--inicio', '2099-11-03 10:00', '--fin', '2099-11-03 11:00']), "
            "main(['--db', r'" + str(db) + "', 'reservar', '--unidad', 'MIC-02', '--solicitante', 'Luis', '--inicio', '2099-11-03 10:00', '--fin', '2099-11-03 11:00'])))",
        ],
        cwd=RAIZ,
        text=True,
        capture_output=True,
        check=False,
    )
    assert crear_dos.returncode == 0, crear_dos.stderr

    cancelacion = ejecutar(db, "cancelar", "--id", "1")
    assert cancelacion.returncode == 0, cancelacion.stderr

    listado = ejecutar(db, "listar")
    assert listado.returncode == 0, listado.stderr
    assert "ID: 1 | Unidad: MIC-01 | Solicitante: Ana Pérez" in listado.stdout
    assert "Estado: CANCELADA" in listado.stdout
    assert "ID: 2 | Unidad: MIC-02 | Solicitante: Luis" in listado.stdout
    assert "Estado: ACTIVA" in listado.stdout


def test_r1_ca9_unidades_lista_los_cinco_ids_del_inventario(tmp_path):
    resultado = ejecutar(tmp_path / "reservas.db", "unidades")
    assert resultado.returncode == 0, resultado.stderr
    ids = [line.split(" | ", 1)[0] for line in resultado.stdout.splitlines()]
    assert ids == ["MIC-01", "MIC-02", "OSC-01", "MUL-01", "FUE-01"]


def test_r11_ca10_reinicio_sin_confirmar_conserva_datos(tmp_path):
    db = tmp_path / "reservas.db"
    crear = ejecutar(
        db, "reservar", "--unidad", "MIC-01", "--solicitante", "Ana",
        "--inicio", "2099-11-03 10:00", "--fin", "2099-11-03 11:00",
    )
    assert crear.returncode == 0, crear.stderr

    reiniciar = ejecutar(db, "reiniciar-datos")
    assert reiniciar.returncode == 0, reiniciar.stderr
    listado = ejecutar(db, "listar")
    assert listado.returncode == 0, listado.stderr
    assert "ID: 1 | Unidad: MIC-01 | Solicitante: Ana" in listado.stdout


def test_r6_entrada_invalida_devuelve_uno_y_comando_desconocido_dos(tmp_path):
    db = tmp_path / "reservas.db"
    invalida = ejecutar(
        db, "reservar", "--unidad", "MIC-01", "--solicitante", "Ana",
        "--inicio", "2099-02-30 10:00", "--fin", "2099-03-01 11:00",
    )
    assert invalida.returncode == 1
    assert "Error:" in invalida.stderr

    incorrecto = ejecutar(db, "reservass")
    assert incorrecto.returncode == 2


def test_r9_db_admite_variable_de_entorno(tmp_path):
    db = tmp_path / "desde-entorno.db"
    entorno = os.environ.copy()
    entorno["RESERVAS_DB"] = str(db)
    resultado = subprocess.run(
        [sys.executable, "-m", "reservas", "listar"], cwd=RAIZ, text=True,
        capture_output=True, check=False, env=entorno,
    )
    assert resultado.returncode == 0, resultado.stderr
    assert db.exists()
