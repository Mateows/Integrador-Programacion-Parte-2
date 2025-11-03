import requests
from almacenamiento import guardar_libro

def buscar_libro_api(base_path):
    print("\n📚 BUSCAR LIBRO EN GOOGLE BOOKS\n")

    consulta = input("🔍 Ingresá el título o autor: ").strip()
    if not consulta:
        print("⚠️ Debes ingresar un texto para buscar.")
        return

    # Llamada a la API de Google Books
    url = f"https://www.googleapis.com/books/v1/volumes?q={consulta}"
    print(f"🌐 URL generada: {url}")

    try:
        response = requests.get(url)
        print(f"🔢 Código de respuesta: {response.status_code}")
    except Exception as e:
        print(f"❌ Error al conectar con la API: {e}")
        return

    if response.status_code != 200:
        print("❌ Error al conectar con la API. Verificá tu conexión a internet.")
        return

    data = response.json()
    items = data.get("items", [])
    print(f"📦 Cantidad de resultados encontrados: {len(items)}")

    if not items:
        print("⚠️ No se encontraron resultados.")
        return

    # Mostrar los primeros 5 resultados
    print("\n=== Resultados encontrados ===")
    for i, item in enumerate(items[:5], start=1):
        info = item["volumeInfo"]
        titulo = info.get("title", "Sin título")
        autores = ", ".join(info.get("authors", ["Desconocido"]))
        anio = info.get("publishedDate", "Desconocido")[:4]
        print(f"{i}. {titulo} — {autores} ({anio})")

    # Elegir un libro
    try:
        eleccion = int(input("\nElegí un número para guardar (0 para cancelar): "))
    except ValueError:
        print("❌ Opción inválida.")
        return

    if eleccion == 0:
        print("Operación cancelada.")
        return
    if eleccion < 1 or eleccion > len(items[:5]):
        print("❌ Número fuera de rango.")
        return

    # Guardar el libro elegido
    elegido = items[eleccion - 1]["volumeInfo"]
    titulo = elegido.get("title", "Sin título")
    autores = ", ".join(elegido.get("authors", ["Desconocido"]))
    anio = elegido.get("publishedDate", "Desconocido")[:4]
    paginas = elegido.get("pageCount", "0")
    genero = elegido.get("categories", ["General"])[0]

    print(f"\n✅ Guardando '{titulo}' en el sistema local...")

    guardar_libro(base_path, genero, autores, anio, titulo, paginas)
    print("💾 Libro guardado correctamente.")



# Muestra depende el genero o tema libros ya que la api tiene millones y no permite mostrar todos
def mostrar_libros_api():
    print("\n LISTADO DE LIBROS DESDE GOOGLE BOOKS\n")

    # usamos una consulta genérica si el usuario no ingresa nada
    consulta = input("🔍 Ingresá un tema o presioná ENTER para mostrar libros populares: ").strip()
    if not consulta:
        consulta = "books"  # palabra genérica para traer resultados variados

    # pedimos los primeros 10 resultados
    url = f"https://www.googleapis.com/books/v1/volumes?q={consulta}&maxResults=10"
    response = requests.get(url)

    if response.status_code != 200:
        print("❌ Error al conectar con la API.")
        return

    data = response.json()
    items = data.get("items", [])

    if not items:
        print("No se encontraron libros disponibles.")
        return

    print(f"Mostrando {len(items)} resultados:\n")
    for i, item in enumerate(items, start=1):
        info = item.get("volumeInfo", {})
        titulo = info.get("title", "Sin título")
        autores = ", ".join(info.get("authors", ["Autor desconocido"]))
        anio = info.get("publishedDate", "Sin año")
        paginas = info.get("pageCount", "Desconocidas")
        print(f"{i}. {titulo}\n   Autor(es): {autores}\n   Año: {anio}\n   Páginas: {paginas}\n")
