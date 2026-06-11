from fastapi import FastAPI, Depends, HTTPException
from routes.pokeapi import router as rota_pokeapi
from routes.user_poke import router as rota_usuario
from database.modelos import PokemonDB, Pokemon
from database.db import get_db

app = FastAPI()

app.include_router(rota_pokeapi)
app.include_router(rota_usuario)