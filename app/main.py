from fastapi import FastAPI
from routes.pokeapi import router as rota_pokeapi
from routes.user_poke import router as rota_usuario

app = FastAPI()

app.include_router(rota_pokeapi, prefix="/pokeapi")
app.include_router(rota_usuario)