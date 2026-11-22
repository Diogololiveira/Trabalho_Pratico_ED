import psycopg
from crud import usuario, professor, turma, leciona

def ler_lista(msg):
    texto = input(msg).strip()
    if not texto:
        return None
    return [item.strip() for item in texto.split(",")]

def ler_opcional(msg):
    texto = input(msg).strip()
    return texto if texto else None

def menu_usuario():
    print("\n--- USUÁRIO ---")
    print("1. Criar | 2. Listar | 3. Atualizar | 4. Deletar")
    op = input("Opção: ")
    if op == "1":
        cpf = int(input("CPF (somente números): "))
        nome = input("Nome: ")
        nasc = ler_opcional("Data nascimento (AAAA-MM-DD, enter p/ vazio): ")
        emails = ler_lista("Emails separados por vírgula (enter p/ vazio): ")
        tels = ler_lista("Telefones separados por vírgula (enter p/ vazio): ")
        login = ler_opcional("Login: ")
        senha = ler_opcional("Senha: ")
        usuario.criar_usuario(cpf, nome, nasc, emails, tels, login, senha)
        print("Usuário criado.")
    elif op == "2":
        for row in usuario.listar_usuarios():
            print(row)
    elif op == "3":
        cpf = int(input("CPF do usuário a atualizar: "))
        print("O que deseja atualizar?")
        print("1. Nome | 2. Data nascimento | 3. Emails | 4. Telefones | 5. Login | 6. Senha")
        campo = input("Campo: ")
        if campo == "1":
            rows = usuario.atualizar_usuario(cpf, nome=input("Novo nome: "))
        elif campo == "2":
            rows = usuario.atualizar_usuario(cpf, data_nascimento=input("Nova data nascimento (AAAA-MM-DD): "))
        elif campo == "3":
            rows = usuario.atualizar_usuario(cpf, emails=ler_lista("Novos emails (separados por vírgula): "))
        elif campo == "4":
            rows = usuario.atualizar_usuario(cpf, telefones=ler_lista("Novos telefones (separados por vírgula): "))
        elif campo == "5":
            rows = usuario.atualizar_usuario(cpf, login=input("Novo login: "))
        elif campo == "6":
            rows = usuario.atualizar_usuario(cpf, senha=input("Nova senha: "))
        else:
            print("Campo inválido.")
            return
        print(f"Atualizados: {rows}")
    elif op == "4":
        cpf = int(input("CPF do usuário a deletar: "))
        print(f"Removidos: {usuario.deletar_usuario(cpf)}")

def menu_professor():
    print("\n--- PROFESSOR ---")
    print("1. Criar | 2. Listar | 3. Atualizar | 4. Deletar")
    op = input("Opção: ")
    if op == "1":
        mat = input("Matrícula (ex: P1600): ")
        cpf = int(input("CPF (já cadastrado em usuario): "))
        depto = ler_opcional("Departamento (ex: DCOMP, DMA, DFI, DECAT, DEL): ")
        formacao = ler_opcional("Formação (Graduação/Especialização/Mestrado/Doutorado): ")
        admissao = ler_opcional("Data admissão (AAAA-MM-DD, enter p/ vazio): ")
        jornada = ler_opcional("Jornada (20h/40h/DE): ")
        sal_str = ler_opcional("Salário: ")
        salario = float(sal_str) if sal_str else None
        professor.criar_professor(mat, cpf, depto, formacao, admissao, jornada, salario)
        print("Professor criado.")
    elif op == "2":
        for row in professor.listar_professores():
            print(row)
    elif op == "3":
        mat = input("Matrícula do professor: ")
        print("O que deseja atualizar?")
        print("1. Departamento | 2. Formação | 3. Jornada | 4. Salário")
        campo = input("Campo: ")
        if campo == "1":
            rows = professor.atualizar_professor(mat, departamento=input("Novo departamento: "))
        elif campo == "2":
            rows = professor.atualizar_professor(mat, formacao=input("Nova formação (Graduação/Especialização/Mestrado/Doutorado): "))
        elif campo == "3":
            rows = professor.atualizar_professor(mat, jornada=input("Nova jornada (20h/40h/DE): "))
        elif campo == "4":
            rows = professor.atualizar_professor(mat, salario=float(input("Novo salário: ")))
        else:
            print("Campo inválido.")
            return
        print(f"Atualizados: {rows}")
    elif op == "4":
        mat = input("Matrícula do professor a deletar: ")
        print(f"Removidos: {professor.deletar_professor(mat)}")

def menu_turma():
    print("\n--- TURMA ---")
    print("1. Criar | 2. Listar | 3. Atualizar | 4. Deletar")
    op = input("Opção: ")
    if op == "1":
        cod_disc = input("Código da disciplina (ex: COMP0311): ")
        numero = int(input("Número da turma: "))
        ano = int(input("Ano (ex: 2017 ou 2019): "))
        sem = int(input("Semestre (ex: 1 ou 2): "))
        tid = turma.criar_turma(cod_disc, numero, ano, sem)
        print(f"Turma criada com ID {tid}.")
    elif op == "2":
        for row in turma.listar_turmas():
            print(row)
    elif op == "3":
        tid = int(input("ID da turma: "))
        print("O que deseja atualizar?")
        print("1. Disciplina | 2. Número | 3. Ano | 4. Semestre")
        campo = input("Campo: ")
        if campo == "1":
            rows = turma.atualizar_turma(tid, cod_disc=input("Novo código da disciplina: "))
        elif campo == "2":
            rows = turma.atualizar_turma(tid, numero=int(input("Novo número da turma: ")))
        elif campo == "3":
            rows = turma.atualizar_turma(tid, ano=int(input("Novo ano: ")))
        elif campo == "4":
            rows = turma.atualizar_turma(tid, semestre=int(input("Novo semestre: ")))
        else:
            print("Campo inválido.")
            return
        print(f"Atualizados: {rows}")
    elif op == "4":
        tid = int(input("ID da turma a deletar: "))
        print(f"Removidos: {turma.deletar_turma(tid)}")

def menu_leciona():
    print("\n--- LECIONA ---")
    print("1. Vincular | 2. Listar | 3. Atualizar | 4. Deletar")
    op = input("Opção: ")
    if op == "1":
        tid = int(input("ID da turma: "))
        mat = input("Matrícula do professor (ex: P100): ")
        leciona.criar_leciona(tid, mat)
        print("Vínculo criado.")
    elif op == "2":
        for row in leciona.listar_leciona():
            print(row)
    elif op == "3":
        tid_atual = int(input("ID da turma atual: "))
        mat_atual = input("Matrícula do professor atual: ")
        print("O que deseja atualizar?")
        print("1. Turma | 2. Professor")
        campo = input("Campo: ")
        if campo == "1":
            rows = leciona.atualizar_leciona(tid_atual, mat_atual, nova_id_turma=int(input("Novo ID da turma: ")))
        elif campo == "2":
            rows = leciona.atualizar_leciona(tid_atual, mat_atual, nova_mat_professor=input("Nova matrícula do professor: "))
        else:
            print("Campo inválido.")
            return
        print(f"Atualizados: {rows}")
    elif op == "4":
        tid = int(input("ID da turma: "))
        mat = input("Matrícula do professor: ")
        print(f"Removidos: {leciona.deletar_leciona(tid, mat)}")

def main():
    while True:
        print("\n=== CRUD UNIVERSIDADE (AWS PostgreSQL) ===")
        print("1. Usuário\n2. Professor\n3. Turma\n4. Leciona\n0. Sair")
        escolha = input("Escolha uma tabela: ")
        try:
            if escolha == "1":
                menu_usuario()
            elif escolha == "2":
                menu_professor()
            elif escolha == "3":
                menu_turma()
            elif escolha == "4":
                menu_leciona()
            elif escolha == "0":
                break
            else:
                print("Opção inválida.")
        except psycopg.Error as e:
            print(f"Erro no banco: {e.diag.message_primary or e}")
        except ValueError:
            print("Erro: valor numérico inválido.")

if __name__ == "__main__":
    main()
