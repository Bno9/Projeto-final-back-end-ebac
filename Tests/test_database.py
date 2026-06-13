import pytest
from fastapi.testclient import TestClient
from app.main import app
from database.db import get_db, r
from database.modelos import PokemonDB
from unittest.mock import MagicMock
from Tests.test_endpoint import charmander
import json

client = TestClient(app)

def test_banco_de_dados_verifica_chamada(charmander, mocker):

    mock_db = MagicMock()
    mock_db.query.return_value.filter_by.return_value.first.return_value = None

    app.dependency_overrides[get_db] = lambda: mock_db

    response = client.post(f"/criar-pokemon", json=charmander)

    app.dependency_overrides.clear()

    mock_db.commit.assert_called_once()
    mock_db.add.assert_called_once()

def test_banco_de_dados_verifica_pokemon_existente(charmander, mocker):

    mock_db = MagicMock()

    mock_db.query.return_value.filter_by().first.return_value = PokemonDB(
        name=charmander["name"],
        height=charmander["height"],
        weight=charmander["weight"],
        types=charmander["types"],
        level=charmander["level"]
    )

    app.dependency_overrides[get_db] = lambda: mock_db
    
    client.post(f"/criar-pokemon", json=charmander)

    app.dependency_overrides.clear()

    mock_db.add.assert_not_called()
    mock_db.commit.assert_not_called()

def test_banco_de_dados_cria_pokemon(charmander, mocker):

    mock_db = MagicMock()

    mock_db.query.return_value.filter_by().first.return_value = None

    app.dependency_overrides[get_db] = lambda: mock_db

    response = client.post(f"/criar-pokemon", json=charmander)

    app.dependency_overrides.clear()

    mock_db.commit.assert_called_once()
    mock_db.add.assert_called_once()

def test_redis_set_cache(charmander, mocker):

    mock_redis = MagicMock()
    mocker.patch("routes.pokeapi.r", mock_redis)

    mock_redis.hgetall.return_value = {}

    response = client.get(f"/pokeapi/{charmander['id']}")
   
    mock_redis.hset.assert_called_once_with(f"pokemon:{charmander['id']}",
        mapping={
            "name": charmander["name"],
            "id": charmander["id"],
            "height": charmander["height"],
            "weight": charmander["weight"],
            "types": json.dumps(charmander["types"]),
            "level": charmander["level"],
            "sprites": json.dumps(charmander["sprites"])
            })
    mock_redis.expire.assert_called_once()

def test_redis_get_cache(charmander, mocker):

    mock_redis = MagicMock()
    mocker.patch("routes.pokeapi.r", mock_redis)

    cached_data = {
    "name": charmander["name"],
    "id": charmander["id"],
    "height": charmander["height"],
    "weight": charmander["weight"],
    "types": json.dumps(charmander["types"]),
    "level": charmander["level"],
    "sprites": json.dumps(charmander["sprites"]),
    "message": "Pokemon encontrado no cache e retornado em 0.00 segundos"
    }

    expected = {
        "name": charmander["name"],
        "id": charmander["id"],
        "height": charmander["height"],
        "weight": charmander["weight"],
        "types": charmander["types"],
        "level": charmander["level"],
        "sprites": charmander["sprites"],
        "message": "Pokemon encontrado no cache e retornado em 0.00 segundos"
    }

    mock_redis.hgetall.return_value = cached_data

    response = client.get(f"/pokeapi/{charmander['id']}")

    mock_redis.hgetall.assert_called_once_with(f"pokemon:{charmander['id']}")
    assert response.json() == expected