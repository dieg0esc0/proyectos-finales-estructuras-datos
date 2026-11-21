import unittest

from src import ArbolSistemaArchivos


class ArbolSistemaArchivosTest(unittest.TestCase):
    def crear_arbol_base(self) -> ArbolSistemaArchivos:
        arbol = ArbolSistemaArchivos("M")
        self.assertTrue(arbol.insertar_directorio("G").exitosa)
        self.assertTrue(arbol.insertar_directorio("T").exitosa)
        self.assertTrue(arbol.insertar_archivo("A", "txt", 25).exitosa)
        self.assertTrue(arbol.insertar_archivo("H", ".pdf", 2500).exitosa)
        return arbol

    def test_insercion_busqueda_y_recorrido(self) -> None:
        arbol = self.crear_arbol_base()

        self.assertIs(arbol.buscar("m"), arbol.raiz)
        self.assertIsNotNone(arbol.buscar("A"))
        self.assertIsNone(arbol.buscar("inexistente"))
        self.assertEqual(
            ["A", "G", "H", "M", "T"],
            [nodo.nombre for nodo in arbol.recorrido_inorden()],
        )

    def test_validaciones(self) -> None:
        arbol = self.crear_arbol_base()

        self.assertFalse(arbol.insertar_directorio("g").exitosa)
        self.assertFalse(arbol.insertar_archivo("SinExtension", "", 10).exitosa)
        self.assertFalse(arbol.insertar_archivo("Negativo", "txt", -1).exitosa)
        self.assertFalse(arbol.insertar_directorio(" ").exitosa)
        self.assertFalse(arbol.insertar_directorio("I").exitosa)

    def test_eliminacion(self) -> None:
        arbol = self.crear_arbol_base()

        self.assertFalse(arbol.eliminar("M").exitosa)
        self.assertFalse(arbol.eliminar("G").exitosa)
        self.assertTrue(arbol.eliminar("T").exitosa)
        self.assertIsNone(arbol.buscar("T"))
        self.assertTrue(arbol.eliminar("A").exitosa)
        self.assertIsNone(arbol.buscar("A"))

    def test_tipos_de_entrada(self) -> None:
        arbol = ArbolSistemaArchivos("Raiz")
        self.assertFalse(arbol.insertar_directorio(None).exitosa)
        self.assertFalse(arbol.insertar_archivo("A", None, 10).exitosa)
        self.assertFalse(arbol.insertar_archivo("A", "txt", 1.5).exitosa)


if __name__ == "__main__":
    unittest.main()
