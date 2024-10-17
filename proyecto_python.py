import json
import requests


# Función principal para el menú
def menu():
    listalibros = []
    while True:
        print("\n--- Menú de Libros ---")
        print("1. Agregar libro")
        print("2. Listar libros")
        print("3. Guardar libros en JSON")
        print("4. Buscar libro en API")
        print("5. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            titulo = input("Ingrese el título del libro: ")
            autor = input("Ingrese el autor del libro: ")
            agregar_libro(listalibros, titulo, autor)
        elif opcion == "2":
            listar_libros(listalibros)
        elif opcion == "3":
            archivo = input("Ingrese el nombre del archivo (con .json): ")
            guardar_libros(listalibros, archivo)
        elif opcion == "4":
            titulo = input("Ingrese el título del libro a buscar: ")
            buscar_libro_api(titulo)
        elif opcion == "5":
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida. Intente de nuevo.")


# Clase Libro
class Libro:
    def __init__(self, titulo, autor):
        self.titulo = titulo
        self.autor = autor


# Función agregar libro
def agregar_libro(libros, titulo, autor):
    libros.append(Libro(titulo, autor))
    print(f'Libro "{titulo}" agregado correctamente.')


# Función para listar libros ordenados por título
def listar_libros(libros):
    if libros:
        libros_ordenados = sorted(libros, key=lambda lib: lib.titulo.lower())  #Ordeno los libros por título utilizando lambda, coge cada libro de la lista y lo devuelve en minúsuclas para poder ordenarlo después.

        for libro in libros_ordenados:
            print(f'Título: {libro.titulo}, Autor: {libro.autor}')
    else:
        print("No hay libros en la lista.")


# Función para guardar libros en JSON
def guardar_libros(libros, archivo):
    try:
        with open(archivo, 'w') as file:
            json.dump([libro.__dict__ for libro in libros], file) #esta expresión convierte cada objeto libro en un diccionario
        print(f"Libros guardados en '{archivo}' correctamente.")
    except Exception as e:
        print("Error al guardar libros:", e)

# Función para buscar un libro en una API
def buscar_libro_api(titulo):
    response = requests.get(f"https://www.googleapis.com/books/v1/volumes?q={titulo}") #API google books

    if response.status_code == 200:
        data = response.json()  # Convierte el JSON en un diccionario
        libros = data.get("items", [])  # Obtiene la lista de libros

        if libros: #compruebo si en la lista hay libros
            for libro in libros: #recorro la lista
                info = libro.get("volumeInfo", {})
                titulo_libro = info.get("title", "Sin título")
                autores = info.get("authors", ["Autor desconocido"])
                print(f"Título: {titulo_libro}")
                print(f"Autor(es): {', '.join(autores)}")  #en el caso de que haya mas de un autor, los concatena
                print()  #línea en blanco entre los resultados
        else:
            print(f"No se encontraron libros con el título '{titulo}'.")

    else:
        print(f"Error: {response.status_code}; no se pudo encontrar información para el libro '{titulo}'.")


if __name__ == "__main__": # Buena práctica. Controla cuando se ejecuta el código principal y permite que el archivo se use como un módulo sin ejecutar el menú accidentalmente.
    menu()

