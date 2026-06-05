import pytest
from fastapi.testclient import TestClient
from app.main import app, PokemonDBAPI, get_db
from unittest.mock import MagicMock
from pytest_mock import mocker
from Tests.test_endpoint import charmander

client = TestClient(app)

def test_banco_de_dados_verifica_chamada(charmander, mocker):

    mock_db = mocker.patch("app.main.get_db")

    response = client.get(f"/pokemons/{charmander['id']}")

    mock_db.query.assert_called_with(PokemonDBAPI)

    mock_db.query().filter_by.assert_called_with(
        id=charmander["id"]
        )

def test_banco_de_dados_verifica_pokemon_existente(charmander, mocker):

    mock_db = mocker.patch("app.main.Db")

    mock_db.query.return_value.filter_by().first.return_value = PokemonDBAPI(
        id=charmander["id"]
    )

    client.get(f"/pokemons/{charmander['id']}")

    mock_db.add.assert_not_called()
    mock_db.commit.assert_not_called()

def test_banco_de_dados_cria_pokemon(charmander, mocker):

    mock_db = mocker.patch("app.main.Db")
    mock_db.query.return_value.filter_by().first.return_value = None

    response = client.get(f"/pokemons/{charmander['id']}")

    mock_db.commit.assert_called_once()
    mock_db.add.assert_called_once()