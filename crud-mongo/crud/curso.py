from db import get_db, executar, proximo_id


def criar_curso(nome, grau, turno, campus, nivel):
    id_curso = proximo_id("curso")
    
    get_db().curso.insert_one({
        "_id": id_curso,
        "nome": nome,
        "grau": grau,
        "turno": turno,
        "campus": campus,
        "nivel": nivel,
    })
    return id_curso


def buscar_curso(id_curso):
    return get_db().curso.find_one({"_id": id_curso})


def listar_cursos():
    return list(get_db().curso.find().sort("_id", 1))


def atualizar_curso(id_curso, nome=None, grau=None, turno=None, campus=None, nivel=None):
    fields = {"nome": nome, "grau": grau, "turno": turno, "campus": campus, "nivel": nivel}
    fields = {k: v for k, v in fields.items() if v is not None}
    
    if not fields:
        return 0
    
    return get_db().curso.update_one({"_id": id_curso}, {"$set": fields}).matched_count


def deletar_curso(id_curso):
    db = get_db()

    def op(session):
        if not db.curso.find_one({"_id": id_curso}, session=session):
            return 0
        
        db.vinculo.update_many({"curso": id_curso}, {"$set": {"curso": None}}, session=session)
        
        return db.curso.delete_one({"_id": id_curso}, session=session).deleted_count

    return executar(op)