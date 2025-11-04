import os
import csv
from typing import List, Dict, Tuple, Any, Optional

# --- LECTURA RECURSIVA OBLIGATORIA (Fase 2, Punto 2) ---

def leer_csv_a_diccionarios(ruta_csv: str, niveles_jerarquia: Dict[str, str]) -> List[Dict]:
    """Lee un CSV y lo convierte en lista de diccionarios, incluyendo la jerarquía."""
    libros_list = []
    
    try:
        with open(ruta_csv, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            headers = next(reader, None) # Saltar encabezado (Título, Páginas)
            
            if not headers or len(headers) < 2:
                return libros_list

            for fila in reader:
                if len(fila) >= 2:
                    try:
                        paginas_int = int(fila[1])
                    except ValueError:
                        continue # Ignorar fila si las páginas no son un número
                        
                    # Crear el diccionario (el patrón de datos exigido)
                    libros_list.append({
                        "genero": niveles_jerarquia['genero'], 
                        "autor": niveles_jerarquia['autor'], 
                        "anio": niveles_jerarquia['anio'],
                        "titulo": fila[0],
                        "paginas": paginas_int,
                        # ID simple para identificación en CRUD
                        "id": f"{niveles_jerarquia['genero']}/{niveles_jerarquia['autor']}/{fila[0]}", 
                        "ruta_csv": ruta_csv # Para saber dónde sobrescribir
                    })
                        
    except FileNotFoundError:
        pass 
    except OSError:
        pass 
        
    return libros_list


def consolidar_libros_recursivamente(ruta_actual: str, lista_global: List[Dict]) -> List[Dict]:
    """
    Función recursiva OBLIGATORIA (Fase 2) para recorrer la jerarquía y consolidar los datos.
    """
    
    # 1. Caso Base 1: Encontrar el archivo CSV
    if os.path.basename(ruta_actual) == "items.csv":
        partes = ruta_actual.split(os.sep)
        # Tomamos los 3 niveles (Genero/Autor/Anio) antes de items.csv
        if len(partes) >= 4:
            niveles_jerarquia = {
                'genero': partes[-4],
                'autor': partes[-3],
                'anio': partes[-2],
            }
            libros_csv = leer_csv_a_diccionarios(ruta_actual, niveles_jerarquia)
            lista_global.extend(libros_csv)
        return

    # Caso Base 2: Si es un archivo que no es items.csv
    if os.path.isfile(ruta_actual):
        return

    # 2. Paso Recursivo: Si es un directorio
    try:
        elementos = os.listdir(ruta_actual)
    except Exception:
        return
        
    for elemento in elementos:
        ruta_hijo = os.path.join(ruta_actual, elemento)
        consolidar_libros_recursivamente(ruta_hijo, lista_global)

    return lista_global








