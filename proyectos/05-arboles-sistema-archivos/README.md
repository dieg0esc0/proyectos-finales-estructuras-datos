# Proyecto 5 — Árboles: Sistema de archivos

## Objetivo

Simular un sistema de archivos mediante un árbol binario de búsqueda (ABB). Cada nodo representa un archivo o directorio y los elementos se ordenan alfabéticamente por nombre.

## Funciones

- Crear directorios e insertar archivos.
- Buscar por nombre y mostrar información completa.
- Eliminar archivos o directorios vacíos.
- Mostrar recorridos inorden, preorden y postorden.
- Rechazar duplicados, nombres vacíos, tamaños negativos y archivos sin extensión.
- Proteger el directorio raíz.
- Impedir que un archivo tenga elementos descendientes.

## Estructura

- `main.py`: menú interactivo y punto de entrada.
- `src/arbol_sistema_archivos.py`: operaciones del ABB.
- `src/nodo_archivo.py`: información y enlaces de cada nodo.
- `src/tipo_elemento.py`: tipos `DIRECTORIO` y `ARCHIVO`.
- `src/resultado_operacion.py`: resultado y mensaje de cada operación.
- `tests/test_arbol_sistema_archivos.py`: pruebas automatizadas.

## Requisitos

- Python 3.8 o posterior.
- No requiere instalar paquetes externos.

## Ejecutar

Desde esta carpeta:

```bash
python3 main.py
```

La raíz se crea automáticamente con el nombre `Documentos`.

## Ejecutar pruebas

```bash
python3 -m unittest discover -s tests -v
```

## Casos de prueba manuales

1. Crear los directorios `Aplicaciones` y `Fotos`.
2. Insertar `Carta.txt` con tamaño 2500 bytes.
3. Buscar `carta` para comprobar que la búsqueda no distingue mayúsculas.
4. Intentar insertar otro elemento llamado `Carta`; debe rechazarse.
5. Intentar insertar un archivo sin extensión o con tamaño negativo; debe rechazarse.
6. Mostrar los tres recorridos y comprobar que todos presentan nombre, extensión, tamaño y tipo.
7. Intentar eliminar `Documentos`; debe rechazarse por ser la raíz.
8. Intentar eliminar un directorio que tenga hijos; debe rechazarse.

## Aclaración del diseño

El enunciado exige simultáneamente un ABB global y que un archivo siempre sea hoja. Por ello, si la ruta alfabética de una inserción llega a un archivo, la operación se rechaza con el mensaje indicado por el enunciado. La eliminación contiene el algoritmo tradicional para cero, uno y dos hijos; la validación externa impide eliminar la raíz y directorios que aún contienen elementos.
