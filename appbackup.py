from flask import Flask, render_template

import requests
from random import randint

app: Flask = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/generated_pokemon")
def generate_pokemon():
    generated: Pokemon = Pokemon(id = randint(1,905))
    pokemon_name: str = generated.get_name()
    pokemon_type: list[str] = generated.get_type()
    pokemon_height: int = generated.get_height()
    pokemon_image: str = generated.get_image()
    id = generated.id
    return render_template('generated_pokemon.html', pokemon_name = pokemon_name.capitalize(), pokemon_type = pokemon_type, pokemon_height = pokemon_height, pokemon_image = pokemon_image, id = id)

class Pokemon: 
    type: str
    name: str
    height: int
    id: int
    image: str

    def __init__(self, type = "", name = "", height = 69, id = 420, image = "") -> None:
        self.type = type
        self.name = name
        self.height = height
        self.id = id
        self.image = image

    def get_name(self) -> str:
        pokemon_api_url: str = f"https://pokeapi.co/api/v2/pokemon/{self.id}"
        data = requests.get(pokemon_api_url)
        # response: dict[str,list[dict[str,str]]] = data.json()
        pokemon_dictionary = data.json()
        # is a dictionary with all the categories about the pokemon
        # list is a breakdown of the categories into name and url
        return pokemon_dictionary["name"]

    def get_type(self) -> str:
        pokemon_api_url: str = f"https://pokeapi.co/api/v2/pokemon/{self.id}"
        data = requests.get(pokemon_api_url)
        pokemon_dictionary = data.json()
        pokemon_types: list[str] = []
        for i in range(len(pokemon_dictionary["types"])):
            pokemon_types.append(pokemon_dictionary["types"][i]["type"]["name"])
        pokemon_types_string = str(pokemon_types)
        return pokemon_types_string.lstrip(pokemon_types_string[0]).rstrip(pokemon_types_string[-1])


    def get_height(self) -> float:
        pokemon_api_url: str = f"https://pokeapi.co/api/v2/pokemon/{self.id}"
        data = requests.get(pokemon_api_url)
        pokemon_dictionary = data.json()
        return pokemon_dictionary["height"] / 10

    def get_image(self) -> str:
        if (self.id < 100 and self.id > 10):
            pokemon_image: str = f"https://assets.pokemon.com/assets/cms2/img/pokedex/detail/0{self.id}.png"
        elif (self.id < 10):
            pokemon_image: str = f"https://assets.pokemon.com/assets/cms2/img/pokedex/detail/00{self.id}.png"
        else:
            pokemon_image: str = f"https://assets.pokemon.com/assets/cms2/img/pokedex/detail/{self.id}.png"
        return pokemon_image
        
        


if __name__ == '__main__':
    app.run(debug=True)