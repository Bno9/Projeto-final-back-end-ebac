import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.fixture(scope="module")
def charmander():
    """
    Fixture para criar um pokemon charmander (usando só de modelo para lembrar o que deve ser retornado pela pokeapi.co)
    """
    return {
        "name": "charmander",
        "id": 4,
        "height": 0.6,
        "weight": 8.5,
        "types": ["fire"],
        "level": 5,
        "sprites": {
            "front_default": "",
            "back_default": "",
        }
    }

def test_endpoint_all_pokemons():
    """
    endpoint /pokemons deve retornar um json de pokemons da pokeapi.co
    """
    response = client.get("/pokemons")

    assert response.json() == {
        "data": "",
        "pagination": {
            "total": 0,
            "limite": "",
            "offset": "",
            "next": "",
            "previous": None
        }
    }

    assert response.status_code == 200

def test_endpoint_pokemon_por_id():
    """
    endpoint /pokemons/{id} deve retornar um json de pokemons da pokeapi.co
    """
    response = client.get("/pokemons/1")

    assert response.json() == {
        "data": "",
        "pagination": {
            "total": 0,
            "limite": "",
            "offset": "",
            "next": "",
            "previous": None
        }
    }

    assert response.status_code == 200