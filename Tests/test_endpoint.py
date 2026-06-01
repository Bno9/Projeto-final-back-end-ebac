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

def test_banco_de_dados(charmander, mocker):
    """
    endpoint /pokemons/{id} deve utilizar o banco de dados para verificar se o pokemon já existe antes de fazer a requisição para a pokeapi.co
    """

    mock_db = mocker.patch("app.main.Db")

    response = client.get(f"/pokemons/{charmander['id']}")

    mock_db.query.assert_called_with(PokemonDB)

    mock_db.query().filter_by.assert_called_with(id=charmander["id"])

    existe = mock_db.query(PokemonDB).filter_by(id=charmander["id"]).first()

    if not existe:
        mock_db.add.assert_called_once_with(PokemonDB(
            id=charmander["id"],
            name=charmander["name"],
            height=charmander["height"],
            weight=charmander["weight"],
            types=charmander["types"],
            level=charmander["level"],
            sprites=charmander["sprites"],
         ))
        mock_db.commit.assert_called_once()
