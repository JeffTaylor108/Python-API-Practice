from flask import Flask, render_template, request
import requests

app = Flask(__name__)
base_url = "https://pokeapi.co/api/v2/"

@app.route('/', methods=['GET', 'POST'])
def home():
    result = None

    if request.method == 'POST':
        pokemon1 = request.form['name1'].lower()
        pokemon2 = request.form['name2'].lower()

        url1 = f"{base_url}/pokemon/{pokemon1}"
        url2 = f"{base_url}/pokemon/{pokemon2}"

        response1 = requests.get(url1)
        response2 = requests.get(url2)

        if response1.status_code == 200 and response2.status_code == 200:
            pokemon_data1 = response1.json()
            pokemon_data2 = response2.json()

            types1 = [t['type']['name'] for t in pokemon_data1['types']]
            types2 = [t['type']['name'] for t in pokemon_data2['types']]

            advantage1 = False
            advantage2 = False

            for t in types1:

                print(t)
                print("Pokemon 2 takes double damage from these types:")

                for slot in pokemon_data2['types']:
                    pokemon2_type_response = requests.get(slot['type']['url'])
                    data = pokemon2_type_response.json()


                    print(data['damage_relations']['double_damage_from'])

                    for types in data['damage_relations']['double_damage_from']:
                        if t in types['name']:
                            advantage1 = True


            for t in types2:

                print(t)
                print("Pokemon 1 takes double damage from these types:")

                for slot in pokemon_data1['types']:
                    pokemon1_type_response = requests.get(slot['type']['url'])
                    data = pokemon1_type_response.json()


                    print(data['damage_relations']['double_damage_from'])

                    for types in data['damage_relations']['double_damage_from']:
                        if t in types['name']:
                            advantage2 = True

            result = {
                'pokemon1': {
                    'name': pokemon_data1['name'],
                    'types': types1,
                    'sprite_url': pokemon_data1['sprites']['front_default'],
                    'advantage': advantage1
                },
                'pokemon2': {
                    'name': pokemon_data2['name'],
                    'types': types2,
                    'sprite_url': pokemon_data2['sprites']['front_default'],
                    'advantage': advantage2
                }
            }
        else:
            print("Error retrieving pokemon data")

    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)