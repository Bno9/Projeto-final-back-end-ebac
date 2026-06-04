from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine
from sqlalchemy import Integer, JSON, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase
from pydantic import BaseModel
from typing import Optional
import requests

app = FastAPI()

engine = create_engine("sqlite:///pokemon.db", echo=True)
SessionLocal = sessionmaker(autoflush=False, bind=engine)
Db = SessionLocal()

class Base(DeclarativeBase):
    pass

class Pokemon(BaseModel):
    name: str
    height: int
    weight: int
    types: list[str]
    level: int

class PokemonDB(Base):
    __tablename__ = "pokemons"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    height: Mapped[int] = mapped_column(Integer)
    weight: Mapped[int] = mapped_column(Integer)
    types: Mapped[list[str]] = mapped_column(JSON)
    level: Mapped[int] = mapped_column(Integer)
    sprites: Mapped[dict[str, str]] = mapped_column(JSON)


Base.metadata.create_all(bind=engine)


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

    pokemon = Db.query(PokemonDB).filter_by(id=id).first()

    if pokemon:
        return {
            "name": pokemon.name,
            "id": pokemon.id,
            "height": pokemon.height,
            "weight": pokemon.weight,
            "types": pokemon.types,
            "level": pokemon.level,
            "sprites": pokemon.sprites,

            
            "message": "Pokemon encontrado no banco de dados"
        }

    response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{id}")
    data = response.json()

    weight = data["weight"]
    height = data["height"]

    sprites = data["sprites"]
    back_default, front_default = sprites["back_default"], sprites["front_default"]

    level = data["base_experience"] // 20 #fiz um sistema default que o pokemon upa 1 nivel a cada 20 de base_experience, mas isso é só um exemplo, pode ser qualquer coisa
    types = data["types"]

    Db.add(PokemonDB(
        id=id,
        name=data["name"],
        height=height,
        weight=weight,
        types=[t["type"]["name"] for t in types],
        level=level,
        sprites={
            "front_default": front_default,
            "back_default": back_default,
        }
    ))

    Db.commit()

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
        },
        
        "message": "Pokemon encontrado na API e adicionado ao banco de dados"
    }

@app.post("/criar-pokemon")
def create_pokemon(pokemon: Pokemon) -> dict:

    pokemondb = Db.query(PokemonDB).filter_by(id=pokemon.name).first()

    if pokemondb:
        raise HTTPException(
        status_code=409, 
        detail=f"Pokemon {pokemon.name} já existe no banco de dados")

    Db.add(PokemonDB(
        name=pokemon.name,
        height=pokemon.height,
        weight=pokemon.weight,
        types=pokemon.types,
        level=pokemon.level
    ))

    Db.commit()

    return {
        "message": f"Pokemon {pokemon.name} adicionado ao banco de dados",
    }

@app.put("/atualizar-pokemon/{name}")
def update_pokemon(name: str, pokemon: Pokemon) -> dict:
    
    pokemondb = Db.query(PokemonDB).filter_by(id=pokemon.name).first()

    if not pokemondb:
        raise HTTPException(
            status_code=404,
            detail=f"O pokemon {name} não foi encontrado no banco de dados")
    
    pokemondb.height = pokemon.height
    pokemondb.weight = pokemon.weight
    pokemondb.types = pokemon.types
    pokemondb.level = pokemon.level

    Db.commit()

    return {
        "message": f"Informações do pokemon {name} atualizadas com sucesso"
    }