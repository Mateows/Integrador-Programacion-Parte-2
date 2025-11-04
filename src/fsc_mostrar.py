# --- FUNCIONALIDADES (CRUD y Consultas) ---
from typing import List, Dict, Tuple
import os
import csv
from almacenamiento import consolidar_libros_recursivamente
import unicodedata
from difflib import SequenceMatcher


def normalizar_texto(texto: str) -> str:
    """Convierte texto a minúsculas y elimina acentos."""
    texto = texto.lower()
    texto = unicodedata.normalize('NFKD', texto)
    return ''.join(c for c in texto if not unicodedata.combining(c))


def son_similares(a: str, b: str, umbral: float = 0.6) -> bool:
    """Devuelve True si los textos son suficientemente parecidos (más flexible)."""
    a_norm, b_norm = normalizar_texto(a), normalizar_texto(b)
    
    # Coincidencia directa o parcial
    if a_norm in b_norm or b_norm in a_norm:
        return True
    
    # Coincidencia aproximada
    return SequenceMatcher(None, a_norm, b_norm).ratio() >= umbral



def mostrar_libros(base_path: str):
    """
    Muestra ítems totales y permite filtrado, usando la lectura recursiva.
    """
    lista_libros = consolidar_libros_recursivamente(base_path, []) 
    
    if not lista_libros:
        print("\nNo hay ítems registrados en la estructura de archivos.")
        return

    print("\n📚 LISTADO GLOBAL DE LIBROS\n")
    
    atributo_filtro = input("¿Desea filtrar la lista? (titulo/autor/genero/no): ").lower().strip()
    
    libros_a_mostrar = lista_libros
    
    if atributo_filtro in ["titulo", "autor", "genero"]:
        valor_filtro = input(f"Ingrese el valor a filtrar por {atributo_filtro}: ").strip()
        if valor_filtro:
            # 🔍 Búsqueda flexible (ahora más permisiva)
            libros_a_mostrar = [
                libro for libro in libros_a_mostrar
                if son_similares(valor_filtro, str(libro.get(atributo_filtro, "")))
            ]

            print(f"\nMostrando {len(libros_a_mostrar)} libros filtrados (búsqueda flexible).")

    if not libros_a_mostrar:
        print("No se encontraron libros con ese criterio de filtrado.")
        return

    print("---")
    for i, libro in enumerate(libros_a_mostrar, start=1):
        print(f"[{i}] ID: {libro['id']}")
        print(f"    Título: {libro['titulo']} ({libro['paginas']} pgs)")
        print(f"    Ubicación: {libro['genero']} / {libro['autor']} / {libro['anio']}")
        print("---")


def _seleccionar_item_por_id(base_path: str, operacion: str) -> Tuple[List[Dict], int]:
    """Función auxiliar para buscar un ítem por ID."""
    
    lista_libros = consolidar_libros_recursivamente(base_path, [])
    
    if not lista_libros:
        print("No hay libros registrados para esta operación.")
        return [], -1

    print(f"\n{operacion.upper()} LIBRO\n")
    print("Libros disponibles (ID: Genero/Autor/Titulo):")
    
    for i, libro in enumerate(lista_libros, start=1):
        print(f"[{i}] {libro.get('id', libro['titulo'])}") # Usamos .get() por seguridad
        
    try:
        indice = int(input(f"\nElegí el número del libro a {operacion}: "))
        if indice < 1 or indice > len(lista_libros):
            print("Número inválido.")
            return [], -1
    except ValueError:
        print("Debes ingresar un número.")
        return [], -1
        
    return lista_libros, indice - 1
