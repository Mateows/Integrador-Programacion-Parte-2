import os
from fsc_estadisticas import estadisticas
from fsc_mostrar import mostrar_libros
from fsc_guardado import guardar_libro
from fsc_modificar import modificar_libro, eliminar_libro
from api_libros import buscar_y_guardar_libro, mostrar_libros_api

# Ruta base donde se guardarán los datos
BASE_PATH = os.path.join(os.path.dirname(__file__), "..", "data")
BASE_PATH = os.path.abspath(BASE_PATH)
os.makedirs(BASE_PATH, exist_ok=True)


def mostrar_menu(modo_api=False):
    """Muestra el menú según el modo actual."""
    if modo_api:
        print("\n=== MENÚ PRINCIPAL (Modo API) ===")
        print("1. Buscar y guardar libro (API)")
        print("2. Mostrar libro desde la API")
        print("3. Cambiar a modo local")
        print("4. Salir")
    else:
        print("\n=== MENÚ PRINCIPAL (Modo Local) ===")
        print("1. Agregar nuevo libro")
        print("2. Mostrar libros locales")
        print("3. Modificar libro")
        print("4. Eliminar libro")
        print("5. Estadísticas")
        print("6. Cambiar a modo API")
        print("7. Salir")


def main():
    print("📚 SISTEMA DE GESTIÓN DE LIBROS\n")

    modo_api = False  # Por defecto inicia en modo local

    while True:
        mostrar_menu(modo_api)
        opcion = input("Elegí una opción: ")

        # ----- MODO API -----
        if modo_api:
            match opcion:
                case "1":
                    buscar_y_guardar_libro(BASE_PATH)
                case "2":
                    mostrar_libros_api()
                case "3":
                    modo_api = False
                    print("\n🔄 Cambiado a modo LOCAL.")
                case "4":
                    print("¡Hasta luego!")
                    break
                case _:
                    print("Opción inválida.")

        # ----- MODO LOCAL -----
        else:
            match opcion:
                case "1":
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
                    modo_api = True
                    print("\n🌐 Cambiado a modo API (Google Books).")
                case "7":
                    print("¡Hasta luego!")
                    break
                case _:
                    print("Opción inválida.")


if __name__ == "__main__":
    main()
