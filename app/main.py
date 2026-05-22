from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import BaseModel
import pydantic
import requests

app = FastAPI()