import requests
import re
import random


def pokeapi() -> dict:
    random_pokemon_id = random.randint(1, 9)
    pokeapi_url = f"https://pokeapi.co/api/v2/pokemon-species/{random_pokemon_id}"
    response = requests.get(url=pokeapi_url)
    response.encoding = "utf-8"
    data = response.json()
    pokemon_name = data["name"].title()
    pokemon_description = next(
        (
            item["flavor_text"]
            for item in data["flavor_text_entries"]
            if item["language"]["name"] == "en"
        ),
        None,
    )

    pokemon_description = pokemon_description.replace("POKéMON", "Pokemon")
    pokemon_description = re.sub(r"\s+", " ", pokemon_description)
    pokemon_description = re.sub(r"\n+", " ", pokemon_description)

    pokemon_description = pokemon_description.strip()

    pokemon_color = data["color"]["name"]

    return {
        "name": pokemon_name,
        "description": pokemon_description,
        "color": pokemon_color,
    }
