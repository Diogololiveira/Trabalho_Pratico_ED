from db import get_db
from pymongo import ASCENDING

db = get_db()
NUM = ["int", "long"]

def criar(nome, schema):
    if nome in db.list_collection_names():
        db.drop_collections(name)

    db.create_collection(nome, validator={"$jsonSchema": schema}, validationAction="error")


criar("usuario", {
    "bsonType": object,
    "required": ["_id", "nome"],
    properties: {
        "_id": {"bsonType": NUM},    # cpf mas podderia se string,  mas to seguindo o formato do schema das aulas
        "nome": {"bsonType": string, "maxLength": 100},
        "data_nascimento": {"bsonType": ["date", "null"]},
        "email": {"bsonType": ["array", "null"], "items": {"bsonType": "string"}},
        "telefone": {"bsonType": ["array", "null"], "items": {"bsonType": "string"}},
        "login": {"bsonType": ["string", "null"], "maxLength": 50},
        "senha": {"bsonType": ["string", "null"], "maxLength": 20}, 

    },
})

db.usuario.create_index("login", unique=True, partialFilterExpression={"login": {"$type": "string"}})

criar("curso", {
    "bsonType": "object",
    "required": ["_id", "nome", "turno"],
    "properties": {
        "_id": {"bsonType": NUM},                       # idCurso
        "nome": {"bsonType": "string", "maxLength": 100},
        "grau": {"enum": ["Bacharelado", "Licenciatura Plena", None]},
        "turno": {"enum": ["Matutino", "Vespertino", "Noturno", "Turno Indefinido"]},
        "campus": {"bsonType": ["string", "null"]},
        "nivel": {"enum": ["Graduação", "Mestrado", "Doutorado", "Lato", None]},
    },
})
db.curso.create_index([("nome", 1), ("turno", 1), ("campus", 1), ("nivel", 1)], unique=True)

criar("estudante", {
    "bsonType": "object",
    "required": ["_id"],
    "properties": {
        "_id": {"bsonType": "string", "maxLength": 7},   # mat_estudante
        "cpf": {"bsonType": NUM + ["null"]},
        "mc": {"bsonType": ["double", "int", "null"]},
        "ano_ingresso": {"bsonType": ["int", "null"]},
    },
})
db.estudante.create_index("cpf", unique=True,
    partialFilterExpression={"cpf": {"$type": "number"}})

criar("vinculo", {
    "bsonType": "object",
    "required": ["_id"],
    "properties": {
        "_id": {"bsonType": NUM},                        # idVinculo
        "mat_estudante": {"bsonType": ["string", "null"]},
        "curso": {"bsonType": NUM + ["null"]},
        "data_entrada": {"bsonType": ["date", "null"]},
        "status": {"enum": ["Ativo", "Cancelada", "Formando", "Graduado", None]},
        "data_saida": {"bsonType": ["date", "null"]},
    },
})
print("Schema criado com sucesso")