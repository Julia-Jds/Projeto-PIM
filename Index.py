import json, os, time, traceback, hashlib
from datetime import datetime

ARQUIVO_DADOS = "alunos.json"

def criptografar(texto):
    return hashlib.sha256(texto.encode()).hexdigest()

def descriptografar(texto):
    return texto

def salvar_dados(dados):
    try:
        with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
            f.write(json.dumps(dados, ensure_ascii=False, indent=2))
    except Exception as e:
        print("Erro ao salvar os dados:", e)
        traceback.print_exc()

def carregar_dados():
    if os.path.exists(ARQUIVO_DADOS):  
        with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
            conteudo = f.read()
            if conteudo:
                try:
                    return json.loads(conteudo)
                except Exception as e:
                    print("Erro ao carregar dados:", e)
                    traceback.print_exc()
    return []

def separador():
    print("-" * 40)

def cadastrar_usuario(dados):
    separador()
    print("CADASTRO DE NOVO USUÁRIO")
    separador()

    nome = input("Nome completo: ")
    idade = input("Idade: ")
    email = input("Email: ")

    if any(aluno.get("email") == email for aluno in dados):
        print("Já existe um usuário com este e-mail.")
        return

    senha = input("Crie uma senha: ")
    consentimento = input("Autorizo o uso dos meus dados pessoais e acadêmicos para fins educacionais e estatísticos (s/n): ").lower()
    if consentimento != "s":
        print("Cadastro cancelado. Consentimento é obrigatório.")
        return

    cursos_disponiveis = ["Lógica de Programação", "Cibersegurança", "Python"]
    print("\nCursos disponíveis:")
    for i, curso in enumerate(cursos_disponiveis, 1):
        print(f"{i}. {curso}")

    escolhas = input("Escolha os cursos (ex: 1,2): ").split(",")
    cursos = [cursos_disponiveis[int(i.strip()) - 1] for i in escolhas if i.strip().isdigit() and 1 <= int(i.strip()) <= len(cursos_disponiveis)]

    if not cursos:
        print("Nenhum curso válido selecionado. Cadastro cancelado.")
        return

    dados.append({
        "nome": nome,
        "idade": idade,
        "email": email,
        "senha": criptografar(senha),
        "cursos": cursos,
        "tempo_total": 0,
        "acessos": 0
    })
    salvar_dados(dados)
    print("Usuário cadastrado com sucesso!")

def login(dados):
    separador()
    print("LOGIN")
    separador()

    email = input("Email: ")
    senha = input("Senha: ")

    senha_hash = criptografar(senha)

    for u in dados:
        try:
            if u.get("email") == email and u.get("senha", "") == senha_hash:
                print(f"\nBem-vindo(a), {u.get('nome')}!")
                u["acessos"] = u.get("acessos", 0) + 1
                menu_usuario(u, dados)
                return
        except Exception as e:
            print("Erro ao tentar autenticar:", e)
            traceback.print_exc()
    print("Email ou senha incorretos!")

def menu_usuario(u, dados):
    while True:
        separador()
        print(f"MENU DE {u.get('nome')}")
        separador()
        print("1. Ver cursos\n2. Estudar lógica\n3. Estudar ciber\n4. Estudar Python")
        print("5. Ver relatório\n6. Apagar minha conta\n7. Sair")
        op = input("Escolha: ")

        if op == "1":
            listar_cursos()
        elif op == "2":
            tempo = curso("Lógica de Programação")
            u["tempo_total"] = float(u.get("tempo_total", 0)) + tempo
            salvar_dados(dados)
        elif op == "3":
            tempo = curso("Cibersegurança")
            u["tempo_total"] = float(u.get("tempo_total", 0)) + tempo
            salvar_dados(dados)
        elif op == "4":
            tempo = curso("Python")
            u["tempo_total"] = float(u.get("tempo_total", 0)) + tempo
            salvar_dados(dados)
        elif op == "5":
            print(f"\nNome: {u.get('nome')}\nEmail: {u.get('email')}\nCursos: {', '.join(u.get('cursos', []))}")
            print(f"Acessos: {u.get('acessos', 0)}\nTempo total: {int(float(u.get('tempo_total', 0)))}s")
        elif op == "6":
            confirm = input("Tem certeza que deseja apagar sua conta? (s/n): ").lower()
            if confirm == "s":
                dados.remove(u)
                salvar_dados(dados)
                print("Conta apagada com sucesso.")
                break
        elif op == "7":
            salvar_dados(dados)
            print("Saindo...")
            break
        else:
            print("Opção inválida!")

def listar_cursos():
    separador()
    print("CURSOS DISPONÍVEIS")
    separador()
    for i, curso in enumerate(["Lógica de Programação", "Cibersegurança", "Python"], 1):
        print(f"{i}. {curso}")

def curso(nome):
    separador()
    print(f"CURSO DE {nome} - Módulo Introdutório")
    inicio = time.time()
    input("\nPressione Enter para continuar...")
    duracao = time.time() - inicio
    return duracao

def relatorio_alunos(dados):
    separador()
    print("RELATÓRIO GERAL DE ALUNOS")
    separador()
    if not dados:
        print("Nenhum aluno cadastrado.")
    else:
        for a in dados:
            try:
                print(f"Nome: {a.get('nome')}\nEmail: {a.get('email')}\nIdade: {a.get('idade')}")
                print(f"Cursos: {', '.join(a.get('cursos', []))}\nAcessos: {a.get('acessos', 0)}")
                print(f"Tempo total: {int(float(a.get('tempo_total', 0)))}s")
                separador()
            except Exception as e:
                print("Erro ao exibir aluno:", e)
                traceback.print_exc()

def menu_principal():
    dados = carregar_dados()
    while True:
        separador()
        print("PLATAFORMA - ONG EDUCACIONAL")
        separador()
        print("1. Cadastrar\n2. Login\n3. Ver Relatório\n4. Sair")
        esc = input("Escolha: ")
        if esc == "1":
            cadastrar_usuario(dados)
        elif esc == "2":
            login(dados)
        elif esc == "3":
            relatorio_alunos(dados)
        elif esc == "4":
            print("Saindo...")
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    menu_principal()
