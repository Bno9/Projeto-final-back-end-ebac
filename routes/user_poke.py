
from fastapi import APIRouter, Depends, HTTPException
from database.modelos import Pokemon, PokemonDB
from database.db import get_db

router = APIRouter()

@router.post("/criar-pokemon", tags=["Usuario"])
def create_pokemon(pokemon: Pokemon, Db=Depends(get_db)) -> dict:
    """
    Cria um pokemon novo no banco de dados usando os dados passados pelo usuario
    
    Parametros:
    - pokemon: objeto do tipo Pokemon, contendo os dados do pokemon a ser criado, incluindo nome, altura, peso, tipos e level
    
    Retorno:
    - dicionario com uma mensagem de confirmação indicando que o pokemon foi adicionado ao banco de dados, ou um erro caso o pokemon já exista no banco de dados
    """

    pokemondb = Db.query(PokemonDB).filter_by(name=pokemon.name).first()

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

@router.put("/atualizar-pokemon/{old_name}", tags=["Usuario"])
def update_pokemon(old_name: str, pokemon: Pokemon, Db=Depends(get_db)) -> dict:
    """
    Atualiza as informações de um pokemon já existente no banco de dados, 
    usando o nnome do pokemon como parametro de rota e os dados atualizados passados pelo usuario no corpo da requisição
    
    Parametros: 
    - name: nome do pokemon a ser atualizado
    - pokemon: objeto do tipo Pokemon, contendo os dados atualizados do pokemon, incluindo nome, altura, peso, tipos e level
        
    Retorno:
    - dicionario com uma mensagem de confirmação indicando que as informações do pokemon foram atualizadas com sucesso, ou um erro caso o pokemon não exista no banco de dados
    """
    
    pokemondb = Db.query(PokemonDB).filter_by(name=old_name).first()

    if not pokemondb:
        raise HTTPException(
            status_code=404,
            detail=f"O pokemon {old_name} não foi encontrado no banco de dados")
    
    pokemondb.name = pokemon.name
    pokemondb.height = pokemon.height
    pokemondb.weight = pokemon.weight
    pokemondb.types = pokemon.types
    pokemondb.level = pokemon.level

    Db.commit()

    return {
        "message": f"Informações do pokemon {old_name} atualizadas com sucesso"
    }

@router.delete("/deletar-pokemon/{name}", tags=["Usuario"])
def delete_pokmeon(name: str, Db=Depends(get_db)) -> dict:
    """
    Exclui um pokemon do banco de dados, usando o nome do pokemon como parametro de rota
    
    Parametros:
    - name: nome do pokemon a ser deletado
    
    Retorno:
    - dicionario com uma mensagem de confirmação indicando que o pokemon foi removido do banco de dados, ou um erro caso o pokemon não exista no banco de dados
    """

    pokemondb = Db.query(PokemonDB).filter_by(name=name).first()

    if not pokemondb:
        raise HTTPException(
            status_code=404,
            detail=f"O pokemon {name} não foi encontrado no banco de dados")
    
    Db.delete(pokemondb)
    Db.commit()

    return {
        "message": f"Pokemon {name} removido do banco de dados"
    }

@router.get("/pokemons-criados/{name}", tags=["Usuario"])
def get_pokemon_by_name(name: str, Db=Depends(get_db)) -> dict:
    """
    Retorna um json de um pokemon criado pelo usuario, usando o nome do pokemon como parametro de rota.
    Se o pokemon existir no banco de dados, deve retornar os dados do pokemon, caso contrário, deve retornar um erro indicando que o pokemon não foi encontrado no banco de dados
    """
    
    pokemon = Db.query(PokemonDB).filter_by(name=name).first()

    if pokemon:
        return {
            "name": pokemon.name,
            "height": pokemon.height,
            "weight": pokemon.weight,
            "types": pokemon.types,
            "level": pokemon.level,

            
            "message": "Pokemon encontrado no banco de dados"
        }

    raise HTTPException(
        status_code=404,
        detail=f"O pokemon {name} não foi encontrado no banco de dados")

@router.get("/pokemons-criados", tags=["Usuario"])
def get_created_pokemons(Db=Depends(get_db)) -> dict:
    """
    Retorna um json de todos os pokemons criados pelo usuario, buscando os dados no banco de dados
    """

    pokemons = Db.query(PokemonDB).all()

    if not pokemons:
        raise HTTPException(
            status_code=404,
            detail="Nenhum pokemon criado pelo usuario encontrado no banco de dados")   

    return {
        "data": [
            {
                "name": pokemon.name,
                "height": pokemon.height,
                "weight": pokemon.weight,
                "types": pokemon.types,
                "level": pokemon.level
            }
            for pokemon in pokemons
        ],
        "message": f"{len(pokemons)} pokemons no banco de dados"
    }