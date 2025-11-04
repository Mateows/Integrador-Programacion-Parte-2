# --- FUNCIONES DE PERSISTENCIA (CSV) Y MANEJO DE EXCEPCIONES ---
import os
import csv
from fsc_jerarquia import ensure_path_for_book
from typing import List, Dict, Tuple, Any

CSV_HEADERS = ["Título", "Páginas"]

def guardar_datos_csv(ruta_csv: str, libros_en_memoria: List[Dict]):
    """Sobrescribe un archivo CSV específico (modo 'w') con la lista de diccionarios actualizada."""
    if not libros_en_memoria:
        try:
            if os.path.exists(ruta_csv):
                os.remove(ruta_csv)
            return
        except OSError as e:
            print(f"❌ Error al intentar eliminar el archivo vacío {ruta_csv}: {e}")
            return
    
    try:
        with open(ruta_csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=CSV_HEADERS)
            writer.writeheader()
            for libro in libros_en_memoria:
                writer.writerow({
                'Título': libro.get('titulo', ''),
                'Páginas': libro.get('paginas', 0)
               })

        print(f"✅ Archivo actualizado: {ruta_csv} ({len(libros_en_memoria)} libros)")
    except OSError as e:
        print(f"Error al escribir en el archivo {ruta_csv}: {e}")

# --- FUNCION DE VALIDACIÓN ESTRICTA (Fase 3, Punto 1) ---

def validar_entrada_libro(data: Dict[str, str]) -> Tuple[bool, str | Dict[str, Any]]:
    """Valida los datos del libro antes de guardarlo."""
    
    required_fields = ['genero', 'autor', 'anio', 'titulo', 'paginas']
    # Validar que no haya vacíos
    if not all(str(data.get(field, '')).strip() for field in required_fields):
        return False, "Todos los campos (Género, Autor, Año, Título, Páginas) son obligatorios."

    # Validar que año y páginas sean numéricos y positivos
    try:
        anio_int = int(data['anio'])
        paginas_int = int(data['paginas'])
    except (ValueError, TypeError):
        return False, "Año y Páginas deben ser números válidos."

    if anio_int <= 0 or paginas_int <= 0:
        return False, "El Año de publicación y las Páginas deben ser positivos."

    # Retornar diccionario validado
    libro_data = {
        "genero": str(data['genero']).strip(),
        "autor": str(data['autor']).strip(),
        "anio": anio_int,
        "titulo": str(data['titulo']).strip(),
        "paginas": paginas_int,
    }

    return True, libro_data
          

#---------Guardar libro-----------------
def guardar_libro(base_path: str, data_input: Dict[str, str]):
    """
    Alta de Nuevo Ítem (Creación Jerárquica) - Única que puede crear nuevas carpetas.
    """
    es_valido, resultado = validar_entrada_libro(data_input)
    
    if not es_valido:
        print(f"\nError de validación: {resultado}")
        return

    libro_data: Dict[str, Any] = resultado
    
    niveles_jerarquia = {
        'genero': libro_data['genero'], 
        'autor': libro_data['autor'], 
        'anio': libro_data['anio']
    }
    
    try:
        ruta_csv = ensure_path_for_book(base_path, niveles_jerarquia)
        existe = os.path.exists(ruta_csv)

        with open(ruta_csv, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if not existe:
                writer.writerow(CSV_HEADERS) 
            
            writer.writerow([libro_data['titulo'], libro_data['paginas']])

        print(f"\nLibro '{libro_data['titulo']}' guardado jerárquicamente en {ruta_csv}")
        
    except OSError as e:
        print(f"Error del sistema de archivos al guardar el libro: {e}")


   
