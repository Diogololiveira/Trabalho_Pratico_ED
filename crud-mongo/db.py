import os
from pymongo import MongoCliente
from dotenv import load_env

load_env()
_client = MongoCliente(os.getenv("MONGO_URI"))

def get_db():
    return _clien[os.getenv("MONGO_DB", "universidade")]