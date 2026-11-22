from db import get_connection

def criar_usuario(cpf, nome, data_nascimento, emails, telefones, login, senha):
    sql = """
        INSERT INTO universidade.usuario
            (cpf, nome, data_nascimento, email, telefone, login, senha)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (cpf, nome, data_nascimento, emails, telefones, login, senha))

def listar_usuarios():
    sql = """
        SELECT cpf, nome, data_nascimento, email, telefone, login
        FROM universidade.usuario
        ORDER BY nome;
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            return cur.fetchall()

def atualizar_usuario(cpf, nome=None, data_nascimento=None, emails=None, telefones=None, login=None, senha=None):
    sql = """
        UPDATE universidade.usuario
        SET nome = COALESCE(%s, nome),
            data_nascimento = COALESCE(%s, data_nascimento),
            email = COALESCE(%s, email),
            telefone = COALESCE(%s, telefone),
            login = COALESCE(%s, login),
            senha = COALESCE(%s, senha)
        WHERE cpf = %s;
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (nome, data_nascimento, emails, telefones, login, senha, cpf))
            return cur.rowcount

def deletar_usuario(cpf):
    sql = "DELETE FROM universidade.usuario WHERE cpf = %s;"
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (cpf,))
            return cur.rowcount
