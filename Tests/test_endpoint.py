import pytest
from fastapi.testclient import TestClient
from app.main import app

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
            "total": 1000,
            "limit": 10,
            "offset": 10,
            "next": "https://pokeapi.co/api/v2/pokemon?limit=10&offset=20",
            "previous": "https://pokeapi.co/api/v2/pokemon?limit=10&offset=0"
        }
    }

    assert response.status_code == 200

def test_endpoint_pokemon_por_id(charmander):
    """
    endpoint /pokemons/{id} deve retornar um json de pokemons da pokeapi.co
    """

    response = client.get(f"/pokemons/{charmander['id']}")

    assert response.json() == {
        "name": charmander["name"],
        "id": charmander["id"],
        "height": charmander["height"],
        "weight": charmander["weight"],
        "types": charmander["types"],
        "level": charmander["level"],
        "sprites": charmander["sprites"]
        }

    assert response.status_code == 200