import pytest
from fastapi.testclient import TestClient
from app.main import app, PokemonDB
from pytest_mock import mocker
from Tests.test_endpoint import charmander

client = TestClient(app)

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