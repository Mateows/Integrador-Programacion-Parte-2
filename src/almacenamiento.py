import os
import csv

# Crea la estructura de carpetas:data/genero/autor/anio/ 
# (basicamente crea las ramas donde van a estar los csv)
# y devuelve la ruta completa donde guardar el CSV.

def ensure_path_for_book(base_path, genero, autor, anio):
    
    ruta = os.path.join(base_path, genero, autor, str(anio))
    os.makedirs(ruta, exist_ok=True)
    return os.path.join(ruta, "items.csv")

#Guarda un libro en el archivo correspondiente a su género/autor/año.
# Si el archivo no existe, lo crea con encabezados.

def guardar_libro(base_path, genero, autor, anio, titulo, paginas):
    
    ruta_csv = ensure_path_for_book(base_path, genero, autor, anio)
    existe = os.path.exists(ruta_csv)

    with open(ruta_csv, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not existe:
            writer.writerow(["Título", "Páginas"])
        writer.writerow([titulo, paginas])

    print(f"Libro '{titulo}' guardado en {ruta_csv}")

# Funcion recursiva recorre recursivamente la carpeta base y muestra todos los libros guardados.
def mostrar_libros(base_path):
   
    print("\n📚 LISTADO DE LIBROS\n")

    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file == "items.csv":
                ruta_csv = os.path.join(root, file)
                try:
                    # Tomar el género, autor y año desde la ruta
                    partes = ruta_csv.split(os.sep)
                    genero, autor, anio = partes[-4:-1]

                    print(f"\n=== {genero.upper()} / {autor} / {anio} ===")

                    with open(ruta_csv, "r", encoding="utf-8") as f:
                        reader = csv.reader(f)
                        next(reader, None)  # saltar encabezado
                        for fila in reader:
                            if len(fila) >= 2:
                                titulo, paginas = fila
                                print(f"📖 {titulo} — {paginas} páginas")
                except Exception as e:
                    print(f"Error leyendo {ruta_csv}: {e}")  

# Permite modificar un libro dentro del CSV correspondiente. Busca por género, autor y año.
def modificar_libro(base_path):

    print("\n✏️ MODIFICAR LIBRO\n")

    # Pedimos datos para ubicar el archivo correcto
    genero = input("Género: ")
    autor = input("Autor: ")
    anio = input("Año: ")

    ruta_csv = os.path.join(base_path, genero, autor, str(anio), "items.csv")

    if not os.path.exists(ruta_csv):
        print("No se encontró el archivo. Verificá los datos ingresados.")
        return

    # Leemos todos los libros
    with open(ruta_csv, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        libros = list(reader)

    if len(libros) <= 1:
        print("No hay libros para modificar.")
        return

    # Mostramos los libros con un índice
    print("\nLibros encontrados:")
    for i, fila in enumerate(libros[1:], start=1):
        print(f"{i}. {fila[0]} — {fila[1]} páginas")

    try:
        indice = int(input("\nElegí el número del libro a modificar: "))
        if indice < 1 or indice >= len(libros):
            print("Número inválido.")
            return
    except ValueError:
        print("Debes ingresar un número.")
        return

    # Pedimos los nuevos datos
    nuevo_titulo = input("Nuevo título (dejar vacío para no cambiar): ").strip()
    nuevas_paginas = input("Nuevas páginas (dejar vacío para no cambiar): ").strip()

    if nuevo_titulo:
        libros[indice][0] = nuevo_titulo
    if nuevas_paginas:
        libros[indice][1] = nuevas_paginas

    # Reescribimos el archivo con los cambios
    with open(ruta_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(libros)

    print(f"Libro modificado correctamente en {ruta_csv}")

# Permite eliminar un libro del CSV correspondiente a su género, autor y año.
def eliminar_libro(base_path):
    
    print("\n🗑️ ELIMINAR LIBRO\n")

    genero = input("Género: ")
    autor = input("Autor: ")
    anio = input("Año: ")

    ruta_csv = os.path.join(base_path, genero, autor, str(anio), "items.csv")

    if not os.path.exists(ruta_csv):
        print("No se encontró el archivo. Verificá los datos ingresados.")
        return

    # Leer todos los libros
    with open(ruta_csv, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        libros = list(reader)

    if len(libros) <= 1:
        print("No hay libros para eliminar.")
        return

    # Mostrar los libros con índice
    print("\nLibros encontrados:")
    for i, fila in enumerate(libros[1:], start=1):
        print(f"{i}. {fila[0]} — {fila[1]} páginas")

    try:
        indice = int(input("\nElegí el número del libro a eliminar: "))
        if indice < 1 or indice >= len(libros):
            print("Número inválido.")
            return
    except ValueError:
        print("Debes ingresar un número.")
        return

    # Confirmación
    confirm = input(f"¿Seguro que querés eliminar '{libros[indice][0]}'? (s/n): ").lower()
    if confirm != "s":
        print("Operación cancelada.")
        return

    # Eliminar la fila seleccionada
    eliminado = libros.pop(indice)

    # Reescribir el archivo sin esa fila
    with open(ruta_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(libros)

    print(f"Libro '{eliminado[0]}' eliminado correctamente.")

#Calcula estadísticas generales sobre los libros guardados:
#   - total de libros
#   - promedio de páginas
#   - género con más libros
#   - autor con más libros
def estadisticas(base_path):

    print("\n📊 ESTADÍSTICAS DE LIBROS\n")

    total_libros = 0
    total_paginas = 0
    libros_por_genero = {}
    libros_por_autor = {}

    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file == "items.csv":
                ruta_csv = os.path.join(root, file)
                partes = ruta_csv.split(os.sep)
                genero, autor, anio = partes[-4:-1]

                with open(ruta_csv, "r", encoding="utf-8") as f:
                    reader = csv.reader(f)
                    next(reader, None)  # saltar encabezado
                    for fila in reader:
                        if len(fila) >= 2:
                            titulo, paginas = fila
                            try:
                                paginas = int(paginas)
                            except ValueError:
                                continue

                            total_libros += 1
                            total_paginas += paginas

                            # Contar por género
                            libros_por_genero[genero] = libros_por_genero.get(genero, 0) + 1

                            # Contar por autor
                            libros_por_autor[autor] = libros_por_autor.get(autor, 0) + 1

    if total_libros == 0:
        print("No hay libros registrados.")
        return

    promedio_paginas = total_paginas / total_libros
    genero_mas = max(libros_por_genero, key=libros_por_genero.get)
    autor_mas = max(libros_por_autor, key=libros_por_autor.get)

    print(f"Total de libros: {total_libros}")
    print(f"Promedio de páginas: {promedio_paginas:.2f}")
    print(f"Género con más libros: {genero_mas} ({libros_por_genero[genero_mas]})")
    print(f"Autor con más libros: {autor_mas} ({libros_por_autor[autor_mas]})")



