from database.db import get_db
from database.modelos import PokemonDBAPI
from fastapi import Depends, APIRouter, HTTPException
import requests

router = APIRouter()
#todas rotas aqui tem um prefixo de "pokeapi", então na hora de testar a rota, coloque /pokeapi/ antes 

@router.get("/all", tags=["PokeAPI"])
def get_pokemons(limit: int = 10, offset: int = 10, Db=Depends(get_db)) -> dict:
    """
    Retorna um json de pokemons da pokeapi.co, com paginação usando os query params limit e offset
    
    Parâmetros:
    - limit: número de pokemons a serem retornados (padrão: 10)
    - offset: número de pokemons a serem pulados antes de começar a retornar os resultados (padrão: 10)
    
    Retorna:
    - data: lista de pokemons retornados pela pokeapi.co
    - pagination: informações sobre a paginação, incluindo total de pokemons, limite, offset, e links para a próxima e anterior página
    """

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

@router.get("/{id}", tags=["PokeAPI"])
def get_pokemon_by_id(id: int, Db=Depends(get_db)) -> dict:
    """
    Retorna um json de um pokemon especifico da pokeapi.co, usando o id do pokemon como parametro de rota.
    Se o pokemon já existir no banco de dados, deve retornar os dados do pokemon do banco de dados, caso contrário, deve buscar os dados na pokeapi.co, 
    adicionar ao banco de dados e retornar os dados do pokemon
      
    Parametros:
    - id: id do pokemon a ser buscado
      
    Retorno: 
    - dicionario com os dados do pokemon, incluindo nome, id, altura, peso, tipos, level e sprites, e uma mensagem indicando se o pokemon foi encontrado no banco de dados ou na API
    """

    pokemon = Db.query(PokemonDBAPI).filter_by(id=id).first()

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

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail=f"Erro ao buscar pokemon com id {id} na pokeapi.co: {response.text}"
        )

    data = response.json()

    weight = data["weight"]
    height = data["height"]

    sprites = data["sprites"]
    back_default, front_default = sprites["back_default"], sprites["front_default"]

    level = data["base_experience"] // 20 #fiz um sistema default que o pokemon upa 1 nivel a cada 20 de base_experience, mas isso é só um exemplo, pode ser qualquer coisa
    types = data["types"]

    Db.add(PokemonDBAPI(
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
