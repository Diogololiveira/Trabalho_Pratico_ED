from db import get_db

db = get_db()


def texto(max_len=None, nulo=True):
    s = {"bsonType": ["string", "null"] if nulo else "string"}
    if max_len:
        s["maxLength"] = max_len
    return s


def inteiro(nulo=True, minimo=None, maximo=None):
    s = {"bsonType": ["int", "long", "null"] if nulo else ["int", "long"]}
    if minimo is not None:
        s["minimum"] = minimo
    if maximo is not None:
        s["maximum"] = maximo
    return s


def numero(nulo=True):
    return {"bsonType": ["number", "null"] if nulo else "number"}


def data(nulo=True):
    return {"bsonType": ["date", "null"] if nulo else "date"}


def opcoes(valores, nulo=True):
    return {"enum": valores + [None] if nulo else valores}


def objeto(props, required=()):
    schema = {
        "bsonType": "object",
        "additionalProperties": False,
        "properties": {"_id": {}, **props},
    }
    if required:
        schema["required"] = list(required)
    return schema


def criar(nome, schema):
    if nome in db.list_collection_names():
        db.drop_collection(nome)
    db.create_collection(nome, validator={"$jsonSchema": schema}, validationAction="error")
    print(f"coleção '{nome}' criada")


def so_se_string(*campos):
    return {"$and": [{c: {"$type": "string"}} for c in campos]}


MATRICULA = dict(max_len=7)

criar("usuario", objeto({
    "_id": inteiro(nulo=False),                      # cpf
    "nome": texto(100, nulo=False),
    "data_nascimento": data(),
    "email": {"bsonType": ["array", "null"], "items": {"bsonType": "string"}},
    "telefone": {"bsonType": ["array", "null"], "items": {"bsonType": "string"}},
    "login": texto(45),
    "senha": texto(32),
}, required=["nome"]))

db.usuario.create_index("login", unique=True, name="uq_login",
                        partialFilterExpression={"login": {"$type": "string"}})

criar("departamento", objeto({
    "_id": texto(5, nulo=False),                     # cod_depto
    "nome": texto(50, nulo=False),
    "chefe": texto(7),                               # professor._id
    "orcamento": {"bsonType": ["number", "null"], "minimum": 0, "exclusiveMinimum": True},
    "comissal": numero(),
}, required=["nome"]))

criar("professor", objeto({
    "_id": texto(7, nulo=False),                     # mat_professor
    "cpf": inteiro(),                                # usuario._id
    "departamento": texto(5),                        # departamento._id
    "formacao": opcoes(["Graduação", "Especialização", "Mestrado", "Doutorado"]),
    "data_admissao": data(),
    "tipo_jornada_trabalho": opcoes(["20h", "40h", "DE"]),
    "salario": numero(),
}))
db.professor.create_index("cpf", unique=True, name="uq_professor_cpf",
                          partialFilterExpression={"cpf": {"$type": "number"}})

criar("curso", objeto({
    "_id": inteiro(nulo=False),                      # idCurso
    "nome": texto(100, nulo=False),
    "grau": opcoes(["Bacharelado", "Licenciatura Plena"]),
    "turno": opcoes(["Matutino", "Vespertino", "Noturno", "Turno Indefinido"], nulo=False),
    "campus": texto(100),
    "nivel": opcoes(["Graduação", "Mestrado", "Doutorado", "Lato"]),
}, required=["nome", "turno"]))

db.curso.create_index([("nome", 1), ("turno", 1), ("campus", 1), ("nivel", 1)],
                      unique=True, name="uq_curso",
                      partialFilterExpression=so_se_string("campus", "nivel"))

criar("estudante", objeto({
    "_id": texto(7, nulo=False),                     # mat_estudante
    "cpf": inteiro(),                                # usuario._id
    "mc": numero(),
    "ano_ingresso": inteiro(),
}))
db.estudante.create_index("cpf", unique=True, name="uq_estudante_cpf",
                          partialFilterExpression={"cpf": {"$type": "number"}})

criar("vinculo", objeto({
    "_id": inteiro(nulo=False),                      # idVinculo
    "mat_estudante": texto(7),                       # estudante._id
    "curso": inteiro(),                              # curso._id
    "data_entrada": data(),
    "status": opcoes(["Ativo", "Cancelada", "Formando", "Graduado"]),
    "data_saida": data(),
}))

criar("projeto", objeto({
    "_id": inteiro(nulo=False),                      # id_projeto
    "descricao": texto(),
}))

criar("plano", objeto({
    "id_projeto": inteiro(),                         #  projeto._id
    "mat_professor": texto(7),                       #  professor._id
    "mat_estudante": texto(7, nulo=False),           #  estudante._id
    "ano": inteiro(nulo=False),
}, required=["mat_estudante", "ano"]))

db.plano.create_index([("mat_estudante", 1), ("ano", 1)], unique=True, name="pk_plano")

criar("disciplina", objeto({
    "_id": texto(8, nulo=False),                     # cod_disc
    "nome": texto(40, nulo=False),
    "pre_req": texto(8),                             # disciplina._id
    "creditos": inteiro(minimo=1, maximo=11),        # checagem se 1 <= creditos < 12
    "depto_responsavel": texto(5),                   # departamento._id
}, required=["nome"]))

criar("semestre", objeto({
    "ano": inteiro(nulo=False),
    "semestre": inteiro(nulo=False),
    "data_inicio": data(),
    "data_fim": data(),                              # data_fom no SQL
}, required=["ano", "semestre"]))
db.semestre.create_index([("ano", 1), ("semestre", 1)], unique=True, name="pk_semestre")


criar("sala", objeto({
    "_id": inteiro(nulo=False),                      # id_sala
    "descricao": texto(),
}))

criar("horario", objeto({
    "_id": inteiro(nulo=False),                      # id_horario
    "dia": texto(15, nulo=False),
    "slot": inteiro(nulo=False),
}, required=["dia", "slot"]))

criar("turma", objeto({
    "_id": inteiro(nulo=False),                      # id_turma
    "cod_disc": texto(8, nulo=False),                # disciplina._id
    "numero": inteiro(),
    "ano": inteiro(),                                # semestre (ano, semestre)
    "semestre": inteiro(),
    "professores": {                                 # leciona
        "bsonType": "array", "uniqueItems": True,
        "items": {"bsonType": "string", "maxLength": 7},
    },
    "alocacoes": {                                   # alocacao
        "bsonType": "array",
        "items": {
            "bsonType": "object", "required": ["id_horario"],
            "additionalProperties": False,
            "properties": {"id_horario": inteiro(nulo=False), "id_sala": inteiro()},
        },
    },
    "matriculas": {                                  # cursa
        "bsonType": "array",
        "items": {
            "bsonType": "object", "required": ["mat_estudante"],
            "additionalProperties": False,
            "properties": {"mat_estudante": texto(7, nulo=False), "nota": numero()},
        },
    },
}, required=["cod_disc"]))

db.turma.create_index([("cod_disc", 1), ("numero", 1), ("semestre", 1), ("ano", 1)],
                      unique=True, name="uq_turma")

db.turma.create_index([("alocacoes.id_horario", 1), ("alocacoes.id_sala", 1)],
                      unique=True, name="uq_alocacao",
                      partialFilterExpression={"alocacoes.0": {"$exists": True}})

if "contadores" in db.list_collection_names():
    db.drop_collection("contadores")

db.create_collection("contadores")
print("coleção 'contadores' criada")

print("\nSchema pronto.")