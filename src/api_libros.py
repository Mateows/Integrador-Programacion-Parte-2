import requests
import json
import unicodedata
from typing import Dict, Any, Optional
from fsc_guardado import guardar_libro, validar_entrada_libro
from difflib import SequenceMatcher


API_URL = "https://www.googleapis.com/books/v1/volumes"



# -------------------------------
# UTILIDADES
# -------------------------------

def son_similares(a: str, b: str, umbral: float = 0.4) -> bool:
    """
    Determina si dos cadenas son similares según un umbral (0 a 1).
    Permite búsquedas tolerantes a errores ortográficos.
    """
    a_norm, b_norm = a.lower().strip(), b.lower().strip()
    similitud = SequenceMatcher(None, a_norm, b_norm).ratio()
    return similitud >= umbral


def limpiar_dato(valor):
    """Evita errores con campos faltantes o vacíos."""
    return valor if valor not in [None, "", " "] else "Desconocido"


# -------------------------------
# API GOOGLE BOOKS
# -------------------------------

def obtener_libros_api(nombre_libro: str):
    """
    Consulta la API de Google Books y devuelve una lista de coincidencias válidas.
    Ignora los libros que no tienen páginas o año.
    """
    try:
        response = requests.get(API_URL, params={"q": nombre_libro, "maxResults": 15})
        data = response.json()

        if "items" not in data:
            print("❌ No se encontraron resultados en la API.")
            return []

        resultados_validos = []

        for item in data["items"]:
            info = item.get("volumeInfo", {})
            titulo = limpiar_dato(info.get("title"))
            autor = ", ".join(info.get("authors", ["Desconocido"]))
            genero = limpiar_dato(info.get("categories", ["General"])[0])
            paginas = info.get("pageCount", 0)
            anio = info.get("publishedDate", "0")[:4]

            # Validar campos numéricos
            try:
                paginas = int(paginas)
                anio = int(anio)
                if paginas <= 0 or anio <= 0:
                    continue  # Saltar si no tiene datos válidos
            except (ValueError, TypeError):
                continue

            # Filtrar por similitud aproximada en título
            if son_similares(nombre_libro, titulo) or nombre_libro.lower() in titulo.lower():
                resultados_validos.append({
                    "genero": genero,
                    "autor": autor,
                    "anio": anio,
                    "titulo": titulo,
                    "paginas": paginas
                })

        # Si no hubo coincidencias similares, mostrar las primeras válidas
        if not resultados_validos:
            print("⚠️ No se encontraron coincidencias exactas, mostrando resultados válidos de respaldo.")
            for item in data["items"]:
                info = item.get("volumeInfo", {})
                if "pageCount" in info and "publishedDate" in info:
                    titulo = info.get("title", "Desconocido")
                    autor = ", ".join(info.get("authors", ["Desconocido"]))
                    genero = info.get("categories", ["General"])[0]
                    paginas = int(info.get("pageCount", 0))
                    anio = int(info.get("publishedDate", "0")[:4]) if info.get("publishedDate") else 0
                    if paginas > 0 and anio > 0:
                        resultados_validos.append({
                            "genero": genero,
                            "autor": autor,
                            "anio": anio,
                            "titulo": titulo,
                            "paginas": paginas
                        })

        return resultados_validos

    except requests.RequestException as e:
        print(f"⚠️ Error al conectarse con la API: {e}")
        return []


# -------------------------------
# FUNCIONES PRINCIPALES
# -------------------------------
def buscar_y_guardar_libro(base_path: str):
    """
    Busca un libro en la API (tolerando errores de escritura)
    y permite guardar el que el usuario elija.
    """
    nombre_libro = input("Ingresa el libro de la API que quieres guardar: ").strip()

    resultados = obtener_libros_api(nombre_libro)

    if not resultados:
        print("No se encontró ningún libro válido con esos datos.")
        return

    print(f"\n📚 Se encontraron {len(resultados)} libros similares:\n")
    for i, libro in enumerate(resultados, start=1):
        print(f"[{i}] {libro['titulo']} - {libro['autor']} ({libro['anio']}) [{libro['paginas']} páginas]")

    try:
        indice = int(input("\nSeleccioná el número del libro que querés guardar (0 para cancelar): "))
        if indice == 0:
            print("Operación cancelada.")
            return
        if indice < 1 or indice > len(resultados):
            print("Número inválido.")
            return
    except ValueError:
        print("Debes ingresar un número válido.")
        return

    seleccionado = resultados[indice - 1]

    es_valido, resultado = validar_entrada_libro(seleccionado)
    if not es_valido:
        print(f"❌ Error de validación: {resultado}")
        return

    guardar_libro(base_path, resultado)
    print(f"\n✅ Libro '{resultado['titulo']}' guardado correctamente desde la API.")



def normalizar_texto(texto: str) -> str:
    """Elimina acentos y pasa todo a minúsculas."""
    texto = texto.lower()
    texto = unicodedata.normalize('NFKD', texto)
    return ''.join(c for c in texto if not unicodedata.combining(c))



def mostrar_libros_api(base_path: str = None):
    """
    Busca libros en la API por género, tema o palabra clave,
    mostrando hasta 25 resultados reales usando paginación.
    """
    consulta = input("\n🔎 Ingresa un género, autor o palabra clave para buscar libros: ").strip()
    if not consulta:
        print("Búsqueda cancelada.")
        return

    try:
        max_resultados = 25
        resultados = []
        start_index = 0

        print("\nBuscando en la API...")

        while len(resultados) < max_resultados:
            restante = max_resultados - len(resultados)
            params = {
                "q": consulta,
                "maxResults": min(40, restante),
                "startIndex": start_index,
                "printType": "books",
                "langRestrict": "es",
                #"key":"API KEY ACÁ"
            }

            response = requests.get(API_URL, params=params, timeout=5)
            response.raise_for_status()
            data = response.json()

            if start_index == 0:
                print(f"Total de resultados disponibles: {data.get('totalItems', 0)}")

            items = data.get("items", [])
            if not items:
                break

            resultados.extend(items)
            start_index += len(items)

            # Si la API devolvió menos de lo solicitado, no hay más páginas
            if len(items) < params["maxResults"]:
                break

        if not resultados:
            print("❌ No se encontraron libros en la API para esa búsqueda.")
            return

        print(f"\n📚 Resultados encontrados para: '{consulta}'\n")
        for i, item in enumerate(resultados[:max_resultados], start=1):
            info = item.get("volumeInfo", {})
            titulo = info.get("title", "Título desconocido")
            autores = ", ".join(info.get("authors", ["Autor desconocido"]))
            categorias = ", ".join(info.get("categories", ["Género desconocido"]))
            anio = info.get("publishedDate", "¿?").split("-")[0]
            paginas = info.get("pageCount", "N/D")

            print(f"[{i}] {titulo}")
            print(f"     Autor: {autores}")
            print(f"     Género: {categorias}")
            print(f"     Año: {anio} | Páginas: {paginas}")
            print("---")

    except requests.exceptions.RequestException as e:
        print(f"⚠️ Error al conectar con la API: {e}")