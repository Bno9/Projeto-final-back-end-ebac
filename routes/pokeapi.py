from database.db import r
from fastapi import Depends, APIRouter, HTTPException
import time
import requests
import json

router = APIRouter()
#todas rotas aqui tem um prefixo de "pokeapi", então na hora de testar a rota, coloque /pokeapi/ antes 

@router.get("/all", tags=["PokeAPI"])
def get_pokemons(limit: int = 10, offset: int = 10) -> dict:
    """
    Retorna um json de pokemons da pokeapi.co, com paginação usando os query params limit e offset
    
    Parâmetros:
    - limit: número de pokemons a serem retornados (padrão: 10)
    - offset: número de pokemons a serem pulados antes de começar a retornar os resultados (padrão: 10)
    
    Retorna:
    - data: lista de pokemons retornados pela pokeapi.co
    - pagination: informações sobre a paginação, incluindo total de pokemons, limite, offset, e links para a próxima e anterior página
    """
    comeco = time.time()

    cached_data = r.get(f"https://pokeapi.co/api/v2/pokemon?limit={limit}&offset={offset}")

    if cached_data:
        return {
            "data": json.loads(cached_data),
            "pagination": {
                "total": limit,
                "limit": limit,
                "offset": offset,
                "next": f"https://pokeapi.co/api/v2/pokemon?limit={limit}&offset={offset+limit}",
                "previous": f"https://pokeapi.co/api/v2/pokemon?limit={limit}&offset={max(0, offset-limit)}" if offset > 0 else None,

                "message": f"Dados encontrados no cache e retornados em {time.time() - comeco:.2f} segundos"
            }
        }

    response = requests.get(f"https://pokeapi.co/api/v2/pokemon?limit={limit}&offset={offset}")
    data = response.json()

    r.setex(f"https://pokeapi.co/api/v2/pokemon?limit={limit}&offset={offset}", 300, json.dumps(data)) #cacheia a resposta por 5 minutos
    
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
def get_pokemon_by_id(id: int) -> dict:
    """
    Retorna um json de um pokemon especifico da pokeapi.co, usando o id do pokemon como parametro de rota.
    Se o pokemon já existir no banco de dados, deve retornar os dados do pokemon do banco de dados, caso contrário, deve buscar os dados na pokeapi.co, 
    adicionar ao banco de dados e retornar os dados do pokemon
      
    Parametros:
    - id: id do pokemon a ser buscado
      
    Retorno: 
    - dicionario com os dados do pokemon, incluindo nome, id, altura, peso, tipos, level e sprites, e uma mensagem indicando se o pokemon foi encontrado no banco de dados ou na API
    """

    comeco = time.time()

    pokemon = r.hgetall(f"pokemon:{id}")

    if pokemon:
        return {
            "name": pokemon["name"],
            "id": int(pokemon["id"]),
            "height": float(pokemon["height"]),
            "weight": float(pokemon["weight"]),
            "types": json.loads(pokemon["types"]),
            "level": int(pokemon["level"]),
            "sprites": json.loads(pokemon["sprites"]),

            
            "message": f"Pokemon encontrado no cache e retornado em {time.time() - comeco:.2f} segundos"
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

    r.hset(
        f"pokemon:{id}",
        mapping={
            "name": data["name"],
            "id": id,
            "height": float(height),
            "weight": float(weight),
            "types": json.dumps([t["type"]["name"] for t in types]),
            "level": level,
            "sprites": json.dumps({
                "front_default": front_default,
                "back_default": back_default
            })
        }
    )

    r.expire(f"pokemon:{id}", 300) #expira o cache em 5 minutos

    return {
        "name": data["name"],
        "id": id,
        "height": float(height),
        "weight": float(weight),
        "types": [t["type"]["name"] for t in types],
        "level": level,
        "sprites": {
            "front_default": front_default,
            "back_default": back_default,
        },
        
        "message": f"Pokemon encontrado na API e adicionado ao cache, retornado em {time.time() - comeco:.2f} segundos"
    }
