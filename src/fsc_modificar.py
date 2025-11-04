from typing import List, Dict, Tuple
from fsc_mostrar import _seleccionar_item_por_id
from fsc_guardado import guardar_datos_csv

def modificar_libro(base_path: str):
    """Modificación de Item (Update)"""
    
    lista_libros, indice_global = _seleccionar_item_por_id(base_path, "modificar")
    if indice_global == -1:
        return

    libro_a_modificar = lista_libros[indice_global]
    ruta_csv_original = libro_a_modificar['ruta_csv']
    
    print(f"\n✏️ Modificando: {libro_a_modificar['titulo']} ({libro_a_modificar['paginas']} páginas)")

    nuevo_titulo = input(f"Nuevo título (dejar vacío para no cambiar): ").strip()
    nuevas_paginas_str = input(f"Nuevas páginas (dejar vacío para no cambiar): ").strip()

    if nuevo_titulo:
        libro_a_modificar['titulo'] = nuevo_titulo
        libro_a_modificar['id'] = f"{libro_a_modificar['genero']}_{libro_a_modificar['autor']}_{nuevo_titulo}"

    if nuevas_paginas_str:
        try:
            paginas_int = int(nuevas_paginas_str)
            if paginas_int <= 0:
                print("❌ Las páginas deben ser un número positivo.")
                return
            libro_a_modificar['paginas'] = paginas_int
        except ValueError:
            print("❌ Las páginas deben ser un número entero.")
            return

    libros_mismo_csv = [lib for lib in lista_libros if lib['ruta_csv'] == ruta_csv_original]
    
    guardar_datos_csv(ruta_csv_original, libros_mismo_csv)
    print(f"\n✅ Libro '{libro_a_modificar['titulo']}' actualizado correctamente.")


def eliminar_libro(base_path: str):
    """Eliminación de Item (Delete)"""
    
    lista_libros, indice_global = _seleccionar_item_por_id(base_path, "eliminar")
    if indice_global == -1:
        return

    libro_a_eliminar = lista_libros[indice_global]
    ruta_csv_original = libro_a_eliminar['ruta_csv']

    confirm = input(f"¿Seguro que querés eliminar '{libro_a_eliminar['titulo']}'? (s/n): ").lower()
    if confirm != "s":
        print("Operación cancelada.")
        return

    libros_mismo_csv_actualizado = [
        lib for i, lib in enumerate(lista_libros)
        if lib['ruta_csv'] == ruta_csv_original and i != indice_global
    ]
    
    try:
        guardar_datos_csv(ruta_csv_original, libros_mismo_csv_actualizado)
        print(f"\n✅ Libro '{libro_a_eliminar['titulo']}' eliminado correctamente.")
    except Exception as e:
        print(f"\n❌ Falló la eliminación. Problemas de escritura en {ruta_csv_original}: {e}")
