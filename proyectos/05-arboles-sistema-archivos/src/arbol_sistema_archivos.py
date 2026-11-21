from typing import List, Optional

from .nodo_archivo import NodoArchivo
from .resultado_operacion import ResultadoOperacion
from .tipo_elemento import TipoElemento


class ArbolSistemaArchivos:
    """Árbol binario de búsqueda ordenado por el nombre del elemento."""

    def __init__(self, nombre_raiz: str) -> None:
        nombre = self._normalizar_nombre(nombre_raiz)
        self.raiz = NodoArchivo(nombre, "", 0, TipoElemento.DIRECTORIO)

    def insertar_directorio(self, nombre: str) -> ResultadoOperacion:
        try:
            nuevo = NodoArchivo(
                self._normalizar_nombre(nombre),
                "",
                0,
                TipoElemento.DIRECTORIO,
            )
        except (TypeError, ValueError) as error:
            return ResultadoOperacion.error(str(error))
        return self._insertar(nuevo)

    def insertar_archivo(
        self, nombre: str, extension: str, tamano_bytes: int
    ) -> ResultadoOperacion:
        try:
            nombre_validado = self._normalizar_nombre(nombre)
            extension_validada = self._normalizar_extension(extension)
            if not isinstance(tamano_bytes, int):
                raise TypeError("El tamaño debe ser un número entero.")
            if tamano_bytes < 0:
                raise ValueError("El tamaño no puede ser negativo.")
            nuevo = NodoArchivo(
                nombre_validado,
                extension_validada,
                tamano_bytes,
                TipoElemento.ARCHIVO,
            )
        except (TypeError, ValueError) as error:
            return ResultadoOperacion.error(str(error))
        return self._insertar(nuevo)

    def _insertar(self, nuevo: NodoArchivo) -> ResultadoOperacion:
        actual = self.raiz

        while True:
            comparacion = self._comparar(nuevo.nombre, actual.nombre)
            if comparacion == 0:
                return ResultadoOperacion.error(
                    f"Ya existe un elemento con el nombre '{nuevo.nombre}'."
                )

            if actual.tipo is TipoElemento.ARCHIVO:
                return ResultadoOperacion.error(
                    "No se puede insertar el elemento: un archivo no puede "
                    "contener otros elementos."
                )

            if comparacion < 0:
                if actual.hijo_izquierdo is None:
                    actual.hijo_izquierdo = nuevo
                    break
                actual = actual.hijo_izquierdo
            else:
                if actual.hijo_derecho is None:
                    actual.hijo_derecho = nuevo
                    break
                actual = actual.hijo_derecho

        return ResultadoOperacion.exito(
            f"Elemento '{nuevo.nombre_completo}' insertado correctamente."
        )

    def buscar(self, nombre: str) -> Optional[NodoArchivo]:
        try:
            objetivo = self._normalizar_nombre(nombre)
        except (TypeError, ValueError):
            return None

        actual: Optional[NodoArchivo] = self.raiz
        while actual is not None:
            comparacion = self._comparar(objetivo, actual.nombre)
            if comparacion == 0:
                return actual
            if comparacion < 0:
                actual = actual.hijo_izquierdo
            else:
                actual = actual.hijo_derecho
        return None

    def eliminar(self, nombre: str) -> ResultadoOperacion:
        try:
            objetivo = self._normalizar_nombre(nombre)
        except (TypeError, ValueError) as error:
            return ResultadoOperacion.error(str(error))

        if self._comparar(objetivo, self.raiz.nombre) == 0:
            return ResultadoOperacion.error(
                "No se puede eliminar el directorio raíz."
            )

        encontrado = self.buscar(objetivo)
        if encontrado is None:
            return ResultadoOperacion.error(
                "El elemento no existe en el sistema de archivos."
            )
        if encontrado.tipo is TipoElemento.DIRECTORIO and encontrado.tiene_hijos:
            return ResultadoOperacion.error(
                "No se puede eliminar un directorio que contiene elementos."
            )

        self.raiz = self._eliminar_recursivo(self.raiz, objetivo)
        return ResultadoOperacion.exito(
            f"Elemento '{encontrado.nombre_completo}' eliminado."
        )

    def _eliminar_recursivo(
        self, nodo: Optional[NodoArchivo], nombre: str
    ) -> Optional[NodoArchivo]:
        """Eliminación tradicional de un ABB con cero, uno o dos hijos."""
        if nodo is None:
            return None

        comparacion = self._comparar(nombre, nodo.nombre)
        if comparacion < 0:
            nodo.hijo_izquierdo = self._eliminar_recursivo(
                nodo.hijo_izquierdo, nombre
            )
            return nodo
        if comparacion > 0:
            nodo.hijo_derecho = self._eliminar_recursivo(
                nodo.hijo_derecho, nombre
            )
            return nodo

        if nodo.hijo_izquierdo is None:
            return nodo.hijo_derecho
        if nodo.hijo_derecho is None:
            return nodo.hijo_izquierdo

        sucesor = self._minimo(nodo.hijo_derecho)
        reemplazo = NodoArchivo(
            sucesor.nombre,
            sucesor.extension,
            sucesor.tamano_bytes,
            sucesor.tipo,
            nodo.hijo_izquierdo,
            self._eliminar_recursivo(nodo.hijo_derecho, sucesor.nombre),
        )
        return reemplazo

    @staticmethod
    def _minimo(nodo: NodoArchivo) -> NodoArchivo:
        actual = nodo
        while actual.hijo_izquierdo is not None:
            actual = actual.hijo_izquierdo
        return actual

    def recorrido_inorden(self) -> List[NodoArchivo]:
        resultado: List[NodoArchivo] = []
        self._inorden(self.raiz, resultado)
        return resultado

    def recorrido_preorden(self) -> List[NodoArchivo]:
        resultado: List[NodoArchivo] = []
        self._preorden(self.raiz, resultado)
        return resultado

    def recorrido_postorden(self) -> List[NodoArchivo]:
        resultado: List[NodoArchivo] = []
        self._postorden(self.raiz, resultado)
        return resultado

    def _inorden(
        self, nodo: Optional[NodoArchivo], resultado: List[NodoArchivo]
    ) -> None:
        if nodo is None:
            return
        self._inorden(nodo.hijo_izquierdo, resultado)
        resultado.append(nodo)
        self._inorden(nodo.hijo_derecho, resultado)

    def _preorden(
        self, nodo: Optional[NodoArchivo], resultado: List[NodoArchivo]
    ) -> None:
        if nodo is None:
            return
        resultado.append(nodo)
        self._preorden(nodo.hijo_izquierdo, resultado)
        self._preorden(nodo.hijo_derecho, resultado)

    def _postorden(
        self, nodo: Optional[NodoArchivo], resultado: List[NodoArchivo]
    ) -> None:
        if nodo is None:
            return
        self._postorden(nodo.hijo_izquierdo, resultado)
        self._postorden(nodo.hijo_derecho, resultado)
        resultado.append(nodo)

    @staticmethod
    def _comparar(primero: str, segundo: str) -> int:
        primero_normalizado = primero.casefold()
        segundo_normalizado = segundo.casefold()
        return (primero_normalizado > segundo_normalizado) - (
            primero_normalizado < segundo_normalizado
        )

    @staticmethod
    def _normalizar_nombre(nombre: str) -> str:
        if not isinstance(nombre, str):
            raise TypeError("El nombre debe ser texto.")
        nombre_limpio = nombre.strip()
        if not nombre_limpio:
            raise ValueError("El nombre no puede estar vacío.")
        return nombre_limpio

    @staticmethod
    def _normalizar_extension(extension: str) -> str:
        if not isinstance(extension, str):
            raise TypeError("La extensión debe ser texto.")
        extension_limpia = extension.strip().lstrip(".")
        if not extension_limpia:
            raise ValueError("Un archivo debe tener extensión.")
        return extension_limpia
