# Integrador-Programacion-Parte-2
Entrega del Integrador Programación Para el Profesor Hualpa
# 📚 Parcial 2 - Programación 1: Gestión Jerárquica de Biblioteca

**Equipo de Desarrollo:**
* **Amanda Pagano**
* **Lucas Avila**
* **Mateo Olmedo**


Enlace del Video Explicativo: https://youtu.be/i3qtqYqo--0?si=has4AEoJxIpZpDZ-

Proyecto desarrollado en Python 3.10+ para la Universidad Tecnológica Nacional (UTN) que implementa un sistema de gestión de Libros aplicando una estructura de persistencia jerárquica, recursividad para la lectura de datos, y consumo de API.

## 🎯 Objetivo General

* Desarrollar una aplicación que gestione una biblioteca local, cumpliendo con los requisitos de la Fase 2 y 3 del parcial, aplicando:
* Diseño de estructuras de datos (Diccionarios).
* Manipulación avanzada de archivos CSV y gestión de I/O (`with`, `try/except`).
* Recursividad para la lectura y consolidación del sistema de archivos[cite: 44, 49].
* Funciones de la librería estándar `os` para gestionar la estructura de carpetas de forma dinámica.


## 📂 Diseño y Persistencia Jerárquica (Fase 1)

El proyecto utiliza el dominio de una Biblioteca y define una jerarquía de tres niveles que se mapea directamente a la estructura de carpetas[cite: 27]:

| Nivel | Rol en la Jerarquía | Lógica de Almacenamiento / Carpeta |
| :--- | :--- | :--- |
| **Nivel 1** | Género Principal | `/data/Género/` |
| **Nivel 2** | Autor | `/data/Género/Autor/` |
| **Nivel 3** | Año de Publicación | `/data/Género/Autor/Año/` |
| **Ítem Final** | Libro | `items.csv` (Almacena ítems individuales) |

### Patrón de Datos (Diccionarios)

Cada libro es representado internamente como un **diccionario** que consolida sus atributos y su ubicación jerárquica:

```python
{
    "genero": "Ciencia Ficcion",
    "autor": "Isaac Asimov",
    "año": 1951,
    "titulo": "Fundacion",
    "paginas": 255,
    "id": "Ciencia Ficcion/Isaac Asimov/Fundacion", 
    "ruta_csv": ".../data/Ciencia Ficcion/Isaac Asimov/1951/items.csv" 
}


🛠️ Implementación y Funcionalidades (Fase 2 y 3)
1. Lectura Recursiva Centralizada
La función recursiva cumple con los requisitos de recibir la ruta actual, definir un caso base (encontrar el CSV) y un paso recursivo (llamar a subdirectorios). Su objetivo es consolidar todos los datos en una única lista de diccionarios.


3. Funcionalidades Adicionales (Fase 3, Punto 5)
Ordenamiento Global: Permite ordenar la lista completa de libros (obtenida recursivamente) por al menos dos atributos diferentes (ej. Título y Páginas).

Estadísticas Básicas: Calcula la cantidad total de libros, el promedio de páginas (atributo numérico clave) y el recuento de ítems por Género (categoría de primer nivel).

API Integration: Permite consultar la Google Books API para buscar y guardar nuevos libros en la estructura jerárquica local.

🚀 Instrucciones de Uso:

Requisitos:

Python 3.10+

Librería requests (Necesaria para el Modo API), ejecuten la Terminal o cdm como Administrador:

            pip install requests


Ejecución:

1-Clonar el repositorio.

2-Ejecutar el programa principal (asumiendo que main.py está en src o fuente):

            python fuente/main.py

3-Al iniciar, seleccionar el modo de trabajo (1. Local o 2. API).

4-La carpeta de persistencia data se creará automáticamente para almacenar la estructura jerárquica de archivos.

