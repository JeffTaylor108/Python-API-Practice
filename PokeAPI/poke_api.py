# import requests using 'pip install requests'
import requests

base_url = "https://pokeapi.co/api/v2/"

def get_pokemon_info(name):
    url = f"{base_url}/pokemon/{name}"
    response = requests.get(url) # returns response object from url (should be <Response [200]>)
    print(response)

    if response.status_code == 200:
        pokemon_data = response.json() # converts response obj to a python dictionary of key-value pairs
        return pokemon_data
    else:
        print(f"Failed to retrieve data {response.status_code}")



pokemon_name = "pikachu"
pokemon_info = get_pokemon_info(pokemon_name)

if pokemon_info:
    print(f"Name: {pokemon_info['name']}") # returns with the name of the pokemon
    print(f"Id: {pokemon_info['id']}")
    print(f"Height: {pokemon_info['height']}")
    print(f"Weight: {pokemon_info['weight']}")


