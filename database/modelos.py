
from sqlalchemy.orm import Mapped
from sqlalchemy import Integer, JSON, String
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase
from pydantic import BaseModel, Field, field_validator
from database.db import engine

class Base(DeclarativeBase):
    pass

#Classe do tipo Pydantic, usada para validar os dados de entrada do usuario na criação e atualização de pokemons criados pelo usuario
class Pokemon(BaseModel):
    name: str = Field(description="Nome do pokemon", examples=["Charizard"])

    @field_validator("name")
    @classmethod
    def validar_nome(cls, value):

        if not value.strip():
            raise ValueError("Nome inválido")

        return value
    
    height: float = Field(description="Altura do pokemon, deve ser um número inteiro positivo", ge=1, examples=["5.4"])
    weight: float = Field(description="Peso do pokemon, deve ser um número inteiro positivo", ge=1, examples=["200"])
    types: list[str] = Field(min_length=1, description="Lista de tipos do pokemon, deve conter pelo menos um tipo", examples=[["fogo", "dragão"]])
    level: int = Field(description="Level permitido do pokemon", ge=1, le=100, examples=["36"], default=1)

#Classe do tipo SQLAlchemy, usada para mapear a tabela de pokemons no banco de dados, e armazenar os pokemons da pokeapi.co
class PokemonDBAPI(Base):
    __tablename__ = "pokemons"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    height: Mapped[int] = mapped_column(Integer)
    weight: Mapped[int] = mapped_column(Integer)
    types: Mapped[list[str]] = mapped_column(JSON)
    level: Mapped[int] = mapped_column(Integer)
    sprites: Mapped[dict[str, str]] = mapped_column(JSON)

#Classe do tipo SQLAlchemy, usada para mapear a tabela de pokemons no banco de dados, e armazenar os pokemons criados pelo usuario
class PokemonDB(Base):
    __tablename__ = "pokemons_user"
    name: Mapped[str] = mapped_column(String(30), primary_key=True)
    height: Mapped[int] = mapped_column(Integer)
    weight: Mapped[int] = mapped_column(Integer)
    types: Mapped[list[str]] = mapped_column(JSON)
    level: Mapped[int] = mapped_column(Integer)

#Criando as tabelas no banco de dados, caso elas ainda não existam
Base.metadata.create_all(bind=engine)