import os
# --- IMPORTACIÓN OBLIGATORIA ---
# Traemos la función que lee los datos desde el módulo de almacenamiento.
# Sin esto, 'consolidar_libros_recursivamente' no está definido.
from almacenamiento import consolidar_libros_recursivamente

def ordenar_libros(base_path: str):
    """
    Permite ordenar la lista completa de ítems (obtenida recursivamente)
    alfabéticamente por Título o numéricamente por Año.
    
    Esta función es llamada por la Opción 6 del menú en main.py.
    """
    
    # 1. Obtener la lista global de datos de la función recursiva
    # Esta línea ahora funciona gracias a la importación
    lista_libros = consolidar_libros_recursivamente(base_path, [])
    
    if not lista_libros:
        print("\nNo hay libros registrados para ordenar.")
        return

    print("\n⬆️ ORDENAR LISTA GLOBAL DE LIBROS\n")
    print("¿Cómo deseas ordenar la lista?")
    print("1. Alfabéticamente (por Título)")
    print("2. Por Año de publicación")
    
    opcion = input("Elegí una opción (1 o 2): ")
    
    clave_orden = None
    es_numerico = False

    if opcion == "1":
        clave_orden = "titulo"
        print("Ordenando alfabéticamente por Título...")
    elif opcion == "2":
        clave_orden = "anio"
        es_numerico = True
        print("Ordenando por Año de publicación...")
    else:
        print("Opción no válida. Operación cancelada.")
        return

    # 2. Preguntar orden ascendente o descendente
    orden_str = input("¿Orden ascendente (a) o descendente (d)? ").lower().strip()
    # Si el usuario escribe 'd', reverse será True.
    invertir_orden = orden_str == 'd'

    # 3. Aplicar el ordenamiento usando 'key' y lambda
    try:
        if es_numerico:
            # Para 'Año', aseguramos la conversión a entero para un orden numérico correcto
            # Usamos .get() para evitar errores si falta la clave, aunque no debería
            lista_libros.sort(key=lambda libro: int(libro.get(clave_orden, 0)), reverse=invertir_orden)
        else:
            # Para 'Título', usamos .lower() para un orden alfabético que no distinga mayúsculas
            lista_libros.sort(key=lambda libro: str(libro.get(clave_orden, "")).lower(), reverse=invertir_orden)
            
    except ValueError:
        print("Error: Se encontró un dato no numérico al intentar ordenar por año.")
        return
    except Exception as e:
        print(f"Error inesperado durante el ordenamiento: {e}")
        return

    # 4. Mostrar el resultado
    print(f"\n--- Libros Ordenados por {clave_orden.capitalize()} ({'Descendente' if invertir_orden else 'Ascendente'}) ---")
    for i, libro in enumerate(lista_libros, start=1):
        print(f"[{i}] {libro['titulo']} ({libro['autor']})")
        print(f"    └─ Año: {libro['anio']} | Páginas: {libro['paginas']} | Género: {libro['genero']}")
    print("--------------------------------------------------")

# (No agregues más código a este archivo a menos que sea otra función de ordenamiento)