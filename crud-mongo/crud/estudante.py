from db import get_db, executar

db = get_db()

def criar_estudante(mat, cpf=None, mc=None, ano_ingresso= None): # unico campo que não pode começar vazio é a matricula
    if cpf is not None and not db.usuario.find_one({"_id": cpf}):
        raise ValueError("cpf não existe em usuario")

    db.estudante.insert_one({"_id": mat, "cpf": cpf, "mc": mc, "ano_ingresso": ano_ingresso})


def buscar_estudante(mat):
    return db.estudante.find_one({"_id": mat})


def buscar_por_cpf(cpf):
    return list(db.estudante.find({"cpf": cpf}))


def listar_estudantes():
    return list(db.estudante.find().sort("_id", 1))

def atualizar_estudante(mat, **fields):
    fields = {k: v for k, v in fields.items() if v is not None}

    if not fields:
        return 0

    if "cpf" in fields and not db.usuario.find_one({"_id": fields["cpf"]}):
        raise ValueError("cpf não existe em usuario")

    return db.estudante.update_one({"_id": mat}, {"$set": fields}).modified_count


def deletar_estudante(mat):
    def op(session):
        if not db.estudante.find_one({"_id": mat}, session=session):
            return 0
        if db.plano.find_one({"mat_estudante": mat}, session=session):
            raise ValueError("estudante possui plano de trabalho, remova o plano antes")
        db.vinculo.update_many({"mat_estudante": mat}, {"$set": {"mat_estudante": None}}, session=session)
        db.turma.update_many({"matriculas.mat_estudante": mat}, {"$pull": {"matriculas": {"mat_estudante": mat}}}, session=session)
        return db.estudante.delete_one({"_id": mat}, session=session).deleted_count

    return executar(op)
