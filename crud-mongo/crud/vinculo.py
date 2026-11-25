from db import get_db, proximo_id


def _validar_referencias(db, mat_estudante, curso):
    if mat_estudante is not None and not db.estudante.find_one({"_id": mat_estudante}):
        raise ValueError("Matrícula não existe em estudante (integridade referencial).")
    
    if curso is not None and not db.curso.find_one({"_id": curso}):
        raise ValueError("Curso não existe (integridade referencial).")


def criar_vinculo(mat_estudante, curso, data_entrada, status, data_saida):
    db = get_db()
    
    _validar_referencias(db, mat_estudante, curso)
    
    id_vinculo = proximo_id("vinculo")
    
    db.vinculo.insert_one({
        "_id": id_vinculo,
        "mat_estudante": mat_estudante,
        "curso": curso,
        "data_entrada": data_entrada,
        "status": status,
        "data_saida": data_saida,
    })
    
    return id_vinculo


def buscar_vinculo(id_vinculo):
    return get_db().vinculo.find_one({"_id": id_vinculo})


def vinculos_do_estudante(mat_estudante):
    return list(get_db().vinculo.find({"mat_estudante": mat_estudante}))


def vinculos_do_curso(id_curso):
    return list(get_db().vinculo.find({"curso": id_curso}))


def listar_vinculos():
    return list(get_db().vinculo.aggregate([
        {"$lookup": {"from": "curso", "localField": "curso",
                     "foreignField": "_id", "as": "c"}},
        {"$addFields": {"nome_curso": {"$arrayElemAt": ["$c.nome", 0]}}},
        {"$project": {"c": 0}},
        {"$sort": {"_id": 1}},
    ]))


def atualizar_vinculo(id_vinculo, mat_estudante=None, curso=None,
                      data_entrada=None, status=None, data_saida=None):
    db = get_db()
    
    fields = {
        "mat_estudante": mat_estudante,
        "curso": curso,
        "data_entrada": data_entrada,
        "status": status,
        "data_saida": data_saida,
    }
    
    fields = {k: v for k, v in fields.items() if v is not None}
    
    if not fields:
        return 0
    
    _validar_referencias(db, fields.get("mat_estudante"), fields.get("curso"))
    return db.vinculo.update_one({"_id": id_vinculo}, {"$set": fields}).matched_count


def deletar_vinculo(id_vinculo):
    return get_db().vinculo.delete_one({"_id": id_vinculo}).deleted_count