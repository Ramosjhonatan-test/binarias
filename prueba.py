import time
import colorama
from colorama import Fore
import pyfiglet
import subprocess  # Importa subprocess para ejecutar binarias.py

# Inicializa colorama
colorama.init()

# Función para mostrar el logo o nombre
def mostrar_logo():
    logo = pyfiglet.figlet_format("JHONATAN")
    print(Fore.GREEN + logo)  # Puedes cambiar el color como desees

# Función para mostrar el menú
def mostrar_menu():
    print(Fore.YELLOW + "Elige una opción:")
    print("1. Realizar operaciones")
    print("2. Soporte")
    print("0. Salir")

# Función para manejar la opción seleccionada
def manejar_opcion(opcion):
    if opcion == "1":
        print(Fore.CYAN + "Realizando operaciones...")
        # Aquí se ejecuta el archivo binarias.py
        subprocess.run(['python', 'binarias.py'])  # Ejecuta binarias.py
    elif opcion == "2":
        print(Fore.CYAN + "Contacto de soporte: tucorreo@dominio.com")
        # Aquí podrías agregar más detalles del soporte, como tu número de teléfono
    elif opcion == "0":
        print(Fore.RED + "Saliendo...")
        time.sleep(1)
        exit()
    else:
        print(Fore.RED + "Opción no válida. Intenta nuevamente.")

# Función principal
def main():
    mostrar_logo()
    while True:
        mostrar_menu()
        opcion = input(Fore.WHITE + "Selecciona una opción: ")
        manejar_opcion(opcion)

if __name__ == "__main__":
    main()
