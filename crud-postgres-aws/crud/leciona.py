from db import get_connection

def criar_leciona(id_turma, mat_professor):
    sql = "INSERT INTO universidade.leciona (id_turma, mat_professor) VALUES (%s, %s);"
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (id_turma, mat_professor))

def listar_leciona():
    sql = """
        SELECT l.id_turma, t.cod_disc, l.mat_professor, u.nome
        FROM universidade.leciona l
        JOIN universidade.turma t ON t.id_turma = l.id_turma
        JOIN universidade.professor p ON p.mat_professor = l.mat_professor
        LEFT JOIN universidade.usuario u ON u.cpf = p.cpf
        ORDER BY l.id_turma, l.mat_professor;
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            return cur.fetchall()

def atualizar_leciona(id_turma_atual, mat_professor_atual, nova_id_turma=None, nova_mat_professor=None):
    sql = """
        UPDATE universidade.leciona
        SET id_turma = COALESCE(%s, id_turma),
            mat_professor = COALESCE(%s, mat_professor)
        WHERE id_turma = %s AND mat_professor = %s;
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (nova_id_turma, nova_mat_professor, id_turma_atual, mat_professor_atual))
            return cur.rowcount

def deletar_leciona(id_turma, mat_professor):
    sql = "DELETE FROM universidade.leciona WHERE id_turma = %s AND mat_professor = %s;"
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (id_turma, mat_professor))
            return cur.rowcount
