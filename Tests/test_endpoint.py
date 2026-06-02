import pytest
from fastapi.testclient import TestClient
from app.main import app, PokemonDB
from pytest_mock import mocker

client = TestClient(app)

@pytest.fixture()
def charmander():
    """
    Fixture para criar um pokemon charmander (id 4) para ser usado nos testes, usando os dados da pokeapi.co
    """
    return {
        "name": "charmander",
        "id": 4,
        "height": 6,
        "weight": 85,
        "types": ["fire"],
        "level": 3,
        "sprites": {
            "front_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/4.png",
            "back_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/back/4.png",
        }
    }

def test_endpoint_all_pokemons():
    """
    endpoint /pokemons deve retornar um json de pokemons da pokeapi.co
    """
    response = client.get("/pokemons")

    assert response.json() == {
        "data": response.json()["data"],
        "pagination": {
            "total": 10,
            "limit": 10,
            "offset": 10,
            "next": "https://pokeapi.co/api/v2/pokemon?limit=10&offset=20",
            "previous": "https://pokeapi.co/api/v2/pokemon?limit=10&offset=0"
        }
    }

    assert response.status_code == 200

def test_endpoint_pokemon_por_id(charmander, mocker):
    """
    endpoint /pokemons/{id} deve retornar um json de pokemons da pokeapi.co
    """

    mock_db = mocker.patch("app.main.Db")
    mock_db.query.return_value.filter_by().first.return_value = None

    response = client.get(f"/pokemons/{charmander['id']}")



    assert response.json() == {
        "name": charmander["name"],
        "id": charmander["id"],
        "height": charmander["height"],
        "weight": charmander["weight"],
        "types": charmander["types"],
        "level": charmander["level"],
        "sprites": charmander["sprites"],

        "message": "Pokemon encontrado na API e adicionado ao banco de dados"
        }

    assert response.status_code == 200

def test_endpoint_criar_pokemon(charmander, mocker):
    """
    endpoint /criar-pokemon/{id} deve criar um pokemons novo no banco de dados, usando os dados passados pelo usuario, e retornar um json de confirmação
    """

    mock_db = mocker.patch("app.main.Db")
    mock_db.query.return_value.filter_by().first.return_value = None

    response = client.post("/criar-pokemon", json=charmander)

    assert response.json() == {
        "message": f"Pokemon {charmander['name']} adicionado ao banco de dados",
        }

    assert response.status_code == 200

def test_endpoint_criar_pokemon_pokemon_ja_existe(charmander, mocker):
    """
    endpoint /criar_pokemon/{id} deve criar um pokemons novo no banco de dados, usando os dados passados pelo usuario, e retornar um json de confirmação
    """

    mock_db = mocker.patch("app.main.Db")
    mock_db.query.return_value.filter_by().first.return_value = PokemonDB(
        id=charmander["id"],
        name=charmander["name"],
        height=charmander["height"],
        weight=charmander["weight"],
        types=charmander["types"],
        level=charmander["level"],
        sprites=charmander["sprites"],
     )

    response = client.post("/criar-pokemon", json=charmander)

    assert response.json() == {
        "message": f"Pokemon {charmander['name']} já existe no banco de dados",
        }

    assert response.status_code == 400