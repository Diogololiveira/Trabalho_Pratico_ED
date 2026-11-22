from db import get_connection

def criar_professor(mat_professor, cpf, departamento, formacao, data_admissao, jornada, salario):
    sql = """
        INSERT INTO universidade.professor
            (mat_professor, cpf, departamento, formacao, data_admissao, tipo_jornada_trabalho, salario)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (mat_professor, cpf, departamento, formacao, data_admissao, jornada, salario))

def listar_professores():
    sql = """
        SELECT p.mat_professor, u.nome, p.cpf, p.departamento,
               p.formacao, p.tipo_jornada_trabalho, p.salario
        FROM universidade.professor p
        LEFT JOIN universidade.usuario u ON u.cpf = p.cpf
        ORDER BY p.mat_professor;
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            return cur.fetchall()

def atualizar_professor(mat_professor, departamento=None, formacao=None, jornada=None, salario=None):
    sql = """
        UPDATE universidade.professor
        SET departamento = COALESCE(%s, departamento),
            formacao = COALESCE(%s, formacao),
            tipo_jornada_trabalho = COALESCE(%s, tipo_jornada_trabalho),
            salario = COALESCE(%s, salario)
        WHERE mat_professor = %s;
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (departamento, formacao, jornada, salario, mat_professor))
            return cur.rowcount

def deletar_professor(mat_professor):
    sql = "DELETE FROM universidade.professor WHERE mat_professor = %s;"
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (mat_professor,))
            return cur.rowcount
