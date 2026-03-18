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
    
def area_aluno(request):
    return render(request, 'conecta/area_aluno.html')