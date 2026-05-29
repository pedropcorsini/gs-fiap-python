# ============================================================
# Projeto : Orbital Watch - Monitor de Conjuncoes Orbitais
# Disciplina: Computational Thinking with Python
# Global Solution - 2026
# Curso: Engenharia de Software - TURMA 1ESPU
#
# Integrantes:
#   Pedro Passos Corsini           - RM: 573493
#   Pedro Thyago Araújo dos Santos - RM: 570939
#   Daniel Gomes Torres            - RM: 573436
#   Henrique Lira                  - RM: 571009
# ============================================================


# --- Bibliotecas que vamos usar ---
# 'os' -> para limpar a tela do terminal.
# 'math' -> para cálculos matemáticos (raiz quadrada, pi).
# 'random' -> para gerar distâncias aleatórias simuladas.

import os
import math
import random


# ============================================================
# CONSTANTES 
# Constantes são variáveis que não mudam nunca (são fixas).
# Usamos letras MAIÚSCULAS para identificar constantes.
# ============================================================

RAIO_DA_TERRA = 6371      # raio medio da Terra em km.
PARAMETRO_GRAV = 398600   # parametro gravitacional da Terra (km^3/s^2).

# Nomes dos satélites que vem de fábrica e não podem ser removidos.
SATELITES_FIXOS = ['CBERS-4A', 'AMAZONIA-1', 'SCD-2']


# ============================================================
# LISTA DE SATELITES
# Cada satelite e um dicionario com 4 informacoes:
#   nome     -> identificacao do satelite
#   norad    -> codigo internacional de rastreamento
#   altitude -> altura acima da Terra em km
#   orbita   -> tipo de orbita (LEO / MEO / GEO)
# ============================================================

satelites = [
    {'nome': 'CBERS-4A',   'norad': 44883, 'altitude': 628.0, 'orbita': 'LEO'},
    {'nome': 'AMAZONIA-1', 'norad': 47699, 'altitude': 752.0, 'orbita': 'LEO'},
    {'nome': 'SCD-2',      'norad': 25504, 'altitude': 750.0, 'orbita': 'LEO'},
]


# ============================================================
# FUNCOES UTILITÁRIAS
# Funções pequenas que auxiliam o resto do programa.
# ============================================================

def limpar_tela():
    """Limpa o terminal. Funciona no Windows e no Mac/Linux."""
    if os.name == 'nt':         # 'nt' significa Windows.
        os.system('cls')
    else:                       # Mac ou Linux.
        os.system('clear')

def pausar():
    """Para o programa e espera o usuário apertar Enter."""
    input('\nPressione Enter para continuar...')

def classificar_orbita(altitude):
    """
    Recebe uma altitude em km e retorna o tipo de órbita:
      LEO = Low Earth Orbit  (abaixo de 2.000 km)
      MEO = Medium Earth Orbit (2.000 a 35.000 km)
      GEO = Geostationary Orbit (acima de 35.000 km)
    """
    if altitude < 2000:
        return 'LEO'
    elif altitude < 35000:
        return 'MEO'
    else:
        return 'GEO'


# ============================================================
# MENU PRINCIPAL
# ============================================================

def mostrar_menu():
    """Exibe o menu com as opções disponíveis."""
    print('=' * 105)
    exibir_nome_progama()
    print('=' * 105)
    print('  1. Sobre o projeto')
    print('  2. Cadastrar satélite brasileiro')
    print('  3. Listar satélites cadastrados')
    print('  4. Calcular risco de conjunção')
    print('  5. Simular propagação orbital')
    print('  6. Relatório de risco por órbita')
    print('  7. Sair')
    print('=' * 48)


def sobre_projeto():
    """Exibe informações gerais sobre o Orbital Watch."""
    limpar_tela()
    print('=' * 48)
    print('SOBRE O ORBITAL WATCH')
    print('=' * 48)
    print()
    print('Orbital Watch monitora detritos espaciais e calcula riscos de conjunção')
    print('para satélites brasileiros (CBERS-4A, AMAZONIA-1, SCD-2) em órbita LEO.')
    print('O sistema usa dados públicos da NORAD e a 3ª Lei de Kepler para simular')
    print('propagação orbital e gerar relatórios de risco por faixa orbital (LEO/MEO/GEO).')
    print('Solução gratuita em português, alternativa ao STK. (ODS 9)')
    print()
    pausar()


# ============================================================
# PONTO DE ENTRADA DO PROGRAMA
# Tudo comeca aqui. O 'while True' cria um loop infinito que
# so para quando o usuario escolher a opcao 7 (Sair).
# O 'match/case' e como um if/elif mais elegante do Python 3.10+.
# ============================================================

def exibir_nome_progama():
    """
    Exibe nome do programa.
    """
    print("""
░█████╗░██████╗░██████╗░██╗████████╗░█████╗░██╗░░░░░  ░██╗░░░░░░░██╗░█████╗░████████╗░█████╗░██╗░░██╗
██╔══██╗██╔══██╗██╔══██╗██║╚══██╔══╝██╔══██╗██║░░░░░  ░██║░░██╗░░██║██╔══██╗╚══██╔══╝██╔══██╗██║░░██║
██║░░██║██████╔╝██████╦╝██║░░░██║░░░███████║██║░░░░░  ░╚██╗████╗██╔╝███████║░░░██║░░░██║░░╚═╝███████║
██║░░██║██╔══██╗██╔══██╗██║░░░██║░░░██╔══██║██║░░░░░  ░░████╔═████║░██╔══██║░░░██║░░░██║░░██╗██╔══██║
╚█████╔╝██║░░██║██████╦╝██║░░░██║░░░██║░░██║███████╗  ░░╚██╔╝░╚██╔╝░██║░░██║░░░██║░░░╚█████╔╝██║░░██║
░╚════╝░╚═╝░░╚═╝╚═════╝░╚═╝░░░╚═╝░░░╚═╝░░╚═╝╚══════╝  ░░░╚═╝░░░╚═╝░░╚═╝░░╚═╝░░░╚═╝░░░░╚════╝░╚═╝░░╚═╝
""")

def cadastrar_satelite():
    """
    Pede ao usuário os dados de um novo satélite e salva na lista.
    Valida cada campo com try/except para evitar erros de digitacao.
    Bloqueia cadastro se o nome ja existir na lista.
    """
    limpar_tela()
    print('=' * 48)
    print('CADASTRAR SATELITE')
    print('=' * 48)
    print()

    # --- Validacao do nome ---
    nome = input('Nome do satelite: ').strip().upper()

    if nome == '':
        print('Erro: o nome não pode ficar em branco.')
        pausar()
        return  # 'return' sai da funcao sem cadastrar nada.

    # Verifica se ja existe um satelite com esse nome na lista.
    nomes_ja_cadastrados = [s['nome'] for s in satelites]
    if nome in nomes_ja_cadastrados:
        print(f'Erro: o satelite "{nome}" já esta cadastrado!')
        pausar()
        return

    # --- Validacao do NORAD ID ---
    # try/except: tenta converter para inteiro. Se o usuario digitar
    # letra ou deixar em branco, cai no 'except' e exibe o erro.
    try:
        norad = int(input('NORAD ID (numero inteiro): ').strip())
        if norad <= 0:
            raise ValueError   # forcamos o erro se o numero for negativo.
    except ValueError:
        print('Erro: NORAD ID deve ser um número inteiro positivo.')
        pausar()
        return

    # --- Validacao da altitude ---
    try:
        altitude = float(input('Altitude em km (ex: 550.0): ').strip())
        if altitude <= 0:
            raise ValueError
    except ValueError:
        print('Erro: altitude deve ser um número positivo.')
        pausar()
        return

    # Classifica a orbita automaticamente com base na altitude.
    orbita = classificar_orbita(altitude)

    # Cria o dicionario com os dados do novo satelite.
    novo_satelite = {
        'nome': nome,
        'norad': norad,
        'altitude': altitude,
        'orbita': orbita
    }

    # Adiciona o novo satelite ao final da lista.
    satelites.append(novo_satelite)

    print()
    print(f'Satélite "{nome}" cadastrado com sucesso!')
    print(f'Órbita identificada automaticamente: {orbita}.')
    pausar()


def listar_satelites():
    """
    Mostra todos os satélites cadastrados em formato de tabela.
    Ao final, pergunta se o usuário quer remover algum dos satélites
    que ele mesmo cadastrou (os 3 fixos não podem ser removidos).
    """
    limpar_tela()
    print('=' * 48)
    print('SATÉLITES CADASTRADOS')
    print('=' * 48)
    print()

    if len(satelites) == 0:
        print('Nenhum satélite cadastrado ainda.')
        pausar()
        return

    # Cabecalho da tabela.
    print(f'  {"N":<4} {"Nome":<14} {"Altitude":<12} {"Órbita"}') # Alinhamento de texto
    print('  ' + '-' * 38)

    # Loop 'for' percorre cada satelite da lista.
    for i, satelite in enumerate(satelites, start=1):
        # enumerate() da o indice (i) junto com o item (satelite).
        # start=1 faz a contagem começar do 1 (mais natural pro usuario).
        marcacao = ' [fixo]' if satelite['nome'] in SATELITES_FIXOS else ''  
        print(f'  {i:<4} {satelite["nome"]:<14} {satelite["altitude"]:<12} {satelite["orbita"]}{marcacao}')

    print()
    print('[fixo] = satélite protegido, não pode ser removido.')

    # Filtra apenas satelites que podem ser removidos.
    removiveis = []
    for s in satelites:
        if s['nome'] not in SATELITES_FIXOS:
            removiveis.append(s)

    if len(removiveis) == 0:
        # Se nao ha nada removivel, nao oferece a opcao.
        pausar()
        return

    print()
    resposta = input('Deseja remover algum satelite? (s/n): ').strip().lower()

    if resposta != 's':
        pausar()
        return

    print()
    print('Satélites que podem ser removidos:')

    # Mostra apenas os removiveis com seus numeros originais.
    for i, satelite in enumerate(satelites, start=1):
        if satelite['nome'] not in SATELITES_FIXOS:
            print(f'  {i}. {satelite["nome"]}')

    print()

    try:
        numero = int(input('Digite o número do satélite a remover: ').strip())
        indice = numero - 1  # lista comeca do 0, menu comeca do 1.

        # Verifica se o numero esta dentro do intervalo valido.
        if indice < 0 or indice >= len(satelites):
            raise ValueError

        nome_escolhido = satelites[indice]['nome']

        # Bloqueia remocao dos satelites fixos.
        if nome_escolhido in SATELITES_FIXOS:
            print(f'Erro: "{nome_escolhido}" e um satélite fixo e não pode ser removido.')
            pausar()
            return

        # Remove o satelite da lista.
        satelites.pop(indice)
        print(f'Satelite "{nome_escolhido}" removido com sucesso.')

    except ValueError:
        print('Número inválido. Nenhum satélite foi removido.')

    pausar()


def calcular_risco(distancia_km):
    """
    Recebe a distância em km entre dois objetos em órbita
    e retorna o nível de risco como texto.

    Escala de risco:
      BAIXO   -> distância maior que 1.0 km
      MÉDIO   -> entre 0.5 km e 1.0 km
      ALTO    -> entre 0.2 km e 0.5 km
      CRÍTICO -> menos de 0.2 km (menos de 200 metros!)
    """
    if distancia_km > 1.0:
        return 'BAIXO'
    elif distancia_km > 0.5:
        return 'MEDIO'
    elif distancia_km > 0.2:
        return 'ALTO'
    else:
        return 'CRITICO'


def calcular_risco_interativo():
    """
    Pede ao usuário que escolha dois satélites da lista.
    Gera uma distância aleatória simulada entre eles (0.05 a 5.0 km)
    e exibe o nível de risco calculado.
    """
    limpar_tela()
    print('=' * 48)
    print('CALCULAR RISCO DE CONJUNÇÃO')
    print('=' * 48)
    print()

    # Precisamos de pelo menos 2 satelites para comparar
    if len(satelites) < 2:
        print('E necessário ter ao menos 2 satélites cadastrados.')
        pausar()
        return

    print('Satélites disponiveis:')
    print()
    for i, satelite in enumerate(satelites, start=1):
        print(f'  {i}. {satelite["nome"]}  ({satelite["altitude"]} km - {satelite["orbita"]})')
    print()

    # Selecao do primeiro satelite
    try:
        numero1 = int(input('Escolha o 1° satélite (número): ').strip())
        indice1 = numero1 - 1

        if indice1 < 0 or indice1 >= len(satelites):
            raise ValueError

    except ValueError:
        print('Seleção inválida para o 1° satélite.')
        pausar()
        return

    # Selecao do segundo satelite
    try:
        numero2 = int(input('Escolha o 2° satélite (número): ').strip())
        indice2 = numero2 - 1

        if indice2 < 0 or indice2 >= len(satelites):
            raise ValueError

    except ValueError:
        print('Seleção inválida para o 2° satélite.')
        pausar()
        return

    # Nao faz sentido calcular risco de um satelite com ele mesmo
    if indice1 == indice2:
        print('Erro: escolha dois satélites diferentes.')
        pausar()
        return

    satelite_a = satelites[indice1]
    satelite_b = satelites[indice2]

    # Simula uma distancia aleatoria entre 0.05 km e 5.0 km
    # random.uniform(a, b) gera um numero decimal entre a e b
    distancia = round(random.uniform(0.05, 5.0), 3)
    nivel = calcular_risco(distancia)

    # Exibe o resultado
    print()
    print('-' * 48)
    print('  RESULTADO DA ANÁLISE DE CONJUNÇÃO')
    print('-' * 48)
    print(f'  Satélite A : {satelite_a["nome"]} ({satelite_a["altitude"]} km)')
    print(f'  Satelite B : {satelite_b["nome"]} ({satelite_b["altitude"]} km)')
    print(f'  Distância  : {distancia} km')
    print(f'  Nível      : {nivel}')
    print('-' * 48)

    # Mensagem de alerta dependendo do nivel
    if nivel == 'CRITICO':
        print('  [ALERTA!] Risco crítico! Protocolo de avaliação imediata!')
    elif nivel == 'ALTO':
        print('  [ATENÇÃO] Risco alto. Monitoramento reforçado necessário.')
    elif nivel == 'MEDIO':
        print('  [AVISO] Risco médio. Acompanhar nas próximas horas.')
    else:
        print('  [OK] Risco baixo. Nenhuma ação necessária por agora.')

    pausar()


def simular_propagacao():
    """
    Simula a propagação orbital de um satélite usando a 3° Lei de Kepler.

    A formula calcula o período orbital (tempo para dar uma volta completa)
    e usa isso para descobrir em qual ângulo o satélite estará depois de
    um determinado numero de horas.

    Formula do período orbital:
      T = 2 * pi * raiz_cubica(r^3 / mi)
      onde r = raio da Terra + altitude do satélite
      mi = parâmetro gravitacional da Terra
    """
    limpar_tela()
    print('=' * 48)
    print('  SIMULAR PROPAGAÇÃO ORBITAL')
    print('=' * 48)
    print()

    if len(satelites) == 0:
        print('Nenhum satélite cadastrado.')
        pausar()
        return

    print('Escolha o satélite para simular:')
    print()
    for i, satelite in enumerate(satelites, start=1):
        print(f'  {i}. {satelite["nome"]} - {satelite["altitude"]} km ({satelite["orbita"]})')
    print()

    # Selecao do satelite
    try:
        numero = int(input('Numero do satélite: ').strip())
        indice = numero - 1

        if indice < 0 or indice >= len(satelites):
            raise ValueError

    except ValueError:
        print('Seleção inválida.')
        pausar()
        return

    # Selecao do tempo de simulacao
    try:
        horas = float(input('Quantas horas deseja simular? ').strip())
        if horas <= 0:
            raise ValueError

    except ValueError:
        print('Erro: informe um número positivo de horas.')
        pausar()
        return

    satelite = satelites[indice]
    altitude = satelite['altitude']

    # ---- Calculo pela 3° Lei de Kepler ----
    # Passo 1: raio total = raio da Terra + altitude do satelite
    raio = RAIO_DA_TERRA + altitude                          # em km

    # Passo 2: período orbital em segundos
    # math.sqrt() faz a raiz quadrada
    # math.pi é o valor de pi (3.14...)
    periodo_segundos = 2 * math.pi * math.sqrt(raio**3 / PARAMETRO_GRAV)

    # Passo 3: converter para minutos
    periodo_minutos = periodo_segundos / 60

    # Passo 4: total de segundos simulados
    total_segundos = horas * 3600  

    # Passo 5: quantas orbitas completas o satélite deu
    orbitas_completas = int(total_segundos / periodo_segundos)

    # Passo 6: ângulo final (resto da divisão das orbitas)
    # O operador '%' retorna o resto da divisao
    angulo_final = (total_segundos / periodo_segundos) * 360 % 360

    # ---- Exibe o resultado ----
    print()
    print('-' * 48)
    print('RESULTADO DA SIMULAÇÃO')
    print('-' * 48)
    print(f'Satélite       : {satelite["nome"]}')
    print(f'Altitude       : {altitude} km')
    print(f'Período        : {periodo_minutos:.2f} minutos por órbita')
    print(f'Tempo simulado : {horas} horas')
    print(f'Órbitas dadas  : {orbitas_completas}')
    print(f'Ângulo final   : {angulo_final:.2f} graus')
    print('-' * 48)

    pausar()


def relatorio_por_orbita():
    """
    Agrupa os satélites cadastrados por faixa orbital e
    exibe um relatório com contagem e altitude média de cada grupo.

    Faixas:
      LEO = abaixo de 2.000 km (mais denso em detritos)
      MEO = entre 2.000 e 35.000 km (GPS, por exemplo)
      GEO = acima de 35.000 km (satélites de comunicação)
    """
    limpar_tela()
    print('=' * 48)
    print('RELATÓRIO DE RISCO POR ÓRBITA')
    print('=' * 48)
    print()

    grupo_leo = []
    grupo_meo = []
    grupo_geo = []

    for s in satelites:
        if s['altitude'] < 2000:
            grupo_leo.append(s)
        elif 2000 <= s['altitude'] < 35000:
            grupo_meo.append(s)
        else:
            grupo_geo.append(s)

    def exibir_grupo(nome_faixa, grupo):
        """Função auxiliar que exibe as informações de um grupo."""
        print(f'[{nome_faixa}]  -  {len(grupo)} satelite(s)')

        if len(grupo) == 0:
            print('Nenhum satélite nesta faixa.')
        else:
            # Calcula a media das altitudes do grupo
            soma_altitudes = sum(s['altitude'] for s in grupo)
            altitude_media = soma_altitudes / len(grupo)
            print(f'Altitude média: {altitude_media:.1f} km')

            # Lista cada satelite do grupo
            for satelite in grupo:
                print(f'- {satelite["nome"]} ({satelite["altitude"]} km)')
        print()

    # Exibe os tres grupos
    exibir_grupo('LEO - Órbita Baixa   < 2.000 km', grupo_leo)
    exibir_grupo('MEO - Órbita Media   2.000 a 35.000 km', grupo_meo)
    exibir_grupo('GEO - Órbita Alta    >= 35.000 km', grupo_geo)

    print(f'Total de satélites monitorados: {len(satelites)}')
    print()

    pausar()


def iniciar_programa():
    """Função principal que roda o loop do menu."""
    while True:
        limpar_tela()
        mostrar_menu()

        opcao = input('Escolha uma opção: ').strip()

        # match/case: olha o valor de 'opcao' e executa o bloco certo
        match opcao:
            case '1':
                sobre_projeto()
            case '2':
                cadastrar_satelite()
            case '3':
                listar_satelites()
            case '4':
                calcular_risco_interativo()
            case '5':
                simular_propagacao()
            case '6':
                relatorio_por_orbita()
            case '7':
                print()
                print('Encerrando o Orbital Watch. Até logo!')
                print()
                break   # break sai do loop while e encerra o programa
            case _:
                # O underscore '_' e o "caso contrario" (equivale ao else)
                print('Opção inválida! Digite um número de 1 a 7.')
                pausar()


# Este bloco garante que o programa so roda quando voce executar
# este arquivo diretamente (nao quando importado por outro arquivo)
if __name__ == '__main__':
    iniciar_programa()
