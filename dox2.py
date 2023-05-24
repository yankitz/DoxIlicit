#Este código está estructurado en tres partes principales: la función main, y dos funciones para 
#obtener información del usuario get_user_info_by_name y get_user_info_by_username,
# y una función para procesar las peticiones get_info

from time import sleep
import random
import requests
from bs4 import BeautifulSoup
import urllib.parse

def main():
    print("¡Bienvenido al buscador de información de usuarios!")
    print("Este programa te permite buscar información sobre usuarios introduciendo su nombre de usuario o su nombre y apellido.")
    print("Las búsquedas se realizan en 'https://search.illicit.services/'.")
    print()

    while True:
        print("Selecciona una opción:")
        print("1. Buscar por nombre de usuario.")
        print("2. Buscar por nombre y apellido.")
        print("3. Salir.")
        option = input()

        if option == '1':
            num_users = int(input("¿Cuántos usuarios deseas buscar? "))
            for _ in range(num_users):
                get_user_info_by_username()
        elif option == '2':
            num_names = int(input("¿Cuántos nombres deseas buscar? "))
            for _ in range(num_names):
                get_user_info_by_name()
        elif option == '3':
            break
        else:
            print("Opción no válida. Por favor, intenta de nuevo.")
        print()

def get_user_info_by_name():
    base_url = 'https://search.illicit.services/records?'
    first_name = input('Ingresa el nombre del usuario: ')
    last_name = input('Ingresa el apellido del usuario: ')

    # Codificar los nombres para que sean seguros para usar en una URL
    first_name = urllib.parse.quote_plus(first_name)
    last_name = urllib.parse.quote_plus(last_name)

    url = base_url + f'firstName={first_name}&lastName={last_name}'

    get_info(url)

def get_user_info_by_username():
    base_url = 'https://search.illicit.services/records?usernames='
    username = input('Ingresa un nombre de usuario: ')
    url = base_url + username

    get_info(url)

#La función 'get_info' toma una URL, hace una solicitud HTTP GET a esa URL, y procesa la respuesta.
def get_info(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0;Win64) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print(f"URL: {url}")  # Imprime la URL antes de mostrar la información

        # Crea una nueva instancia de BeautifulSoup con el texto de la respuesta
        soup = BeautifulSoup(response.text, 'html.parser')

        # Selecciona todos los divs con la clase 'record'
        records = soup.select('div.record')

        # Para cada div, selecciona todos los elementos 'dd' y obtén su texto
        for record in records:
            dds = record.select('dd')
            for dd in dds:
                print(dd.get_text().strip())  # strip() para eliminar espacios en blanco al principio y al final

            # Encuentra el primer enlace en el div record
            a_tag = record.select_one('a')
            if a_tag is not None:
                more_info_url = "https://search.illicit.services" + a_tag['href']
                print(f"\nMás información en: {more_info_url}\n")  # Imprime el enlace

            print()  # Imprime una línea en blanco después de cada div 'record'
    else:
        print(f"Error: {response.status_code}")
        return None


if __name__ == "__main__":
    main()
