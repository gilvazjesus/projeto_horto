from django.shortcuts import render
from django.conf import settings

def conecta(request):
    return render(request, 'conecta/home.html')
    
# ------------------------------------------ Chamada ------------------------------------------
from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from django.contrib import messages
import pandas as pd
import os

senha_correta = "hora_chamada"

alunos = [
    "Miguel Simões",
    "Miguel Martins ",
    "João Tomaz ",
    "Thiago Ribeiro",
    "Pietro",
    "Bianca dos Santos",
    "Lucius Calisto",
    "Pedro Henrique",
    "Byanca Cavenatti",
]


def gerar_datas():
    return ["21/03", "28/03", "11/04", "18/04", "25/04","09/05", "16/05", "23/05", "30/05", "13/06", "20/06", "27/06"]


def carregar_presenca(datas):

    arquivo = "presenca_atual.csv"

    if os.path.exists(arquivo):
        df = pd.read_csv(arquivo, index_col=0)

        for data in datas:
            if data not in df.columns:
                df[data] = False

    else:
        df = pd.DataFrame(False, index=alunos, columns=datas)

    return df


# ------------------------------------------ Chamada ------------------------------------------
from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from django.contrib import messages
import pandas as pd
import os

from django.shortcuts import render, redirect
from django.contrib import messages

def chamada(request):

    arquivos = []


    caminho_absoluto = os.path.join(settings.BASE_DIR, 'static','conecta','files','Lista_Chamada.xlsx')
    print(caminho_absoluto)



    datas = gerar_datas()
    df_presenca = carregar_presenca(datas)

    tabela = []

    for aluno in alunos:
        linha = {"aluno": aluno, "presencas": []}

        for data in datas:
            linha["presencas"].append({
                "data": data,
                "checked": bool(df_presenca.loc[aluno, data])
            })

        tabela.append(linha)

    if request.method == "POST":

        senha = request.POST.get("senha")

        if senha != senha_correta:
            messages.error(request, "❌ Senha incorreta! Presença não salva.")
            return redirect("chamada")

        for aluno in alunos:
            for data in datas:
                checkbox_name = f"{aluno}_{data}"
                df_presenca.loc[aluno, data] = checkbox_name in request.POST

        df_presenca.to_csv("presenca_atual.csv")

        messages.success(request, "✅ Presença salva com sucesso!")
        return redirect("chamada")

    return render(request, "conecta/chamada.html", {
        "datas": datas,
        "tabela": tabela
    })

def calendario(request):

    # Caminho do arquivo Excel
    caminho = os.path.join(settings.BASE_DIR, 'conecta','static','conecta','files','Calendario.xlsx')

    # Lê o Excel
    df = pd.read_excel(caminho)

    # Converte para lista de dicionários
    dados = df.to_dict(orient='records')


    return render(request, 'conecta/calendario.html', {'dados': dados})
    
import os
import pandas as pd
import csv
from django.conf import settings
from django.shortcuts import render, redirect

DIARIO_CSV = os.path.join(settings.BASE_DIR, 'conecta', 'static', 'conecta', 'files', 'diario.csv')

# Senha definida no backend
SENHA_PROFESSOR = "sou_professor"

def area_professor(request):
    acesso_permitido = False
    erro_senha = False

    # Verifica se o professor enviou a senha
    if request.method == 'POST' and 'senha' in request.POST:
        senha_digitada = request.POST.get('senha')
        if senha_digitada == SENHA_PROFESSOR:
            acesso_permitido = True
        else:
            erro_senha = True

    # Se não enviou senha ou está errada, mostra só formulário de login
    if not acesso_permitido and 'data' not in request.POST:
        return render(request, 'conecta/area_professor.html', {'erro_senha': erro_senha})

    # Caminho do arquivo Excel de materiais
    caminho = os.path.join(settings.BASE_DIR, 'conecta', 'static', 'conecta', 'files', 'Materiais.xlsx')
    df = pd.read_excel(caminho)

    # Renomeia colunas do Excel
    df = df.rename(columns={
        'nome da aula': 'nome_aula',
        'link do arquivo': 'link_arquivo',
    })

    dados = df.to_dict(orient='records')

    # -------------- Diário de bordo --------------
    # Se houver POST de anotação
    if request.method == 'POST' and 'data' in request.POST:
        data = request.POST.get('data')
        anotacao = request.POST.get('anotacao')
        if data and anotacao:
            if not os.path.exists(DIARIO_CSV):
                with open(DIARIO_CSV, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(['data', 'anotacao'])
            with open(DIARIO_CSV, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([data, anotacao])
        return redirect(request.path)

    # Lê as anotações existentes
    anotacoes = []
    if os.path.exists(DIARIO_CSV):
        with open(DIARIO_CSV, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                anotacoes.append(row)

    return render(request, 'conecta/area_professor.html', {
        'aulas': dados,
        'anotacoes': anotacoes
    })
    
# views.py

import os
import csv

from django.conf import settings
from django.shortcuts import render, redirect


# ==========================
# CSV
# ==========================
MATERIAIS_CSV = 'materiais.csv'

# ==========================
# SENHA
# ==========================
SENHA_UPLOAD = 'subir_material'


def material_aula(request):

    # ==========================
    # ERRO SENHA
    # ==========================
    erro_senha = False

    # ==========================
    # POST
    # ==========================
    if request.method == 'POST':

        acao = request.POST.get('acao')

        senha = request.POST.get('senha')

        # senha errada
        if senha != SENHA_UPLOAD:

            erro_senha = True

        else:

            # ==========================
            # SALVAR
            # ==========================
            if acao == 'salvar':

                descricao = request.POST.get(
                    'descricao'
                )

                tipo = request.POST.get(
                    'tipo_material'
                )

                link = ''
                arquivo = ''

                # ======================
                # LINK
                # ======================
                if tipo == 'link':

                    link = request.POST.get(
                        'link'
                    )

                # ======================
                # ARQUIVO
                # ======================
                if tipo == 'arquivo':

                    arquivo_enviado = request.FILES.get(
                        'arquivo'
                    )

                    if arquivo_enviado:

                        pasta_arquivos = os.path.join(
                            settings.BASE_DIR,
                            'conecta',
                            'static',
                            'conecta',
                            'files'
                        )

                        # cria pasta
                        os.makedirs(
                            pasta_arquivos,
                            exist_ok=True
                        )

                        caminho_arquivo = os.path.join(
                            pasta_arquivos,
                            arquivo_enviado.name
                        )

                        # salva arquivo
                        with open(
                            caminho_arquivo,
                            'wb+'
                        ) as destino:

                            for chunk in arquivo_enviado.chunks():

                                destino.write(chunk)

                        # caminho html
                        arquivo = (
                            '/static/conecta/files/'
                            + arquivo_enviado.name
                        )

                # ======================
                # CSV
                # ======================
                arquivo_existe = os.path.exists(
                    MATERIAIS_CSV
                )

                with open(
                    MATERIAIS_CSV,
                    'a',
                    newline='',
                    encoding='utf-8'
                ) as f:

                    writer = csv.writer(f)

                    # cabeçalho
                    if not arquivo_existe:

                        writer.writerow([
                            'descricao',
                            'tipo_material',
                            'link',
                            'arquivo'
                        ])

                    # linha
                    writer.writerow([
                        descricao,
                        tipo,
                        link,
                        arquivo
                    ])

                return redirect(request.path)

            # ==========================
            # EXCLUIR
            # ==========================
            if acao == 'excluir':

                linha_excluir = int(
                    request.POST.get('linha')
                )

                linhas = []

                with open(
                    MATERIAIS_CSV,
                    newline='',
                    encoding='utf-8'
                ) as f:

                    reader = csv.reader(f)

                    for row in reader:

                        linhas.append(row)

                cabecalho = linhas[0]

                dados = linhas[1:]

                # ======================
                # PEGA ITEM
                # ======================
                item = dados[linha_excluir]

                tipo_material = item[1]

                caminho_arquivo = item[3]

                # ======================
                # APAGA ARQUIVO FÍSICO
                # ======================
                if tipo_material == 'arquivo':

                    if caminho_arquivo:

                        caminho_fisico = os.path.join(
                            settings.BASE_DIR,
                            caminho_arquivo.replace(
                                '/static/',
                                'conecta/static/'
                            )
                        )

                        if os.path.exists(
                            caminho_fisico
                        ):

                            os.remove(
                                caminho_fisico
                            )

                # remove linha csv
                del dados[linha_excluir]

                # reescreve csv
                with open(
                    MATERIAIS_CSV,
                    'w',
                    newline='',
                    encoding='utf-8'
                ) as f:

                    writer = csv.writer(f)

                    writer.writerow(cabecalho)

                    writer.writerows(dados)

                return redirect(request.path)

    # ==========================
    # LER MATERIAIS
    # ==========================
    materiais = []

    if os.path.exists(MATERIAIS_CSV):

        with open(
            MATERIAIS_CSV,
            newline='',
            encoding='utf-8'
        ) as f:

            reader = csv.DictReader(f)

            for row in reader:

                materiais.append(row)

    # ==========================
    # RENDER
    # ==========================
    return render(
        request,
        'conecta/material_aula.html',
        {

            'materiais': materiais,
            'erro_senha': erro_senha

        }
    )
    
def area_aluno(request):
    return render(request, 'conecta/area_aluno.html')