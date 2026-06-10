from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine
from sqlalchemy import Integer, JSON, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase
from pydantic import BaseModel, Field, field_validator
import requests
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///:memory:")

app = FastAPI()

engine = create_engine(
    DATABASE_URL,
    echo=True
)
SessionLocal = sessionmaker(autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Base(DeclarativeBase):
    pass

#Classe do tipo Pydantic, usada para validar os dados de entrada do usuario na criação e atualização de pokemons criados pelo usuario
class Pokemon(BaseModel):
    name: str

    @field_validator("name")
    @classmethod
    def validar_nome(cls, value):

        if not value.strip():
            raise ValueError("Nome inválido")

        return value
    
    height: int = Field(description="Altura do pokemon, deve ser um número inteiro positivo", ge=1)
    weight: int = Field(description="Peso do pokemon, deve ser um número inteiro positivo", ge=1)
    types: list[str] = Field(min_length=1, description="Lista de tipos do pokemon, deve conter pelo menos um tipo")
    level: int = Field(description="Level permitido do pokemon", ge=1, le=100)

#Classe do tipo SQLAlchemy, usada para mapear a tabela de pokemons no banco de dados, e armazenar os pokemons da pokeapi.co
class PokemonDBAPI(Base):
    __tablename__ = "pokemons"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    height: Mapped[int] = mapped_column(Integer)
    weight: Mapped[int] = mapped_column(Integer)
    types: Mapped[list[str]] = mapped_column(JSON)
    level: Mapped[int] = mapped_column(Integer)
    sprites: Mapped[dict[str, str]] = mapped_column(JSON)

#Classe do tipo SQLAlchemy, usada para mapear a tabela de pokemons no banco de dados, e armazenar os pokemons criados pelo usuario
class PokemonDB(Base):
    __tablename__ = "pokemons_user"
    name: Mapped[str] = mapped_column(String(30), primary_key=True)
    height: Mapped[int] = mapped_column(Integer)
    weight: Mapped[int] = mapped_column(Integer)
    types: Mapped[list[str]] = mapped_column(JSON)
    level: Mapped[int] = mapped_column(Integer)

#Criando as tabelas no banco de dados, caso elas ainda não existam
Base.metadata.create_all(bind=engine)

@app.get("/pokemons")
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

@app.get("/pokemons/{id}")
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


#Como foram feitas duas propostas diferente de projeto e não ficou definido qual deveria ser feita, resolvi fazer as duas. Acima são os endpoints para buscar pokemons na pokeapi, e abaixo estão os endpoints para criar, atualizar, deletar e buscar pokemons criados pelo usuario.

@app.post("/criar-pokemon")
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

@app.put("/atualizar-pokemon/{old_name}")
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

@app.delete("/deletar-pokemon/{name}")
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

@app.get("/pokemons-criados/{name}")
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

@app.get("/pokemons-criados")
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