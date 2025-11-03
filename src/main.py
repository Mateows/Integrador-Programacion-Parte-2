import os
from almacenamiento import guardar_libro, mostrar_libros, modificar_libro, eliminar_libro, estadisticas
from api_libros import buscar_libro_api, mostrar_libros_api

# Ruta base donde se guardarán los datos

BASE_PATH = os.path.join(os.path.dirname(__file__), "..", "data")
BASE_PATH = os.path.abspath(BASE_PATH)
os.makedirs(BASE_PATH, exist_ok=True)
print("Guardando datos en:", BASE_PATH)



# Aseguramos que exista la carpeta data
os.makedirs(BASE_PATH, exist_ok=True)

def mostrar_menu(modo_api=False):

    print("\n=== MENÚ PRINCIPAL ===")

    if modo_api:
        print("1. Buscar y guardar libro (API)")
        print("7. Mostrar libros desde API (sin guardar)")
    else:
        print("1. Agregar nuevo ítem")
    print("2. Mostrar ítems")
    print("3. Modificar ítem")
    print("4. Eliminar ítem")
    print("5. Estadísticas")
    print("6. Salir")

def main():
    print("SISTEMA DE GESTIÓN DE LIBROS\n")

# pregunta si quiere trabajar con la api o solo con el csv
    while True:
        print("Seleccioná modo de trabajo:")
        print("1. Local (usar datos guardados en CSV)")
        print("2. API (consultar Google Books)")
        modo = input("Elegí una opción (1 o 2): ")

        if modo == "1":
            modo_api = False
            print("\nModo seleccionado: LOCAL (CSV manual)")
            break
        elif modo == "2":
            modo_api = True
            print("\nModo seleccionado: API de Google Books")
            break
        else:
            print("Opción inválida. Intentá de nuevo.\n")


# MENU PRINCIPAL
    while True:
        mostrar_menu(modo_api)
        opcion = input("Elegí una opción: ")
        match opcion:
            case "1":
                if modo_api:
                    buscar_libro_api(BASE_PATH)
                else:
                    genero = input("Género del libro: ")
                    autor = input("Autor: ")
                    anio = input("Año de publicación: ")
                    titulo = input("Título del libro: ")
                    paginas = input("Cantidad de páginas: ")
                    guardar_libro(BASE_PATH, genero, autor, anio, titulo, paginas)

            case "2":
                mostrar_libros(BASE_PATH)
            case "3":
                modificar_libro(BASE_PATH)
            case "4":
                 eliminar_libro(BASE_PATH)
            case "5":
                 estadisticas(BASE_PATH)
            case "6":
                print("¡Hasta luego!")
                break
            case "7":
                if modo_api:
                    mostrar_libros_api()
                else:
                    print("Esta opción solo está disponible en modo API.")

            case _:
                print("Opción no válida. Probá de nuevo.")

if __name__ == "__main__":
    main()

