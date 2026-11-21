from typing import List

from src import ArbolSistemaArchivos, NodoArchivo


def mostrar_menu() -> None:
    print("=== SISTEMA DE ARCHIVOS (ABB) ===")
    print("1. Crear directorio")
    print("2. Insertar archivo")
    print("3. Buscar elemento por nombre")
    print("4. Eliminar archivo o directorio")
    print("5. Mostrar información de un elemento")
    print("6. Mostrar recorrido inorden")
    print("7. Mostrar recorrido preorden")
    print("8. Mostrar recorrido postorden")
    print("0. Salir")


def leer_entero(mensaje: str) -> int:
    while True:
        try:
            return int(input(mensaje).strip())
        except ValueError:
            print("Ingrese un número entero válido.")


def imprimir_recorrido(nombre: str, elementos: List[NodoArchivo]) -> None:
    print(f"--- RECORRIDO {nombre} ---")
    for elemento in elementos:
        print(elemento)


def ejecutar_menu(sistema: ArbolSistemaArchivos) -> None:
    while True:
        mostrar_menu()
        opcion = leer_entero("Seleccione una opción: ")
        print()

        if opcion == 1:
            nombre = input("Nombre del directorio: ")
            print(sistema.insertar_directorio(nombre).mensaje)
        elif opcion == 2:
            nombre = input("Nombre del archivo (sin extensión): ")
            extension = input("Extensión: ")
            tamano = leer_entero("Tamaño en bytes: ")
            print(sistema.insertar_archivo(nombre, extension, tamano).mensaje)
        elif opcion == 3:
            encontrado = sistema.buscar(input("Nombre a buscar: "))
            if encontrado is None:
                print("El elemento no existe en el sistema de archivos.")
            else:
                print(f"Elemento encontrado: {encontrado.nombre_completo}")
        elif opcion == 4:
            nombre = input("Nombre a eliminar: ")
            print(sistema.eliminar(nombre).mensaje)
        elif opcion == 5:
            encontrado = sistema.buscar(input("Nombre del elemento: "))
            if encontrado is None:
                print("El elemento no existe en el sistema de archivos.")
            else:
                print(encontrado)
        elif opcion == 6:
            imprimir_recorrido("INORDEN", sistema.recorrido_inorden())
        elif opcion == 7:
            imprimir_recorrido("PREORDEN", sistema.recorrido_preorden())
        elif opcion == 8:
            imprimir_recorrido("POSTORDEN", sistema.recorrido_postorden())
        elif opcion == 0:
            print("Programa finalizado.")
            return
        else:
            print("Opción no válida.")
        print()


def main() -> None:
    ejecutar_menu(ArbolSistemaArchivos("Documentos"))


if __name__ == "__main__":
    main()
