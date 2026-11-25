import os
from dotenv import load_dotenv
from pymongo import MongoClient, ReturnDocument
from pymongo.errors import OperationFailure

load_dotenv()

_client = None


def get_client():
    global _client
    if _client is None:
        uri = os.getenv("MONGO_URI")
        if not uri:
            raise RuntimeError("MONGO_URI não definido no .env")
        _client = MongoClient(uri, serverSelectionTimeoutMS=8000)
    return _client


def get_db():
    return get_client()[os.getenv("MONGO_DB", "universidade")]


def proximo_id(nome, session=None):
    """ substitui o SERIAL do postgre por contador atomico por coleção"""
    doc = get_db().contadores.find_one_and_update(
        {"_id": nome},
        {"$inc": {"seq": 1}},
        upsert=True,
        return_document=ReturnDocument.AFTER,
        session=session,
    )
    return doc["seq"]


def executar(op):
    with get_client().start_session() as sessao:
        try:
            return sessao.with_transaction(op)
        except OperationFailure as e:
            if e.code == 20 or "replica set" in str(e):
                return op(None)
            raise
