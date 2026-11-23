from db import get_db

db = get_db

def criar_estudante(mat, cpf=None, mc=None, ano_ingresso= None): # unico campo que não pode começar vazio é a matricula
    if cpf is not None and not db.usuario.find_one({"_id": cpf}):
        raise ValueError("cpf não existe em usuario")

    db.estudante.insert_one({"_id": mat, "cpf": cpf, "mc": mc, "ano_ingesso": ano_ingresso})


def listar_estudantes():
    return list(db.estudante.find().sort("_id", 1))

def atualizar_estudantes(mat, **fields):
    fields = {k: v for k, v in fields.items() if v is not None}

    if "cpf" in fields and not db.usuario.find_one({"_id": fields["cpf"]}):
        raise ValueError("cpf não existe em usuario")

    return db.estudante.update_one({"_id": mat}, {"$set": fields}).modified_count


def deletar_estudante(mat):
    db.vinculo.update_many({"mat_estudante": mat}, {"$set": {"mat_estudante": None}})
    return db.estudante.delete_one({"_id": mat}).deleted_count