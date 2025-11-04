from typing import Dict
from almacenamiento import consolidar_libros_recursivamente

def estadisticas(base_path: str):
    """
    Calcula y muestra estadísticas básicas globales sobre los libros almacenados.
    """
    lista_libros = consolidar_libros_recursivamente(base_path, [])
    
    if not lista_libros:
        print("\nNo hay libros registrados para calcular estadísticas.")
        return

    print("\n📊 ESTADÍSTICAS GLOBALES DE LIBROS 📊\n")

    total_libros = len(lista_libros)
    total_paginas = 0
    libros_por_genero: Dict[str, int] = {}

    for libro in lista_libros:
        genero = libro['genero']
        libros_por_genero[genero] = libros_por_genero.get(genero, 0) + 1
        
        try:
            paginas = int(libro['paginas'])
            total_paginas += paginas
        except (ValueError, TypeError):
            pass

    promedio_paginas = total_paginas / total_libros if total_libros else 0
    libro_mas_largo = max(lista_libros, key=lambda x: int(x['paginas']), default=None)
    genero_mas_frecuente = max(libros_por_genero, key=libros_por_genero.get, default=None)

    print(f"📚 Total de libros registrados: {total_libros}")
    print(f"📄 Promedio de páginas por libro: {promedio_paginas:.2f}")
    print(f"🏆 Género más frecuente: {genero_mas_frecuente} ({libros_por_genero[genero_mas_frecuente]} libros)")
    
    if libro_mas_largo:
        print(f"📘 Libro con más páginas: '{libro_mas_largo['titulo']}' ({libro_mas_largo['paginas']} páginas)")

    print("\nRecuento por género:")
    for genero, count in sorted(libros_por_genero.items(), key=lambda item: item[1], reverse=True):
        print(f"  - {genero}: {count} libros")
    
    print("---------------------------------------")
