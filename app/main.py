from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.pokeapi import router as rota_pokeapi
from routes.user_poke import router as rota_usuario

app = FastAPI()

app.add_middleware(CORSMiddleware,
                   allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],)

app.include_router(rota_pokeapi, prefix="/pokeapi")
app.include_router(rota_usuario)