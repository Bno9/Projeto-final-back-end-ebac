import pytest
from fastapi.testclient import TestClient
from app.main import app
from database.db import get_db
from database.modelos import PokemonDBAPI
from unittest.mock import MagicMock
from Tests.test_endpoint import charmander

client = TestClient(app)

def test_banco_de_dados_verifica_chamada(charmander, mocker):

    mock_db = MagicMock()
    mock_db.query.return_value.filter_by.return_value.first.return_value = None

    app.dependency_overrides[get_db] = lambda: mock_db

    response = client.get(f"/pokeapi/{charmander['id']}")

    app.dependency_overrides.clear()

    mock_db.commit.assert_called_once()
    mock_db.add.assert_called_once()

def test_banco_de_dados_verifica_pokemon_existente(charmander, mocker):

    mock_db = MagicMock()

    mock_db.query.return_value.filter_by().first.return_value = PokemonDBAPI(
        id=charmander["id"]
    )

    app.dependency_overrides[get_db] = lambda: mock_db
    
    client.get(f"/pokeapi/{charmander['id']}")

    app.dependency_overrides.clear()

    mock_db.add.assert_not_called()
    mock_db.commit.assert_not_called()

def test_banco_de_dados_cria_pokemon(charmander, mocker):

    mock_db = MagicMock()

    mock_db.query.return_value.filter_by().first.return_value = None

    app.dependency_overrides[get_db] = lambda: mock_db

    response = client.get(f"/pokeapi/{charmander['id']}")

    app.dependency_overrides.clear()

    mock_db.commit.assert_called_once()
    mock_db.add.assert_called_once()