from dataclasses import dataclass


@dataclass(frozen=True)
class ResultadoOperacion:
    exitosa: bool
    mensaje: str

    @classmethod
    def exito(cls, mensaje: str) -> "ResultadoOperacion":
        return cls(True, mensaje)

    @classmethod
    def error(cls, mensaje: str) -> "ResultadoOperacion":
        return cls(False, mensaje)
