from pymongo.errors import DuplicateKeyError, WriteError, PyMongoError

from crud import usuario, estudante, curso, vinculo
from util import parse_data, mostrar

GRAUS = "Bacharelado / Licenciatura Plena"
TURNOS = "Matutino / Vespertino / Noturno / Turno Indefinido"
NIVEIS = "Graduação / Mestrado / Doutorado / Lato"
STATUS = "Ativo / Cancelada / Formando / Graduado"


def ler_opcional(msg):
    texto = input(msg).strip()
    return texto if texto else None


def ler_lista(msg):
    texto = input(msg).strip()
    if not texto:
        return None
    return [item.strip() for item in texto.split(",")]


def ler_int_opcional(msg):
    texto = input(msg).strip()
    return int(texto) if texto else None


def ler_float_opcional(msg):
    texto = input(msg).strip().replace(",", "")
    return float(texto) if texto else None

def menu_usuario():
    print("\n--- USUÁRIO ---")
    print("1. Criar | 2. Listar | 3. Atualizar | 4. Deletar")
    op = input("Opção: ")

    if op == "1":
        cpf = int(input("CPF (somente números): "))
        nome = input("Nome: ")
        nasc = parse_data(ler_opcional("Data nascimento (AAAA-MM-DD, enter para vazio): "))
        emails = ler_lista("Emails separados por vírgula (enter para vazio): ")
        tels = ler_lista("Telefones separados por vírgula (enter para vazio): ")
        login = ler_opcional("Login: ")
        senha = ler_opcional("Senha: ")
        mostrar("ANTES", usuario.buscar_usuario(cpf))
        usuario.criar_usuario(cpf, nome, nasc, emails, tels, login, senha)
        
        print("Usuário criado")
        mostrar("DEPOIS", usuario.buscar_usuario(cpf))

    elif op == "2":
        mostrar("USUÁRIOS", usuario.listar_usuarios())
    elif op == "3":
        cpf = int(input("CPF do usuário a atualizar: "))
        print("1. Nome | 2. Data nascimento | 3. Emails | 4. Telefones | 5. Login | 6. Senha")
        
        campo = input("Campo: ")
        mostrar("ANTES", usuario.buscar_usuario(cpf))
        
        if campo == "1":
            rows = usuario.atualizar_usuario(cpf, nome=input("Novo nome: "))
        elif campo == "2":
            rows = usuario.atualizar_usuario(
                cpf, data_nascimento=parse_data(input("Nova data nascimento (AAAA-MM-DD): ")))
        elif campo == "3":
            rows = usuario.atualizar_usuario(cpf, emails=ler_lista("Novos emails (separados por vírgula): "))
        elif campo == "4":
            rows = usuario.atualizar_usuario(cpf, telefones=ler_lista("Novos telefones (separados por vírgula): "))
        elif campo == "5":
            rows = usuario.atualizar_usuario(cpf, login=input("Novo login: "))
        elif campo == "6":
            rows = usuario.atualizar_usuario(cpf, senha=input("Nova senha: "))
        else:
            print("Campo inválido")
            return
        
        print(f"Atualizados: {rows}")
        mostrar("DEPOIS", usuario.buscar_usuario(cpf))
    
    elif op == "4":
        cpf = int(input("CPF do usuário a deletar: "))
        mostrar("USUÁRIO ANTES", usuario.buscar_usuario(cpf))
        ligados = estudante.buscar_por_cpf(cpf)
        mostrar("ESTUDANTE(S) LIGADO(S) ANTES", ligados)
        print(f"Removidos: {usuario.deletar_usuario(cpf)}")
        mostrar("USUÁRIO DEPOIS", usuario.buscar_usuario(cpf))
        mostrar("ESTUDANTE(S) LIGADO(S) DEPOIS (cpf -> null)",
                [estudante.buscar_estudante(e["_id"]) for e in ligados])
    else:
        print("Opção inválida")


def menu_estudante():
    print("\n--- ESTUDANTE ---")
    print("1. Criar | 2. Listar | 3. Atualizar | 4. Deletar")
    op = input("Opção: ")
    
    if op == "1":
        mat = input("Matrícula (ex: E101): ")
        cpf = ler_int_opcional("CPF (já cadastrado em usuario, enter para vazio): ")
        mc = ler_float_opcional("MC (enter para vazio): ")
        ano = ler_int_opcional("Ano de ingresso (enter para vazio): ")
        mostrar("ANTES", estudante.buscar_estudante(mat))
        estudante.criar_estudante(mat, cpf, mc, ano)
        print("Estudante criado")
        mostrar("DEPOIS", estudante.buscar_estudante(mat))
    elif op == "2":
        mostrar("ESTUDANTES", estudante.listar_estudantes())
    
    elif op == "3":
        mat = input("Matrícula do estudante: ")
        print("1. CPF | 2. MC | 3. Ano de ingresso")
        campo = input("Campo: ")
        mostrar("ANTES", estudante.buscar_estudante(mat))
        if campo == "1":
            rows = estudante.atualizar_estudante(mat, cpf=int(input("Novo CPF: ")))
        elif campo == "2":
            rows = estudante.atualizar_estudante(mat, mc=float(input("Novo MC: ").replace(",", "")))
        elif campo == "3":
            rows = estudante.atualizar_estudante(mat, ano_ingresso=int(input("Novo ano de ingresso: ")))
        else:
            print("Campo inválido")
            return
        
        print(f"Atualizados: {rows}")
        mostrar("DEPOIS", estudante.buscar_estudante(mat))
    
    elif op == "4":
        mat = input("Matrícula do estudante a deletar: ")
        mostrar("ESTUDANTE ANTES", estudante.buscar_estudante(mat))
        ligados = vinculo.vinculos_do_estudante(mat)
        mostrar("VÍNCULOS ANTES", ligados)
        print(f"Removidos: {estudante.deletar_estudante(mat)}")
        mostrar("ESTUDANTE DEPOIS", estudante.buscar_estudante(mat))
        mostrar("VÍNCULOS DEPOIS (mat_estudante -> null)",
                [vinculo.buscar_vinculo(v["_id"]) for v in ligados])
    else:
        print("Opção inválida")


def menu_curso():
    print("\n--- CURSO ---")
    print("1. Criar | 2. Listar | 3. Atualizar | 4. Deletar")
    op = input("Opção: ")

    if op == "1":
        nome = input("Nome: ")
        grau = ler_opcional(f"Grau ({GRAUS}, enter para vazio): ")
        turno = input(f"Turno ({TURNOS}): ")
        campus = ler_opcional("Campus (enter para vazio): ")
        nivel = ler_opcional(f"Nível ({NIVEIS}, enter para vazio): ")
        id_curso = curso.criar_curso(nome, grau, turno, campus, nivel)
        print(f"Curso criado com ID {id_curso}")
        mostrar("DEPOIS", curso.buscar_curso(id_curso))

    elif op == "2":
        mostrar("CURSOS", curso.listar_cursos())

    elif op == "3":
        id_curso = int(input("ID do curso: "))
        print("1. Nome | 2. Grau | 3. Turno | 4. Campus | 5. Nível")
        campo = input("Campo: ")
        mostrar("ANTES", curso.buscar_curso(id_curso))
        
        if campo == "1":
            rows = curso.atualizar_curso(id_curso, nome=input("Novo nome: "))
        elif campo == "2":
            rows = curso.atualizar_curso(id_curso, grau=input(f"Novo grau ({GRAUS}): "))
        elif campo == "3":
            rows = curso.atualizar_curso(id_curso, turno=input(f"Novo turno ({TURNOS}): "))
        elif campo == "4":
            rows = curso.atualizar_curso(id_curso, campus=input("Novo campus: "))
        elif campo == "5":
            rows = curso.atualizar_curso(id_curso, nivel=input(f"Novo nível ({NIVEIS}): "))
        else:
            print("Campo inválido")
            return
        
        print(f"Atualizados: {rows}")
        mostrar("DEPOIS", curso.buscar_curso(id_curso))

    elif op == "4":
        id_curso = int(input("ID do curso a deletar: "))
        mostrar("CURSO ANTES", curso.buscar_curso(id_curso))
        ligados = vinculo.vinculos_do_curso(id_curso)
        mostrar("VÍNCULOS ANTES", ligados)
        print(f"Removidos: {curso.deletar_curso(id_curso)}")
        mostrar("CURSO DEPOIS", curso.buscar_curso(id_curso))
        mostrar("VÍNCULOS DEPOIS (curso -> null)",
                [vinculo.buscar_vinculo(v["_id"]) for v in ligados])
    else:
        print("Opção inválida")


def menu_vinculo():
    print("\n--- VÍNCULO ---")
    print("1. Criar | 2. Listar | 3. Atualizar | 4. Deletar")
    op = input("Opção: ")
    if op == "1":
        mat = ler_opcional("Matrícula do estudante (enter para vazio): ")
        id_curso = ler_int_opcional("ID do curso (enter para vazio): ")
        entrada = parse_data(ler_opcional("Data entrada (AAAA-MM-DD, enter para vazio): "))
        status = ler_opcional(f"Status ({STATUS}, enter para vazio): ")
        saida = parse_data(ler_opcional("Data saída (AAAA-MM-DD, enter para vazio): "))
        id_v = vinculo.criar_vinculo(mat, id_curso, entrada, status, saida)
        print(f"Vínculo criado com ID {id_v}")
        mostrar("DEPOIS", vinculo.buscar_vinculo(id_v))

    elif op == "2":
        mostrar("VÍNCULOS", vinculo.listar_vinculos())
    elif op == "3":
        id_v = int(input("ID do vínculo: "))
        
        print("1. Estudante | 2. Curso | 3. Data entrada | 4. Status | 5. Data saída")
        
        campo = input("Campo: ")
        mostrar("ANTES", vinculo.buscar_vinculo(id_v))
        
        if campo == "1":
            rows = vinculo.atualizar_vinculo(id_v, mat_estudante=input("Nova matrícula: "))
        elif campo == "2":
            rows = vinculo.atualizar_vinculo(id_v, curso=int(input("Novo ID do curso: ")))
        elif campo == "3":
            rows = vinculo.atualizar_vinculo(
                id_v, data_entrada=parse_data(input("Nova data entrada (AAAA-MM-DD): ")))
        elif campo == "4":
            rows = vinculo.atualizar_vinculo(id_v, status=input(f"Novo status ({STATUS}): "))
        elif campo == "5":
            rows = vinculo.atualizar_vinculo(
                id_v, data_saida=parse_data(input("Nova data saída (AAAA-MM-DD): ")))
        else:
            print("Campo inválido")
            return
        
        print(f"Atualizados: {rows}")
        
        mostrar("DEPOIS", vinculo.buscar_vinculo(id_v))
    
    elif op == "4":
        id_v = int(input("ID do vínculo a deletar: "))
        mostrar("ANTES", vinculo.buscar_vinculo(id_v))
        print(f"Removidos: {vinculo.deletar_vinculo(id_v)}")
        mostrar("DEPOIS", vinculo.buscar_vinculo(id_v))
    else:
        print("Opção inválida")


def main():
    while True:
        print("\n=== CRUD UNIVERSIDADE ===")
        print("1. Usuário\n2. Estudante\n3. Curso\n4. Vínculo\n0. Sair")
        escolha = input("Escolha uma coleção: ")
        try:
            if escolha == "1":
                menu_usuario()
            elif escolha == "2":
                menu_estudante()
            elif escolha == "3":
                menu_curso()
            elif escolha == "4":
                menu_vinculo()
            elif escolha == "0":
                break
            else:
                print("Opção inválida")
        except DuplicateKeyError as e:
            print(f"Violação de unicidade (chave/UNIQUE): {e.details.get('errmsg', e)}")
        except WriteError as e:
            print(f"Violação de restrição (validador do schema): {e.details.get('errmsg', e)}")
        except PyMongoError as e:
            print(f"Erro no banco: {e}")
        except ValueError as e:
            print(f"Erro: {e}")


if __name__ == "__main__":
    main()