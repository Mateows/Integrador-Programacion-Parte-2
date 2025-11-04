from almacenamiento import consolidar_libros_recursivamente
from typing import List, Dict

def ordenar_libros(base_path: str):
    """
    Permite ordenar la lista completa de ítems por uno o dos atributos.
    """
    lista_libros = consolidar_libros_recursivamente(base_path, [])
    
    if not lista_libros:
        print("No hay libros para ordenar.")
        return

    print("\n⬆️ ORDENAR LIBROS\n")
    print("Atributos disponibles: titulo, paginas, genero, autor")
    
    clave1_str = input("Elegí el atributo principal para ordenar: ").lower().strip()
    clave2_str = input("Elegí el atributo secundario (opcional, dejar vacío): ").lower().strip()
    
    if clave1_str not in ["titulo", "paginas", "genero", "autor"]:
        print("Opción de ordenamiento principal inválida.")
        return

    orden_asc = input("Orden ascendente (asc) o descendente (desc)? ").lower().startswith('a')

    # Función auxiliar para obtener valores comparables
    def obtener_valor(libro, clave):
        valor = libro.get(clave, "")
        if clave == "paginas":
            try:
                return int(valor)
            except ValueError:
                return 0
        return str(valor).lower()

    # Ordenamiento
    if clave2_str in ["titulo", "paginas", "genero", "autor"]:
        lista_libros.sort(
            key=lambda x: (obtener_valor(x, clave1_str), obtener_valor(x, clave2_str)),
            reverse=not orden_asc
        )
        criterio = f"{clave1_str.capitalize()} y {clave2_str.capitalize()}"
    else:
        lista_libros.sort(key=lambda x: obtener_valor(x, clave1_str), reverse=not orden_asc)
        criterio = clave1_str.capitalize()

    # Mostrar resultado
    print(f"\nLista ordenada por {criterio} ({'Ascendente' if orden_asc else 'Descendente'}):")
    print("---")
    for i, libro in enumerate(lista_libros[:15], start=1):
        print(f"[{i}] {libro['titulo']} | Autor: {libro['autor']} | Páginas: {libro['paginas']}")
    print("---")

