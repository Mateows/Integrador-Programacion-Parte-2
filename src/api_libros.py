import requests
import json
from typing import Dict, Any, Optional
from almacenamiento import guardar_libro, validar_entrada_libro

# URL base para la API de Google Books
GOOGLE_BOOKS_API_URL = "https://www.googleapis.com/books/v1/volumes"

def obtener_datos_libro(query: str) -> Optional[Dict[str, Any]]:
    """Busca un libro por título o autor en la Google Books API."""
    try:
        params = {"q": query, "maxResults": 1} # Traemos solo el primer resultado
        response = requests.get(GOOGLE_BOOKS_API_URL, params=params, timeout=5)
        response.raise_for_status() 

        datos = response.json()
        
        if "items" not in datos or not datos["items"]:
            return None

        info = datos["items"][0]["volumeInfo"]
        
        # Mapeamos los datos de la API a nuestro patrón de diccionario
        libro_data = {
            # NIVELES DE JERARQUÍA (Asumidos/Derivados)
            'genero': info.get('categories', ['Desconocido'])[0],
            'autor': info.get('authors', ['Desconocido'])[0],
            'anio': info.get('publishedDate', '0000').split('-')[0], # Tomamos solo el año
            # ATRIBUTOS DEL ÍTEM
            'titulo': info.get('title', 'Título Desconocido'),
            'paginas': str(info.get('pageCount', 0)), # La validación lo convertirá
        }
        return libro_data

    except requests.exceptions.RequestException as e:
        print(f"\n❌ Error de conexión a la API: {e}")
        return None
    except Exception as e:
        print(f"\n❌ Error al procesar datos del libro: {e}")
        return None


def mostrar_libros_api():
    """Permite al usuario buscar un libro y mostrarlo sin guardar."""
    
    query = input("\nIngresa el título o autor del libro a buscar en la API: ")
    if not query.strip():
        print("Búsqueda cancelada.")
        return

    datos = obtener_datos_libro(query)
    
    if datos:
        print("\n--- 📚 LIBRO ENCONTRADO (API) 📚 ---")
        print(f"Título: {datos['titulo']}")
        print(f"Autor: {datos['autor']}")
        print(f"Género: {datos['genero']}")
        print(f"Año: {datos['anio']} | Páginas: {datos['paginas']}")
        print("---------------------------------------")
    else:
        print("No se encontró el libro.")


def buscar_y_guardar_libro(base_path: str):
    """Busca un libro en la API y lo guarda en el sistema de archivos local."""
    
    query = input("\nIngresa el libro de la API que quieres guardar: ")
    if not query.strip():
        print("Operación cancelada.")
        return

    libro_api_data = obtener_datos_libro(query)
    
    if libro_api_data:
        # Usamos la misma función de validación de almacenamiento
        es_valido, resultado = validar_entrada_libro(libro_api_data)
        
        if es_valido:
            # Llama a la función de persistencia jerárquica
            guardar_libro(base_path, libro_api_data)
        else:
            print(f"❌ Error al validar datos de la API (ej: faltan páginas o año): {resultado}")
    else:
        print("No se pudo guardar. El libro no fue encontrado o hubo un error en la API.")