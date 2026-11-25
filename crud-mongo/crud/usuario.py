from db import get_db, executar


def criar_usuario(cpf, nome, data_nascimento, emails, telefones, login, senha):
    doc = {
        "_id": cpf,
        "nome": nome,
        "data_nascimento": data_nascimento,
        "email": emails,
        "telefone": telefones,
        "login": login,
        "senha": senha,
    }
    get_db().usuario.insert_one(doc)


def buscar_usuario(cpf):
    return get_db().usuario.find_one({"_id": cpf})


def listar_usuarios():
    return list(get_db().usuario.find({}, {"senha": 0}).sort("nome", 1))


def atualizar_usuario(cpf, nome=None, data_nascimento=None, emails=None,
                      telefones=None, login=None, senha=None):
    campos = {
        "nome": nome,
        "data_nascimento": data_nascimento,
        "email": emails,
        "telefone": telefones,
        "login": login,
        "senha": senha,
    }
    campos = {k: v for k, v in campos.items() if v is not None}
    if not campos:
        return 0
    return get_db().usuario.update_one({"_id": cpf}, {"$set": campos}).matched_count


def deletar_usuario(cpf):
    db = get_db()

    def op(session):
        if not db.usuario.find_one({"_id": cpf}, session=session):
            return 0
        db.estudante.update_many({"cpf": cpf}, {"$set": {"cpf": None}}, session=session)
        db.professor.update_many({"cpf": cpf}, {"$set": {"cpf": None}}, session=session)
        return db.usuario.delete_one({"_id": cpf}, session=session).deleted_count

    return executar(op)