import json
from dataclasses import dataclass
from pathlib import Path


class ErrorInventario(Exception):
    """Excepción para errores al cargar o validar el inventario."""
    pass


@dataclass(frozen=True)
class Unidad:
    """Representa una unidad de equipo del laboratorio."""
    id: str
    equipo: str


class Inventario:
    """Gestiona el conjunto de unidades disponibles en el laboratorio."""

    def __init__(self, unidades: list[Unidad]):
        self._unidades = {u.id: u for u in unidades}

    @classmethod
    def cargar_desde_archivo(cls, ruta: str | Path = "data/inventario.json") -> "Inventario":
        path = Path(ruta)
        if not path.exists():
            raise ErrorInventario(f"No se encontró el archivo de inventario en '{ruta}'")

        try:
            with open(path, "r", encoding="utf-8") as f:
                datos = json.load(f)
        except json.JSONDecodeError as e:
            raise ErrorInventario(
                f"El archivo de inventario en '{ruta}' no es un JSON válido: {e}"
            ) from e
        except Exception as e:
            raise ErrorInventario(
                f"Error al abrir o leer el archivo de inventario en '{ruta}': {e}"
            ) from e

        if not isinstance(datos, list):
            raise ErrorInventario(
                f"El archivo de inventario en '{ruta}' debe contener una lista de unidades"
            )

        unidades: list[Unidad] = []
        for index, item in enumerate(datos):
            if not isinstance(item, dict) or "id" not in item or "equipo" not in item:
                raise ErrorInventario(
                    f"Elemento #{index + 1} inválido en inventario: debe contener 'id' y 'equipo'"
                )
            unidades.append(Unidad(id=str(item["id"]), equipo=str(item["equipo"])))

        return cls(unidades)

    def listar(self) -> list[Unidad]:
        return list(self._unidades.values())

    def obtener(self, unidad_id: str) -> Unidad | None:
        return self._unidades.get(unidad_id)

    def existe(self, unidad_id: str) -> bool:
        return unidad_id in self._unidades

    def ids(self) -> set[str]:
        return set(self._unidades.keys())
