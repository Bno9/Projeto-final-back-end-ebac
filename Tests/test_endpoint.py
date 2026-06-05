import pytest
from fastapi.testclient import TestClient
from app.main import app, PokemonDB, get_db
from unittest.mock import MagicMock

client = TestClient(app)


# -------------------------
# FIXTURES
# -------------------------

@pytest.fixture()
def charmander():
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
        "id": 7,
        "height": 5,
        "weight": 90,
        "types": ["water"],
        "level": 3,
        "sprites": {
            "front_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/7.png",
            "back_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/back/7.png",
        }
    }


# -------------------------
# FIXTURE DO FAKE DB
# -------------------------

@pytest.fixture()
def fake_db():
    db = MagicMock()

    db.query.return_value.filter_by.return_value.first.return_value = None
    db.query.return_value.all.return_value = []

    return db


@pytest.fixture(autouse=True)
def override_dependency(fake_db):
    """
    Sobrescreve a dependência global do FastAPI
    """
    app.dependency_overrides[get_db] = lambda: fake_db
    yield
    app.dependency_overrides.clear()


# -------------------------
# TESTES
# -------------------------

def test_endpoint_all_pokemons(fake_db):

    fake_db.query.return_value.all.return_value = []

    response = client.get("/pokemons")

    assert response.status_code == 200


def test_endpoint_pokemon_por_id(charmander, fake_db):

    fake_db.query.return_value.filter_by.return_value.first.return_value = None

    response = client.get(f"/pokemons/{charmander['id']}")

    assert response.status_code == 200
    assert response.json()["id"] == charmander["id"]


def test_endpoint_criar_pokemon(charmander, fake_db):

    fake_db.query.return_value.filter_by.return_value.first.return_value = None

    response = client.post("/criar-pokemon", json=charmander)

    assert response.status_code == 200
    assert response.json() == {
        "message": f"Pokemon {charmander['name']} adicionado ao banco de dados",
    }


def test_endpoint_criar_pokemon_ja_existente(charmander, fake_db):

    fake_db.query.return_value.filter_by.return_value.first.return_value = PokemonDB(
        name=charmander["name"],
        height=charmander["height"],
        weight=charmander["weight"],
        types=charmander["types"],
        level=charmander["level"]
    )

    response = client.post("/criar-pokemon", json=charmander)

    assert response.status_code == 409


def test_endpoint_atualizar_pokemon(charmander, squirtle, fake_db):

    fake_db.query.return_value.filter_by.return_value.first.return_value = PokemonDB(
        name=charmander["name"],
        height=charmander["height"],
        weight=charmander["weight"],
        types=charmander["types"],
        level=charmander["level"]
    )

    response = client.put(f"/atualizar-pokemon/{charmander['name']}", json=squirtle)

    assert response.status_code == 200


def test_endpoint_atualizar_pokemon_nao_existente(charmander, fake_db):

    fake_db.query.return_value.filter_by.return_value.first.return_value = None

    response = client.put(f"/atualizar-pokemon/{charmander['name']}", json=charmander)

    assert response.status_code == 404


def test_endpoint_deletar_pokemon_nao_existente(charmander, fake_db):

    fake_db.query.return_value.filter_by.return_value.first.return_value = None

    response = client.delete(f"/deletar-pokemon/{charmander['name']}")

    assert response.status_code == 404


def test_endpoint_deletar_pokemon_existente(charmander, fake_db):

    fake_db.query.return_value.filter_by.return_value.first.return_value = PokemonDB(
        name=charmander["name"],
        height=charmander["height"],
        weight=charmander["weight"],
        types=charmander["types"],
        level=charmander["level"]
    )

    response = client.delete(f"/deletar-pokemon/{charmander['name']}")

    assert response.status_code == 200


def test_endpoint_get_pokemon_nao_existente(charmander, fake_db):

    fake_db.query.return_value.filter_by.return_value.first.return_value = None

    response = client.get(f"/pokemons-criados/{charmander['name']}")

    assert response.status_code == 404


def test_endpoint_get_pokemon_por_nome(charmander, squirtle, fake_db):

    pokemons = [
        PokemonDB(
            name=charmander["name"],
            height=charmander["height"],
            weight=charmander["weight"],
            types=charmander["types"],
            level=charmander["level"]
        ),
        PokemonDB(
            name=squirtle["name"],
            height=squirtle["height"],
            weight=squirtle["weight"],
            types=squirtle["types"],
            level=squirtle["level"]
        )
    ]

    fake_db.query.return_value.all.return_value = pokemons

    response = client.get("/pokemons-criados")

    assert response.status_code == 200
    assert response.json()["message"] == f"{len(pokemons)} pokemons no banco de dados"