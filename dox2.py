import requests
from bs4 import BeautifulSoup
import urllib.parse

def main():
    print("*******************************************")
    print("*  ¡Bienvenido al buscador de usuarios!  *")
    print("*******************************************\n")
    print("Este programa te permite buscar información sobre usuarios introduciendo su nombre de usuario o su nombre y apellido.")
    print("Las búsquedas se realizan en 'https://search.illicit.services/'.\n")

    while True:
        print("Selecciona una opción:")
        print("1. Buscar por nombre de usuario.")
        print("2. Buscar por nombre y apellido.")
        print("3. Salir.")
        option = input("\nIngresa el número de opción: ")

        if option == '1':
            try:
                num_users = int(input("¿Cuántos usuarios deseas buscar? "))
                for _ in range(num_users):
                    get_user_info_by_username()
            except ValueError:
                print("Error: Ingresa un número válido.")
        elif option == '2':
            try:
                num_names = int(input("¿Cuántos nombres deseas buscar? "))
                for _ in range(num_names):
                    get_user_info_by_name()
            except ValueError:
                print("Error: Ingresa un número válido.")
        elif option == '3':
            break
        else:
            print("Opción no válida. Por favor, intenta de nuevo.")
            print("Recuerda que debes ingresar el número de la opción que deseas seleccionar.")
        print()

def get_user_info_by_name():
    print("\n---------------------------------------")
    print("        Búsqueda por nombre y apellido")
    print("---------------------------------------\n")
    base_url = 'https://search.illicit.services/records?'
    first_name = input('Ingresa el nombre del usuario: ')
    last_name = input('Ingresa el apellido del usuario: ')

    # Codificar los nombres para que sean seguros para usar en una URL
    first_name = urllib.parse.quote_plus(first_name)
    last_name = urllib.parse.quote_plus(last_name)

    url = base_url + f'firstName={first_name}&lastName={last_name}'

    get_info(url)

def get_user_info_by_username():
    print("\n---------------------------------")
    print("        Búsqueda por nombre de usuario")
    print("---------------------------------\n")
    base_url = 'https://search.illicit.services/records?usernames='
    username = input('Ingresa un nombre de usuario: ')
    url = base_url + username

    get_info(url)

def get_info(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0;Win64) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Lanza una excepción si hay un error en la respuesta

        print(f"\nURL: {url}")  # Imprime la URL antes de mostrar la información

        # Crea una nueva instancia de BeautifulSoup con el texto de la respuesta
        soup = BeautifulSoup(response.text, 'html.parser')

        # Selecciona todos los divs con la clase 'record'
        records = soup.select('div.record')

        if len(records) == 0:
            print("\nNo se encontraron resultados.")
        else:
            print("\nInformación del usuario:\n")

            # Para cada div, selecciona todos los elementos 'dd' y obtén su texto
            for record in records:
                dds = record.select('dd')
                for dd in dds:
                    print(dd.get_text().strip())  # strip() para eliminar espacios en blanco al principio y al final

                # Encuentra el primer enlace en el div record
                a_tag = record.select_one('a')
                if a_tag is not None:
                    more_info_url = "https://search.illicit.services" + a_tag['href']
                    print(f"\nMás información en: {more_info_url}\n")
                else:
                    print("\nNo hay más información disponible.\n")
                    
                print("---------------------------------------")
    except requests.exceptions.RequestException as e:
        print(f"\nError de conexión: {e}")
    except Exception as e:
        print(f"\nError: {e}")

if __name__ == "__main__":
    main()
