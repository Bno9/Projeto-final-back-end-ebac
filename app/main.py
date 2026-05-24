from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pydantic
import requests

app = FastAPI()

@app.get("/pokemons")
def get_pokemons(limit: int = 10, offset: int = 10) -> dict:
    response = requests.get(f"https://pokeapi.co/api/v2/pokemon?limit={limit}&offset={offset}")
    data = response.json()
    
    return {
        "data": data,
        "pagination": {
            "total": len(data["results"]),
            "limit": limit,
            "offset": offset,
            "next": f"https://pokeapi.co/api/v2/pokemon?limit={limit}&offset={offset+limit}",
            "previous": f"https://pokeapi.co/api/v2/pokemon?limit={limit}&offset={max(0, offset-limit)}" if offset > 0 else None,
        }
    }

@app.get("/pokemons/{id}")
def get_pokemon_by_id(id: int) -> dict:
    response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{id}")
    data = response.json()

    weight = data["weight"]
    height = data["height"]

    sprites = data["sprites"]
    back_default, front_default = sprites["back_default"], sprites["front_default"]

    level = data["base_experience"] // 20 #fiz um sistema default que o pokemon upa 1 nivel a cada 20 de base_experience, mas isso é só um exemplo, pode ser qualquer coisa
    types = data["types"]

    return {
        "name": data["name"],
        "id": id,
        "height": height,
        "weight": weight,
        "types": [t["type"]["name"] for t in types],
        "level": level,
        "sprites": {
            "front_default": front_default,
            "back_default": back_default,
        }
    }