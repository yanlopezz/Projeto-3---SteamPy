import csv
import datetime

from jogo import Jogo
from filabacklog import FilaBacklog
from pilharecentes import PilhasRecentes
from sessaojogo import SessaoJogo

catalogo = []
indice_jogos = {}
backlog = FilaBacklog()
recentes = PilhasRecentes()
historico = []
tempo_por_jogo = {}


def carregar_jogos(nome_arquivo):
    global catalogo, indice_jogos
    catalogo = []
    indice_jogos = {}
    try:
        arquivo = open(nome_arquivo, encoding='utf-8')
        leitor = csv.reader(arquivo)
        next(leitor)
        id_atual = 1
        for linha in leitor:
            try:
                if len(linha) < 13:
                    continue
                img = linha[0]
                titulo = linha[1]
                console = linha[2]
                genero = linha[3]
                publisher = linha[4]
                developer = linha[5]
                try:
                    critic_score = float(linha[6])
                except:
                    critic_score = 0.0
                try:
                    total_vendas = float(linha[7])
                except:
                    total_vendas = 0.0
                try:
                    vendas_an = float(linha[8])
                except:
                    vendas_an = 0.0
                try:
                    vendas_jp = float(linha[9])
                except:
                    vendas_jp = 0.0
                try:
                    vendas_eu = float(linha[10])
                except:
                    vendas_eu = 0.0
                try:
                    outras_vendas = float(linha[11])
                except:
                    outras_vendas = 0.0
                data_lanc = linha[12]
                jogo = Jogo(id_atual, titulo, console, genero, publisher, developer, critic_score, total_vendas, vendas_an, vendas_jp, vendas_eu, outras_vendas, data_lanc)
                catalogo.append(jogo)
                indice_jogos[id_atual] = jogo
                id_atual += 1
            except:
                continue
        arquivo.close()
        print(f'Catálogo carregado com {len(catalogo)} jogos.')
    except:
        print('Erro ao carregar o arquivo.')


def listar_jogos():
    if len(catalogo) == 0:
        print('Catálogo vazio. Carregue o catálogo primeiro.')
        return
    for jogo in catalogo:
        jogo.exibir()


def buscar_jogo_por_nome(termo):
    resultado = []
    for jogo in catalogo:
        if termo.lower() in jogo.titulo.lower():
            resultado.append(jogo)
    if len(resultado) == 0:
        print('Nenhum jogo encontrado.')
    else:
        for jogo in resultado:
            jogo.exibir()
    return resultado


def filtrar_por_genero(genero):
    resultado = []
    for jogo in catalogo:
        if jogo.genero.lower() == genero.lower():
            resultado.append(jogo)
    if len(resultado) == 0:
        print('Nenhum jogo encontrado para esse gênero.')
    else:
        for jogo in resultado:
            jogo.exibir()
    return resultado


def filtrar_por_console(console):
    resultado = []
    for jogo in catalogo:
        if jogo.console.lower() == console.lower():
            resultado.append(jogo)
    if len(resultado) == 0:
        print('Nenhum jogo encontrado para esse console.')
    else:
        for jogo in resultado:
            jogo.exibir()
    return resultado


def filtrar_por_nota(nota_minima):
    resultado = []
    for jogo in catalogo:
        if jogo.critic_score >= nota_minima:
            resultado.append(jogo)
    if len(resultado) == 0:
        print('Nenhum jogo encontrado com essa nota mínima.')
    else:
        for jogo in resultado:
            jogo.exibir()
    return resultado


def filtrar_por_vendas(vendas_minimas):
    resultado = []
    for jogo in catalogo:
        if jogo.total_vendas >= vendas_minimas:
            resultado.append(jogo)
    if len(resultado) == 0:
        print('Nenhum jogo encontrado com esse mínimo de vendas.')
    else:
        for jogo in resultado:
            jogo.exibir()
    return resultado


def filtrar_por_publisher(publisher):
    resultado = []
    for jogo in catalogo:
        if jogo.publisher.lower() == publisher.lower():
            resultado.append(jogo)
    if len(resultado) == 0:
        print('Nenhum jogo encontrado para essa publisher.')
    else:
        for jogo in resultado:
            jogo.exibir()
    return resultado


def ordenar_jogos(criterio):
    if len(catalogo) == 0:
        print('Catálogo vazio.')
        return

    lista = catalogo[:]

    if criterio == 'titulo':
        for i in range(len(lista)):
            for j in range(i + 1, len(lista)):
                if lista[i].titulo > lista[j].titulo:
                    lista[i], lista[j] = lista[j], lista[i]
    elif criterio == 'nota':
        for i in range(len(lista)):
            for j in range(i + 1, len(lista)):
                if lista[i].critic_score < lista[j].critic_score:
                    lista[i], lista[j] = lista[j], lista[i]
    elif criterio == 'vendas':
        for i in range(len(lista)):
            for j in range(i + 1, len(lista)):
                if lista[i].total_vendas < lista[j].total_vendas:
                    lista[i], lista[j] = lista[j], lista[i]
    elif criterio == 'data':
        for i in range(len(lista)):
            for j in range(i + 1, len(lista)):
                if lista[i].data_lanc > lista[j].data_lanc:
                    lista[i], lista[j] = lista[j], lista[i]
    elif criterio == 'console':
        for i in range(len(lista)):
            for j in range(i + 1, len(lista)):
                if lista[i].console > lista[j].console:
                    lista[i], lista[j] = lista[j], lista[i]
    elif criterio == 'genero':
        for i in range(len(lista)):
            for j in range(i + 1, len(lista)):
                if lista[i].genero > lista[j].genero:
                    lista[i], lista[j] = lista[j], lista[i]
    else:
        print('Critério inválido.')
        return

    for jogo in lista:
        jogo.exibir()


def adicionar_ao_backlog(jogo):
    if backlog.contem(jogo.id_jogo):
        print('Esse jogo já está no backlog.')
        return
    backlog.enqueue(jogo)
    print(f'{jogo.titulo} adicionado ao backlog.')


def mostrar_backlog():
    backlog.mostrar()


def jogar_proximo():
    jogo = backlog.dequeue()
    if jogo is None:
        print('Backlog vazio.')
        return
    print(f'Iniciando: {jogo.titulo}')
    recentes.push(jogo)
    tempo = float(input('Quantas horas você jogou nessa sessão? '))
    registrar_sessao(jogo, tempo)


def salvar_backlog():
    arquivo = open('backlog.txt', 'w', encoding='utf-8')
    arquivo.write('id;titulo;console\n')
    for jogo in backlog.dados:
        arquivo.write(f'{jogo.id_jogo};{jogo.titulo};{jogo.console}\n')
    arquivo.close()
    print('Backlog salvo com sucesso.')


def carregar_backlog():
    try:
        arquivo = open('backlog.txt', 'r', encoding='utf-8')
        linhas = arquivo.readlines()
        arquivo.close()
        linhas = linhas[1:]
        for linha in linhas:
            linha = linha.strip()
            if linha == '':
                continue
            partes = linha.split(';')
            if len(partes) < 3:
                continue
            try:
                id_jogo = int(partes[0])
            except:
                continue
            if id_jogo in indice_jogos:
                jogo = indice_jogos[id_jogo]
                if not backlog.contem(id_jogo):
                    backlog.enqueue(jogo)
        print('Backlog carregado.')
    except:
        print('Nenhum backlog salvo encontrado.')


def _calcular_status(tempo_total):
    if tempo_total < 2:
        return 'iniciado'
    elif tempo_total < 10:
        return 'em andamento'
    elif tempo_total < 20:
        return 'muito jogado'
    else:
        return 'concluído simbolicamente'


def registrar_sessao(jogo, tempo):
    if jogo.id_jogo not in tempo_por_jogo:
        tempo_por_jogo[jogo.id_jogo] = 0.0
    tempo_por_jogo[jogo.id_jogo] += tempo
    tempo_total = tempo_por_jogo[jogo.id_jogo]
    status = _calcular_status(tempo_total)
    data_sessao = datetime.date.today().strftime('%Y-%m-%d')
    sessao = SessaoJogo(jogo, tempo, data_sessao, tempo_total, status)
    historico.append(sessao)
    recentes.push(jogo)
    print(f'Sessão registrada! Total em {jogo.titulo}: {tempo_total}h | Status: {status}')
    salvar_historico()


def mostrar_recentes():
    if recentes.is_empty():
        print('Nenhum jogo recente.')
        return
    recentes.mostrar()


def retomar_ultimo_jogo():
    jogo = recentes.topo()
    if jogo is None:
        print('Nenhum jogo recente para retomar.')
        return
    print(f'Retomando: {jogo.titulo}')
    recentes.push(jogo)
    tempo = float(input('Quantas horas você jogou nessa sessão? '))
    registrar_sessao(jogo, tempo)


def salvar_historico():
    arquivo = open('historico_jogo.txt', 'w', encoding='utf-8')
    arquivo.write('titulo;tempo_sessao;tempo_total;status\n')
    for sessao in historico:
        arquivo.write(f'{sessao.jogo.titulo};{sessao.tempo_jogado};{sessao.tempo_total};{sessao.status}\n')
    arquivo.close()


def carregar_historico():
    global historico
    try:
        arquivo = open('historico_jogo.txt', 'r', encoding='utf-8')
        linhas = arquivo.readlines()
        arquivo.close()
        linhas = linhas[1:]
        for linha in linhas:
            linha = linha.strip()
            if linha == '':
                continue
            partes = linha.split(';')
            if len(partes) < 4:
                continue
            titulo = partes[0]
            try:
                tempo_sessao = float(partes[1])
            except:
                tempo_sessao = 0.0
            try:
                tempo_total = float(partes[2])
            except:
                tempo_total = 0.0
            status = partes[3]
            jogo_encontrado = None
            for j in catalogo:
                if j.titulo == titulo:
                    jogo_encontrado = j
                    break
            if jogo_encontrado is None:
                continue
            data_sessao = 'carregado'
            sessao = SessaoJogo(jogo_encontrado, tempo_sessao, data_sessao, tempo_total, status)
            historico.append(sessao)
            tempo_por_jogo[jogo_encontrado.id_jogo] = tempo_total
        print('Histórico carregado.')
    except:
        print('Nenhum histórico salvo encontrado.')


def salvar_recentes():
    arquivo = open('recentes.txt', 'w', encoding='utf-8')
    arquivo.write('id;titulo;console\n')
    for jogo in recentes.dados:
        arquivo.write(f'{jogo.id_jogo};{jogo.titulo};{jogo.console}\n')
    arquivo.close()


def carregar_recentes():
    try:
        arquivo = open('recentes.txt', 'r', encoding='utf-8')
        linhas = arquivo.readlines()
        arquivo.close()
        linhas = linhas[1:]
        for linha in linhas:
            linha = linha.strip()
            if linha == '':
                continue
            partes = linha.split(';')
            if len(partes) < 3:
                continue
            try:
                id_jogo = int(partes[0])
            except:
                continue
            if id_jogo in indice_jogos:
                recentes.push(indice_jogos[id_jogo])
        print('Recentes carregados.')
    except:
        print('Nenhum arquivo de recentes encontrado.')


def mostrar_historico():
    if len(historico) == 0:
        print('Nenhuma sessão registrada.')
        return
    for sessao in historico:
        sessao.exibir()


def _buscar_jogo_por_id(id_jogo):
    if id_jogo in indice_jogos:
        return indice_jogos[id_jogo]
    return None


def menu():
    carregar_jogos('dataset.csv')
    carregar_backlog()
    carregar_historico()
    carregar_recentes()

    while True:
        print('\n===== STEAMPY =====')
        print('1.  Carregar catálogo')
        print('2.  Listar jogos')
        print('3.  Buscar jogo por nome')
        print('4.  Filtrar por gênero')
        print('5.  Filtrar por console')
        print('6.  Filtrar por nota mínima')
        print('7.  Filtrar por vendas mínimas')
        print('8.  Filtrar por publisher')
        print('9.  Ordenar catálogo')
        print('10. Adicionar jogo ao backlog')
        print('11. Ver backlog')
        print('12. Jogar próximo do backlog')
        print('13. Ver jogos recentes')
        print('14. Retomar último jogo')
        print('15. Registrar tempo de jogo')
        print('16. Ver histórico completo')
        print('17. Salvar backlog')
        print('18. Sair')
        print('===================')

        opcao = input('Escolha uma opção: ')

        if opcao == '1':
            carregar_jogos('dataset.csv')

        elif opcao == '2':
            listar_jogos()

        elif opcao == '3':
            termo = input('Digite o nome ou parte do nome: ')
            buscar_jogo_por_nome(termo)

        elif opcao == '4':
            genero = input('Digite o gênero: ')
            filtrar_por_genero(genero)

        elif opcao == '5':
            console = input('Digite o console: ')
            filtrar_por_console(console)

        elif opcao == '6':
            try:
                nota = float(input('Digite a nota mínima: '))
                filtrar_por_nota(nota)
            except:
                print('Valor inválido.')

        elif opcao == '7':
            try:
                vendas = float(input('Digite o mínimo de vendas (em milhões): '))
                filtrar_por_vendas(vendas)
            except:
                print('Valor inválido.')

        elif opcao == '8':
            publisher = input('Digite o nome da publisher: ')
            filtrar_por_publisher(publisher)

        elif opcao == '9':
            print('Critérios: titulo, nota, vendas, data, console, genero')
            criterio = input('Digite o critério: ')
            ordenar_jogos(criterio)

        elif opcao == '10':
            try:
                id_jogo = int(input('Digite o ID do jogo: '))
                jogo = _buscar_jogo_por_id(id_jogo)
                if jogo:
                    adicionar_ao_backlog(jogo)
                else:
                    print('Jogo não encontrado.')
            except:
                print('ID inválido.')

        elif opcao == '11':
            mostrar_backlog()

        elif opcao == '12':
            jogar_proximo()
            salvar_backlog()
            salvar_recentes()

        elif opcao == '13':
            mostrar_recentes()

        elif opcao == '14':
            retomar_ultimo_jogo()
            salvar_recentes()

        elif opcao == '15':
            try:
                id_jogo = int(input('Digite o ID do jogo: '))
                jogo = _buscar_jogo_por_id(id_jogo)
                if jogo:
                    tempo = float(input('Quantas horas você jogou? '))
                    recentes.push(jogo)
                    registrar_sessao(jogo, tempo)
                    salvar_recentes()
                else:
                    print('Jogo não encontrado.')
            except:
                print('Valor inválido.')

        elif opcao == '16':
            mostrar_historico()

        elif opcao == '17':
            salvar_backlog()

        elif opcao == '18':
            salvar_backlog()
            salvar_historico()
            salvar_recentes()
            print('Até logo!')
            break

        else:
            print('Opção inválida.')


menu()
