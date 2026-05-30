from fastapi import FastAPI
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

engine = create_engine("sqlite://", echo=True)
SessionLocal = sessionmaker(autoflush=False, bind=engine)
Db = SessionLocal()

class Base(DeclarativeBase):
    pass

Base.metadata.create_all(bind=engine)

class Pokemon:
    name: str
    id: int
    height: int
    weight: int
    types: list[str]
    level: int
    sprites: dict[str, str]

class PokemonDB(Base):
    __tablename__ = "pokemons"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    height: Mapped[int] = mapped_column(Integer)
    weight: Mapped[int] = mapped_column(Integer)
    types: Mapped[list[str]] = mapped_column(JSON)
    level: Mapped[int] = mapped_column(Integer)
    sprites: Mapped[dict[str, str]] = mapped_column(JSON)


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
            "sprites": pokemon.sprites
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