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

@pytest.fixture()
def squirtle():
    return {
        "name": "squirtle",
        "id": None,
        "height": 5,
        "weight": 90,
        "types": ["water"],
        "level": 3,
        "sprites": {
            "front_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/7.png",
            "back_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/back/7.png",
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

def test_endpoint_criar_pokemon_ja_existente(charmander, mocker):
    """
    endpoint /criar_pokemon/{id} deve criar um pokemons novo no banco de dados, usando os dados passados pelo usuario, e retornar um json de confirmação
    """

    mock_db = mocker.patch("app.main.Db")
    mock_db.query.return_value.filter_by().first.return_value = PokemonDB(
        name=charmander["name"],
        height=charmander["height"],
        weight=charmander["weight"],
        types=charmander["types"],
        level=charmander["level"]
     )

    response = client.post("/criar-pokemon", json=charmander)

    assert response.json() == {
        "detail": f"Pokemon {charmander['name']} já existe no banco de dados",
        }

    assert response.status_code == 409

def test_endpoint_atualizar_pokemon(charmander, squirtle, mocker):
    
    mock_db = mocker.patch("app.main.Db")
    mock_db.query.return_value.filter_by().first.return_value = PokemonDB(
        name=charmander["name"],
        height=charmander["height"],
        weight=charmander["weight"],
        types=charmander["types"],
        level=charmander["level"]
     )

    response = client.put(f"/atualizar-pokemon/{charmander['name']}", json=squirtle)

    assert response.json() == {
        "message": f"Informações do pokemon {charmander['name']} atualizadas com sucesso",
        }

    assert response.status_code == 200

def test_endpoint_atualizar_pokemon_nao_existente(charmander, mocker):
    
    mock_db = mocker.patch("app.main.Db")
    mock_db.query.return_value.filter_by().first.return_value = None

    response = client.put(f"/atualizar-pokemon/{charmander['name']}", json=charmander)

    assert response.json() == {
        "detail": f"O pokemon {charmander['name']} não foi encontrado no banco de dados",
        }

    assert response.status_code == 404

def test_endpoint_deletar_pokemon_nao_existente(charmander, mocker):
    
    mock_db = mocker.patch("app.main.Db")
    mock_db.query.return_value.filter_by().first.return_value = None

    response = client.delete(f"/deletar-pokemon/{charmander['name']}")

    assert response.json() == {
        "detail": f"O pokemon {charmander['name']} não foi encontrado no banco de dados",
        }

    assert response.status_code == 404

def test_endpoint_deletar_pokemon_existente(charmander, mocker):
    
    mock_db = mocker.patch("app.main.Db")
    mock_db.query.return_value.filter_by().first.return_value = PokemonDB(
        name=charmander["name"],
        height=charmander["height"],
        weight=charmander["weight"],
        types=charmander["types"],
        level=charmander["level"]
     )

    response = client.delete(f"/deletar-pokemon/{charmander['name']}")

    assert response.json() == {
        "message": f"Pokemon {charmander['name']} removido do banco de dados",
        }

    assert response.status_code == 200

def test_endpoint_get_pokemon_nao_existente(charmander, mocker):
    
    mock_db = mocker.patch("app.main.Db")
    mock_db.query.return_value.filter_by().first.return_value = None

    response = client.get(f"/pokemons/{charmander['name']}")

    assert response.json() == {
        "detail": f"O pokemon {charmander['name']} não foi encontrado no banco de dados",
        }

    assert response.status_code == 404

def test_endpoint_get_pokemon(charmander, mocker):
    
    mock_db = mocker.patch("app.main.Db")
    mock_db.query.return_value.filter_by().first.return_value = PokemonDB(
        name=charmander["name"],
        height=charmander["height"],
        weight=charmander["weight"],
        types=charmander["types"],
        level=charmander["level"]
    )

    response = client.get(f"/pokemons/{charmander['name']}")

    assert response.json() == {
        "detail": f"O pokemon {charmander['name']} não foi encontrado no banco de dados",
        }

    assert response.status_code == 404