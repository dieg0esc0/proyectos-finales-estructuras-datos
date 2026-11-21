from dataclasses import dataclass
from typing import Optional

from .tipo_elemento import TipoElemento


@dataclass
class NodoArchivo:
    nombre: str
    extension: str
    tamano_bytes: int
    tipo: TipoElemento
    hijo_izquierdo: Optional["NodoArchivo"] = None
    hijo_derecho: Optional["NodoArchivo"] = None

    @property
    def tiene_hijos(self) -> bool:
        return self.hijo_izquierdo is not None or self.hijo_derecho is not None

    @property
    def nombre_completo(self) -> str:
        if self.tipo is TipoElemento.ARCHIVO:
            return f"{self.nombre}.{self.extension}"
        return self.nombre

    def __str__(self) -> str:
        extension_visible = self.extension or "-"
        return (
            f"Nombre: {self.nombre} | Extensión: {extension_visible} | "
            f"Tamaño: {self.tamano_bytes} bytes | Tipo: {self.tipo.value}"
        )
