""" copia os dados do postgres para o mongo """

import os
from datetime import datetime, date, time
from decimal import Decimal

import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv

from db import get_db

load_dotenv()


def conectar_pg():
    return psycopg.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        sslmode="require",
        row_factory=dict_row,
    )


def conv(v):
    if isinstance(v, datetime):
        return v
    
    if isinstance(v, date):
        return datetime.combine(v, time.min)
    
    if isinstance(v, Decimal):
        return float(v)
    
    if isinstance(v, list):
        return [conv(x) for x in v]
    
    return v


def linhas(cur, sql):
    cur.execute(sql)
    return [{k: conv(v) for k, v in r.items()} for r in cur.fetchall()]


def inserir(db, nome, docs):
    db[nome].delete_many({})

    if docs:
        db[nome].insert_many(docs)

    print(f"{nome}: {len(docs)} documento(s)")


def main():
    db = get_db()
    with conectar_pg() as pg, pg.cursor() as cur:
        inserir(db, "usuario", linhas(cur, """
            SELECT cpf::bigint AS _id, nome, data_nascimento, email, telefone, login, senha
            FROM universidade.usuario"""))

        inserir(db, "departamento", linhas(cur, """
            SELECT cod_depto AS _id, nome, chefe::text AS chefe, orcamento, comissal
            FROM universidade.departamento"""))

        inserir(db, "professor", linhas(cur, """
            SELECT mat_professor::text AS _id, cpf::bigint AS cpf, departamento,
                   formacao::text AS formacao, data_admissao,
                   tipo_jornada_trabalho::text AS tipo_jornada_trabalho, salario
            FROM universidade.professor"""))

        inserir(db, "curso", linhas(cur, """
            SELECT idcurso AS _id, nome, grau::text AS grau, turno::text AS turno,
                   campus, nivel::text AS nivel
            FROM universidade.curso"""))

        inserir(db, "estudante", linhas(cur, """
            SELECT mat_estudante::text AS _id, cpf::bigint AS cpf,
                   mc::float8 AS mc, ano_ingresso
            FROM universidade.estudante"""))

        inserir(db, "vinculo", linhas(cur, """
            SELECT idvinculo AS _id, mat_estudante::text AS mat_estudante, curso,
                   data_entrada, status::text AS status, data_saida
            FROM universidade.vinculo"""))

        inserir(db, "projeto", linhas(cur, """
            SELECT id_projeto AS _id, descricao FROM universidade.projeto"""))

        inserir(db, "plano", linhas(cur, """
            SELECT id_projeto, mat_professor::text AS mat_professor,
                   mat_estudante::text AS mat_estudante, ano
            FROM universidade.plano"""))

        inserir(db, "disciplina", linhas(cur, """
            SELECT cod_disc AS _id, nome, pre_req, creditos, depto_responsavel
            FROM universidade.disciplina"""))

        inserir(db, "semestre", linhas(cur, """
            SELECT ano, semestre, data_inicio, data_fom AS data_fim
            FROM universidade.semestre"""))

        inserir(db, "sala", linhas(cur, """
            SELECT id_sala AS _id, descricao FROM universidade.sala"""))

        inserir(db, "horario", linhas(cur, """
            SELECT id_horario AS _id, dia, slot FROM universidade.horario"""))

        # turma com leciona, alocacao e cursa
        turmas = linhas(cur, """
            SELECT id_turma AS _id, cod_disc, numero, ano, semestre
            FROM universidade.turma ORDER BY id_turma""")
        
        por_id = {t["_id"]: t for t in turmas}

        for t in turmas:
            t["professores"], t["alocacoes"], t["matriculas"] = [], [], []

        for r in linhas(cur, """SELECT id_turma, mat_professor::text AS mat_professor
                                FROM universidade.leciona"""):
            por_id[r["id_turma"]]["professores"].append(r["mat_professor"])

        for r in linhas(cur, """SELECT id_turma, id_horario, id_sala
                                FROM universidade.alocacao"""):
            por_id[r["id_turma"]]["alocacoes"].append(
                {"id_horario": r["id_horario"], "id_sala": r["id_sala"]})

        for r in linhas(cur, """SELECT id_turma, mat_estudante::text AS mat_estudante, nota
                                FROM universidade.cursa"""):
            por_id[r["id_turma"]]["matriculas"].append(
                {"mat_estudante": r["mat_estudante"], "nota": r["nota"]})

        inserir(db, "turma", turmas)

        # os contadores continuam a partir do maior id existente
        db.contadores.delete_many({})
        for nome, colecao in [("curso", "curso"), ("vinculo", "vinculo"),
                              ("sala", "sala"), ("horario", "horario"),
                              ("turma", "turma")]:
            ultimo = db[colecao].find_one(sort=[("_id", -1)])
            db.contadores.insert_one({"_id": nome, "seq": ultimo["_id"] if ultimo else 0})
        print("contadores atualizados")

    print("\nMigração concluída.")


if __name__ == "__main__":
    main()