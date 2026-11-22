from db import get_connection

def criar_turma(cod_disc, numero, ano, semestre):
    sql = """
        INSERT INTO universidade.turma (cod_disc, numero, ano, semestre)
        VALUES (%s, %s, %s, %s)
        RETURNING id_turma;
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (cod_disc, numero, ano, semestre))
            return cur.fetchone()[0]

def listar_turmas():
    sql = """
        SELECT t.id_turma, t.cod_disc, d.nome, t.numero, t.ano, t.semestre
        FROM universidade.turma t
        JOIN universidade.disciplina d ON d.cod_disc = t.cod_disc
        ORDER BY t.id_turma;
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            return cur.fetchall()

def atualizar_turma(id_turma, cod_disc=None, numero=None, ano=None, semestre=None):
    sql = """
        UPDATE universidade.turma
        SET cod_disc = COALESCE(%s, cod_disc),
            numero = COALESCE(%s, numero),
            ano = COALESCE(%s, ano),
            semestre = COALESCE(%s, semestre)
        WHERE id_turma = %s;
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (cod_disc, numero, ano, semestre, id_turma))
            return cur.rowcount

def deletar_turma(id_turma):
    sql = "DELETE FROM universidade.turma WHERE id_turma = %s;"
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (id_turma,))
            return cur.rowcount
