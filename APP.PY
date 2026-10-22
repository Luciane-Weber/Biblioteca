# =============================================================================
# SISTEMA DE CADASTRO DE BIBLIOTECA - ETAPA 7 (CÓDIGO ORGANIZADO E REFATORADO)
# =============================================================================
import json

# --- Armazenamento em Memória (Lista Global) ---
biblioteca = []
ARQUIVO_DADOS = "biblioteca.json"

# --- Funções de Persistência ---

def carregar_dados():
    """Lê o arquivo JSON ao iniciar o programa."""
    global biblioteca
    try:
        with open(ARQUIVO_DADOS, "r", encoding="utf-8") as arquivo:
            biblioteca = json.load(arquivo)
    except FileNotFoundError:
        biblioteca = []
    except json.JSONDecodeError:
        print("[Aviso] Arquivo de dados corrompido. Iniciando biblioteca vazia.")
        biblioteca = []

def salvar_dados():
    """Grava a lista global de livros no arquivo JSON."""
    try:
        with open(ARQUIVO_DADOS, "w", encoding="utf-8") as arquivo:
            json.dump(biblioteca, arquivo, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"[Erro] Não foi possível salvar os dados: {e}")

# --- Função Utilitária (ETAPA 7: Eliminação de Códigos Repetidos) ---

def obter_livro_por_id(mensagem_input):
    """
    Centraliza a captura, conversão e validação do ID do livro.
    Retorna uma tupla (indice, livro) se válido, ou (None, None) se inválido.
    """
    try:
        id_livro = int(input(mensagem_input))
        indice = id_livro - 1

        if indice < 0 or indice >= len(biblioteca):
            print("[Erro] ID inválido! Consulte a lista de livros para ver os IDs válidos.")
            return None, None

        return indice, biblioteca[indice]
    except ValueError:
        print("[Erro] Por favor, digite um número de ID válido.")
        return None, None

# --- Funções de Movimentação do Sistema ---

def cadastrar_livro():
    """Coleta os dados do usuário, armazena e salva no JSON."""
    print("\n--- CADASTRO DE NOVO LIVRO ---")
    titulo = input("Digite o título do livro: ").strip()
    autor = input("Digite o autor do livro: ").strip()
    ano = input("Digite o ano de publicação: ").strip()
    
    if not titulo or not autor or not ano:
        print("\n[Erro] Todos os campos são obrigatórios!")
        return

    novo_livro = {
        "titulo": titulo,
        "autor": autor,
        "ano": ano,
        "disponivel": True
    }
    
    biblioteca.append(novo_livro)
    salvar_dados()
    print(f"\n[Sucesso] Livro '{titulo}' cadastrado com sucesso!")

def listar_livros():
    """Exibe os livros permitindo escolher a ordenação de exibição."""
    print("\n--- OPÇÕES DE ORDENAÇÃO ---")
    print("1. Por ID (Ordem de cadastro)")
    print("2. Por Título (Ordem alfabética)")
    print("3. Por Ano (Ordem cronológica)")
    escolha = input("Escolha como deseja ordenar a lista: ").strip()

    lista_com_id = [(i, livro) for i, livro in enumerate(biblioteca, 1)]

    if escolha == "2":
        lista_com_id.sort(key=lambda item: item[1]["titulo"].lower())
        tipo_ordem = "ORDEM ALFABÉTICA"
    elif escolha == "3":
        lista_com_id.sort(key=lambda item: item[1]["ano"])
        tipo_ordem = "ORDEM CRONOLÓGICA"
    else:
        tipo_ordem = "ORDEM ORIGINAL (ID)"

    print("\n" + "-"*50)
    print(f"       ACERVO DA BIBLIOTECA - {tipo_ordem}       ")
    print("-"*50)
    
    if not biblioteca:
        print("Nenhum livro cadastrado no sistema.")
        print("-"*50)
        return
        
    for original_id, livro in lista_com_id:
        status = "Disponível" if livro["disponivel"] else "Emprestado"
        print(f"ID original para ações: {original_id}")
        print(f"Título: {livro['titulo']}")
        print(f"Autor: {livro['autor']} | Ano: {livro['ano']} | Status: {status}")
        print("-" * 50)

def buscar_livro():
    """Busca livros por TÍTULO, AUTOR ou ANO (ignora o ID)."""
    print("\n--- BUSCAR LIVRO ---")
    if not biblioteca:
        print("[Aviso] A biblioteca está vazia. Não há o que buscar.")
        return
        
    termo_busca = input("Digite o título, autor ou ano que deseja buscar: ").strip().lower()
    
    if not termo_busca:
        print("[Erro] O termo de busca não pode ser vazio!")
        return

    encontrados = []

    for livro in biblioteca:
        no_titulo = termo_busca in livro["titulo"].lower()
        no_autor = termo_busca in livro["autor"].lower()
        no_ano = termo_busca in livro["ano"].lower()
        
        if no_titulo or no_autor or no_ano:
            encontrados.append(livro)

    print("\n" + "="*50)
    print(f"   RESULTADOS DA BUSCA POR: '{termo_busca.upper()}'")
    print("="*50)
    
    if not encontrados:
        print("[Erro] Nenhum livro foi encontrado com essa informação.")
        print("="*50)
        return

    for livro in encontrados:
        status = "Disponível" if livro["disponivel"] else "Emprestado"
        print(f"Título: {livro['titulo']}")
        print(f"Autor: {livro['autor']} | Ano: {livro['ano']} | Status: {status}")
        print("-" * 50)

def emprestar_livro():
    """Altera o status do livro para Emprestado utilizando a função utilitária."""
    print("\n--- EMPRÉSTIMO DE LIVRO ---")
    if not biblioteca:
        print("[Aviso] A biblioteca está vazia.")
        return

    # ETAPA 7: Reutilizando a função de validação de ID
    _, livro = obter_livro_por_id("Digite o ID do livro que deseja emprestar: ")
    
    if livro is None:
        return

    if not livro["disponivel"]:
        print(f"[Erro] O livro '{livro['titulo']}' já está emprestado!")
    else:
        livro["disponivel"] = False
        salvar_dados()
        print(f"\n[Sucesso] Empréstimo do livro '{livro['titulo']}' registrado!")

def devolver_livro():
    """Retorna o status do livro para Disponível utilizando a função utilitária."""
    print("\n--- DEVOLUÇÃO DE LIVRO ---")
    if not biblioteca:
        print("[Aviso] A biblioteca está vazia.")
        return

    # ETAPA 7: Reutilizando a função de validação de ID
    _, livro = obter_livro_por_id("Digite o ID do livro que deseja devolver: ")
    
    if livro is None:
        return

    if livro["disponivel"]:
        print(f"[Aviso] O livro '{livro['titulo']}' já consta como Disponível.")
    else:
        livro["disponivel"] = True
        salvar_dados()
        print(f"\n[Sucesso] Devolução do livro '{livro['titulo']}' registrada!")

def remover_livro():
    """Remove permanentemente um livro utilizando a função utilitária."""
    print("\n--- REMOVER LIVRO ---")
    if not biblioteca:
        print("[Aviso] A biblioteca está vazia.")
        return

    # ETAPA 7: Reutilizando a função de validação de ID e capturando o índice também
    indice, livro = obter_livro_por_id("Digite o ID do livro que deseja excluir do sistema: ")
    
    if livro is None:
        return

    livro_removido = biblioteca.pop(indice)
    salvar_dados()
    print(f"\n[Sucesso] O livro '{livro_removido['titulo']}' foi removido com sucesso!")

# --- Função de Validação Inicial ---
def pre_cadastrar_livros():
    """Insere os 5 livros de teste se a biblioteca estiver vazia."""
    if len(biblioteca) == 0:
        livros_iniciais = [
            {"titulo": "Dom Casmurro", "autor": "Machado de Assis", "ano": "1899", "disponivel": True},
            {"titulo": "O Alquimista", "autor": "Paulo Coelho", "ano": "1988", "disponivel": True},
            {"titulo": "O Cortiço", "autor": "Aluísio Azevedo", "ano": "1890", "disponivel": True},
            {"titulo": "Grande Sertão: Veredas", "autor": "Guimarães Rosa", "ano": "1956", "disponivel": True},
            {"titulo": "Memórias Póstumas de Brás Cubas", "autor": "Machado de Assis", "ano": "1881", "disponivel": True}
        ]
        biblioteca.extend(livros_iniciais)
        salvar_dados()

# --- Menu Principal ---

def exibir_menu():
    """Calcula os contadores do acervo em tempo real e exibe o menu."""
    total = len(biblioteca)
    disponiveis = sum(1 for livro in biblioteca if livro["disponivel"])
    emprestados = total - disponiveis

    print("\n" + "="*35)
    print("         SISTEMA BIBLIOTECA        ")
    print("="*35)
    print(f" Livros cadastrados: {total}")
    print(f" Disponíveis: {disponiveis} | Emprestados: {emprestados}")
    print("-"*35)
    print("1. Cadastrar Livro")
    print("2. Listar Livros (Com Ordenação)")
    print("3. Buscar Livro")
    print("4. Emprestar Livro")
    print("5. Devolver Livro")
    print("6. Remover Livro")
    print("0. Sair")
    print("="*35)

def executar_sistema():
    carregar_dados()
    pre_cadastrar_livros()
    
    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            cadastrar_livro()
        elif opcao == "2":
            listar_livros()
        elif opcao == "3":
            buscar_livro()
        elif opcao == "4":
            emprestar_livro()
        elif opcao == "5":
            devolver_livro()
        elif opcao == "6":
            remover_livro()
        elif opcao == "0":
            print("\nEncerrando o sistema. Até logo!")
            break
        else:
            print("\n[Erro] Opção inválida! Tente novamente.")

# --- Inicialização Direta do Programa ---
executar_sistema()

