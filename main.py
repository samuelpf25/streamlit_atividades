#data de edição 30/06/2023
#**********************************************************************************************************************

#**********************************************************************************************************************

#IMPORTAÇÕES
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st
import pandas as pd
from email.message import EmailMessage
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#**********************************************************************************************************************

#**********************************************************************************************************************

#VARIÁVEIS GLOBAIS

#**********************************************************************************************************************

#**********************************************************************************************************************

coluna={'Atividade': 3,'Descrição': 4, 'Fluxo': 5, 'Vinculado a Atividade': 6, 'Link': 7, 'Responsável': 8, 'Data de Entrega': 9, 'Status': 10,'Designado por': 11,'Unidade de Medida': 12,'Total': 13,'Executado': 14,'Categoria': 15, 'e-mail': 16, 'corpo': 19,'copia_email': 21, 'obs_alerta': 22, 'data_alerta': 23, 'v_email_alerta': 24, 'verif_alerta': 25}

coluna_dados={'Nome': 3,'Status': 4, 'Vínculo': 5, 'Data de Finalização': 6, 'e-mail': 7,'Unidades de Medida': 10, 'Categorias': 11}

status_lista=['','A iniciar','Em andamento','Pendente','Parado','Concluído']

#Status	Vínculo	Data de Finalização
scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("controle.json", scope)

cliente = gspread.authorize(creds)

hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
#fim ocultar menu
#padroes
padrao = '<p style="font-family:Courier; color:Blue; font-size: 15px;"'
infor = '<p style="font-family:Courier; color:Green; font-size: 15px;"'
alerta = '<p style="font-family:Courier; color:Red; font-size: 15px;"'
titulo = '<p style="font-family:Courier; color:Blue; font-size: 20px;"'
cabecalho='<div id="logo" class="span8 small"><a title="Universidade Federal do Tocantins"><img src="https://ww2.uft.edu.br/images/template/brasao.png" alt="Universidade Federal do Tocantins"><span class="portal-title-1"></span><h1 class="portal-title corto">Universidade Federal do Tocantins</h1><span class="portal-description">COINFRA - ATIVIDADES</span></a></div>'


codigo = ''

ativ = ''

desc = ''

vinc = []

flux = ''
lista_flux = []

link = ''

data1 = '01/12/2021'
d = data1.replace('/', '-')
data1 = datetime.strptime(d, '%d-%m-%Y')

nome = ''

desi = ''

unid = ''

execut = ''

categ = ''

tot=''

nom = ''

stat = ''

vinc = ''

ema = ''

copia_email = ''


statu = ''

unid = 'PERCENTUAL'

tot = 100

execut = 0

categ = ''

copia_email = ''

text_alerta = ''

data2 = data1

v_alerta = ''


#**********************************************************************************************************************

#**********************************************************************************************************************

#FUNÇÕES

#**********************************************************************************************************************

#**********************************************************************************************************************

#conexão planilha

def conexao(pasta="Atividades - Estagiários",aba="Atividades"):
    """
    carrega os dados da planilha do google sheets

    """
    sheet = cliente.open(pasta).worksheet(aba)  # Open the spreadhseet
    dados = sheet.get_all_records()
    df = pd.DataFrame(dados)
    return sheet,dados,df

def proxima_linha_vazia(worksheet,coluna=1):
    str_list = list(filter(None, worksheet.col_values(coluna)))
    return str(len(str_list)+2)

def atualiza_celula(planilha,linha,col,dado):
    planilha.update_cell(linha, col, dado)
    #data = DataInicio
    #data_formatada=str(data.day) + '/' + str(data.month) + '/' + str(data.year)
    #sheet.update_cell(next_row, 7, data_formatada)

def carrega_dados(planilha,linha):
    return planilha.row_values(linha)

def envia_email(designado,assunto,conteudo,designante):
    EMAIL_ADDRESS = 'naoresponda.coinfra@gmail.com'
    EMAIL_PASSWORD = 'c@infra2021'

    #dados do e-mail
    # Create message container - the correct MIME type is multipart/alternative.
    #msg = EmailMessage()
    msg = MIMEMultipart('alternative')
    msg['Subject'] = assunto
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = designado
    msg['Cc'] = designante
    #msg.set_content(conteudo)
    msg.attach(MIMEText(conteudo,'html'))

    #envio de e-mail
    with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:
        smtp.login(EMAIL_ADDRESS,EMAIL_PASSWORD)
        smtp.send_message(msg)

def preencheBase():

    nomes=[]
    unidades=[]
    categorias=[]

    for n in df_dados.index:
        if (df_dados['Status'][n]=='Ativo'):
            nomes.append(df_dados['Nome'][n])
        #if df_dados['Unidades de Medida'][n]!='':
        unidades.append(df_dados['Unidades de Medida'][n])
        #if df_dados['Categorias'][n]!='':
        categorias.append(df_dados['Categorias'][n])

    return nomes,unidades,categorias

#**********************************************************************************************************************

#**********************************************************************************************************************

#ESTRUTURA DA PÁGINA

#**********************************************************************************************************************

#**********************************************************************************************************************

st.sidebar.title('Atividades - COINFRA')

pg=st.sidebar.radio('',['Atividades','Dados de Usuários','Dados Padrões','Acompanhamento'])

if (pg=='Atividades'):
    #conectar na planilha

    sheet, dados, df_dados = conexao(pasta="Atividades - Estagiários",aba='Dados')

    nomes,unidades,categorias=preencheBase()

    sheet, dados, df = conexao(pasta="Atividades - Estagiários",aba='Atividades')

    atividades=[df['Atividade'][n] for n in df.index]

    cod=[df['Código'][n] for n in df.index]

    #página
    st.markdown(cabecalho,unsafe_allow_html=True)
    st.subheader(pg)

    with st.expander('Selecionar atividade já cadastrada'):
        listas=[]
        indice = []
        nome_filtro = st.selectbox('Nome na atividade:',sorted(nomes))
        responsaveis = [df['Responsável'][n] for n in df.index]
        designados = [df['Designado por'][n] for n in df.index]
        stat = [df['Status'][n] for n in df.index]
        todos = st.radio('Filtro', ['Todos', 'Responsável', 'Designado por'])
        statusSelecionado = st.multiselect('Status', status_lista)

        for i in range(len(cod)):
            if (((nome_filtro == responsaveis[i]) or (nome_filtro == designados[i])) and (stat[i] in statusSelecionado) and (todos == 'Todos')):
                listas.append(cod[i] + ' - ' + atividades[i])
            elif ((nome_filtro == responsaveis[i]) and (stat[i] in statusSelecionado) and (todos == 'Responsável')):
                listas.append(cod[i] + ' - ' + atividades[i])
            elif ((nome_filtro == designados[i]) and (stat[i] in statusSelecionado) and (todos == 'Designado por')):
                listas.append(cod[i] + ' - ' + atividades[i])
            indice.append(cod[i] + ' - ' + atividades[i])
        codigo = st.selectbox('Atividade', listas)

        # if codigo == '' or codigo == None:
        #     codigo = 'A' + str(len(cod) + 1)
        #     for i in range(len(cod)):
        #         listas.append(cod[i] + ' - ' + atividades[i])
        #         indice.append(cod[i] + ' - ' + atividades[i])


    novo = ''
    #if (len(listas)>0):
    if len(listas) > 0:
        if codigo != '' and codigo != None:
            try:
                codigo = cod[indice.index(codigo)]
            except:
                print('Novo!')
                novo = 1
    if codigo != '' and codigo != None and novo=='':
        linha = cod.index(codigo) + 2
        lista = carrega_dados(sheet, linha)  # lista com dados da linha da planilha
        # print(lista)
        print(len(lista))
        if len(lista) < 25:
            j = 25 - len(lista)
            for i in range(j):
                lista.append('')
        print(len(lista))
        # extraindo
        try:
            ativ = lista[coluna['Atividade'] - 1]

            desc = lista[coluna['Descrição'] - 1]

            statu = lista[coluna['Status'] - 1]

            vinc = lista[coluna['Vinculado a Atividade'] - 1].split(';')

            flux = lista[coluna['Fluxo'] - 1]
            lista_flux = flux.split(';')

            link = lista[coluna['Link'] - 1]

            data1 = lista[coluna['Data de Entrega'] - 1]
            d = data1.replace('/', '-')
            data1 = datetime.strptime(d, '%d-%m-%Y')

            nome = lista[coluna['Responsável'] - 1]

            desi = lista[coluna['Designado por'] - 1]

            unid = lista[coluna['Unidade de Medida'] - 1]

            tot = lista[coluna['Total'] - 1]

            execut = lista[coluna['Executado'] - 1]

            categ = lista[coluna['Categoria'] - 1]

            copia_email = lista[coluna['copia_email'] - 1]

            text_alerta = lista[coluna['obs_alerta'] - 1]

            data2 = lista[coluna['data_alerta'] - 1]
            if data2 == '':
                data2 = '01/01/2023'
            d = data2.replace('/', '-')
            data2 = datetime.strptime(d, '%d-%m-%Y')

            v_alerta = lista[coluna['verif_alerta'] - 1]

        except Exception as e:
            print('Alguns dados não foram preenchidos!' + str(e))
    #dados
    dicionario={}

    with st.form(key='my_form'):
        Atividade = st.text_input('Título da Atividade',value=ativ)
        dicionario['Atividade'] = Atividade
        print(Atividade)

        Descricao = st.text_area('Descrição da atividade',value=desc)
        dicionario['Descrição'] = Descricao


        if statu == '':
            statu='A iniciar'
        if (int(execut)==int(tot)):
            statu = 'Concluído'
        with st.expander('Detalhamento de atividade'):
            Status = st.selectbox('Status', status_lista,index = status_lista.index(statu))
            dicionario['Status'] = Status

            Unidade = st.selectbox('Unidade de Medida da Atividade', unidades,index=unidades.index(unid))
            dicionario['Unidade de Medida'] = Unidade

            Executado = st.number_input('Executado', format="%i", step=1, min_value=0, value=int(execut)) #.text_input('Executado',value=execut)
            dicionario['Executado'] = Executado

            Total = st.number_input('Total', format="%i", step=1, min_value=0, value=int(tot))  # .text_input('Total',value=tot)
            dicionario['Total'] = Total

            Categoria = st.selectbox('Categoria', categorias,index=categorias.index(categ))
            dicionario['Categoria'] = Categoria

            Fluxo = st.text_area('Fluxo de Atividades (separar com ;)', value=flux)
            dicionario['Fluxo'] = Fluxo

            #verifica intersecção de listas convertendo lista em conjunto (set)
            if set(vinc).intersection(cod):
                print('atividade encontrada')
            else:
                print('atividade não encontrada')
                vinc=[]

            Vinculo = st.multiselect('Vinculado à(s) atividade',cod,default=vinc)
            dicionario['Vinculado a Atividade'] = ';'.join(Vinculo)

            Link = st.text_area('Link de arquivo/pasta (separar com ;)',value=link)
            dicionario['Link'] = Link

        DataEntrega=st.date_input('Data de Entrega [ANO/MÊS/DIA]',value=data1)
        data=DataEntrega
        data_formatada=str(data.day) + '/' + str(data.month) + '/' + str(data.year)
        dicionario['Data de Entrega'] = data_formatada
        if (nome!=''):
            Responsavel = st.selectbox('Responsável', sorted(nomes), index=sorted(nomes).index(nome))
        else:
            Responsavel = st.selectbox('Responsável', sorted(nomes))
        dicionario['Responsável'] = Responsavel
        email_responsavel=df_dados['e-mail'][nomes.index(Responsavel)]

        if desi!='':
            Designado_por = st.selectbox('Designado por', sorted(nomes),index=sorted(nomes).index(desi))
        else:
            Designado_por = st.selectbox('Designado por', sorted(nomes))
        dicionario['Designado por'] = Designado_por
        email_designante=df_dados['e-mail'][sorted(nomes).index(Designado_por)]

        aux = []
        lista_emails=[]
        for item in nomes:
            if (item in copia_email):
                aux.append(item)
                lista_emails.append(df_dados['e-mail'][sorted(nomes).index(item)])
        itens = aux

        #copia_email_enviar = st.multiselect('Informar sobre atualizações da atividade também para',nomes,itens)

        with st.expander('Criar Alerta'):
            alerta = st.text_area('Observação do alerta:',value=text_alerta)
            dicionario['obs_alerta'] = alerta
            data_alerta = st.date_input('Data do Alerta [ANO/MÊS/DIA]',value=data2)
            data = data_alerta
            data_formatada1 = str(data.day) + '/' + str(data.month) + '/' + str(data.year)
            dicionario['data_alerta'] = data_formatada1

            valores = False
            if v_alerta == 'sim':
                valor = True
            e_alerta = st.checkbox('Encaminhar e-mail somente para o responsável',value=valores)
            dicionario['v_email_alerta'] = 'não'
            if e_alerta:
                dicionario['v_email_alerta'] = 'sim'


        dicionario['e-mail'] = ''

        s=st.text_input('Senha', value="", type="password")

        col1,col2 = st.columns(2)
        botao = col1.form_submit_button('Cadastrar Novo')
        if codigo != '' and codigo!= None:
            botao_atualiza = col2.form_submit_button('Atualizar Existente')
        else:
            botao_atualiza = False
        if Total == '':
            Total = 1
        if Executado == '':
            Executado = 0

        print(botao)

        if botao==True and s=='456':
            print('chegou aqui!')
            with st.spinner('Registrando nova atividade...Aguarde!'):
                try:
                    linha=proxima_linha_vazia(sheet)
                    for chave,valor in dicionario.items():
                        atualiza_celula(sheet, linha, coluna[chave], valor)
                    st.success('Dados Cadastrados!')

                    with st.spinner('Enviando e-mails...'):
                        try:
                            # dados email
                            codigo = 'A' + str(len(cod) + 1)
                            calculo = str(round(float(Executado) / float(Total), 2) * 100)
                            titulo = 'Atividade ' + codigo + ' - ' + Atividade
                            conteudo = '<b>### ATIVIDADE ###</b>'
                            conteudo = conteudo + '<br><br>' + '<b># Atividade: </b>' + Atividade
                            conteudo = conteudo + '<br><br>' + '<b># Designado por: </b>' + Designado_por
                            conteudo = conteudo + '<br><br>' + '<b># Responsável: </b>' + Responsavel
                            conteudo = conteudo + '<br><br>' + '<b># Descrição: </b>' + Descricao
                            if (Fluxo != ""):
                                conteudo = conteudo + '<br><br>' + '<b># Fluxo de Atividades: </b><br><br> &nbsp;&nbsp;&nbsp;' + Fluxo.replace(';', '<br> &nbsp;&nbsp;')
                            if (Link != ""):
                                conteudo = conteudo + '<br><br>' + '<b># Links: </b><br>' + Link.replace(';', '<br>    ')
                            conteudo = conteudo + '<br><br>' + '<b># Data Limite Prevista: </b>' + data_formatada
                            conteudo = conteudo + '<br><br>' + '<b># Status: </b>' + Status
                            conteudo = conteudo + '<br><br>' + '<b># % Executado: </b>' + calculo + f'% [Executado: {Executado} | Total: {Total}]'
                            conteudo = conteudo + '<br><br>' + '<b># Página de Acompanhamento: </b> https://tinyurl.com/uftatividades'

                            dicionario['corpo'] = conteudo
                            atualiza_celula(sheet, linha, coluna['corpo'], dicionario['corpo'])

                            #envia_email(email_responsavel, titulo, conteudo, email_designante)
                            st.success('E-mail enviado!')
                        except Exception as e:
                            st.error('Ocorreu um erro ao enviar o e-mail! ' + str(e))
                except Exception as e:
                    st.error('Ocorreu um erro ao tentar cadastrar novos dados! ' + str(e))

        elif botao_atualiza==True and s=='456':
            with st.spinner('Atualizando dados da atividade...Aguarde!'):
                try:
                    linha=cod.index(codigo)+2
                    #linha = indice.index(codigo)+2
                    for chave,valor in dicionario.items():
                        atualiza_celula(sheet, linha, coluna[chave], valor)
                    st.success('Dados Atualizados!')

                    with st.spinner('Enviando e-mails...'):
                        try:
                            # dados email
                            calculo = str(round(float(Executado) / float(Total), 2) * 100)
                            titulo = 'Atividade ' + codigo + ' - ' + Atividade
                            conteudo = '<b>### ATIVIDADE ###</b>'
                            conteudo = conteudo + '<br><br>' + '<b># Atividade: </b>' + Atividade
                            conteudo = conteudo + '<br><br>' + '<b># Designado por: </b>' + Designado_por
                            conteudo = conteudo + '<br><br>' + '<b># Responsável: </b>' + Responsavel
                            conteudo = conteudo + '<br><br>' + '<b># Descrição: </b>' + Descricao
                            if (Fluxo!=""):
                                conteudo = conteudo + '<br><br>' + '<b># Fluxo de Atividades: </b><br><br> &nbsp;&nbsp;&nbsp;' + Fluxo.replace(';', '<br> &nbsp;&nbsp;')
                            if (Link != ""):
                                conteudo = conteudo + '<br><br>' + '<b># Links: </b><br>' + Link.replace(';', '<br>    ')
                            conteudo = conteudo + '<br><br>' + '<b># Data Limite Prevista: </b>' + data_formatada
                            conteudo = conteudo + '<br><br>' + '<b># Status: </b>' + Status
                            conteudo = conteudo + '<br><br>' + '<b># % Executado: </b>' + calculo + f'% [Executado: {Executado} | Total: {Total}]'
                            conteudo = conteudo + '<br><br>' + '<b># Página de Acompanhamento: </b> https://tinyurl.com/uftatividades'

                            dicionario['corpo'] = conteudo
                            atualiza_celula(sheet, linha, coluna['corpo'], dicionario['corpo'])

                            #envia_email(email_responsavel, titulo, conteudo, email_designante)
                            st.success('E-mail enviado!')
                        except Exception as e:
                            st.error('Ocorreu um erro ao enviar o e-mail! ' + str(e))
                except Exception as e:
                    st.error('Ocorreu um erro ao tentar atualizar os dados! ' + str(e))
        elif (botao==True or botao_atualiza==True) and s!='456':
            st.error('Senha incorreta!')

elif (pg=='Dados de Usuários'):
    #conectar na planilha
    sheet, dados, df = conexao(pasta="Atividades - Estagiários",aba='Dados')

    nomes = [df['Nome'][n] for n in df.index]
    cod = [df['cod'][n] for n in df.index]

    #página
    st.markdown(cabecalho,unsafe_allow_html=True)
    st.subheader(pg)

    with st.expander('Selecionar usuário já cadastrado'):

        cadastrado=st.selectbox('Usuários',nomes)

        codigo=cod[nomes.index(cadastrado)]

        if codigo!='':
            linha=cod.index(codigo)+2
            lista=carrega_dados(sheet,linha) #lista com dados da linha da planilha
            print(lista)
            #extraindo
            try:
                nom=lista[coluna_dados['Nome']-1]

                stat=lista[coluna_dados['Status']-1]

                vinc = lista[coluna_dados['Vínculo'] - 1]

                data1 = lista[coluna_dados['Data de Finalização'] - 1]
                if (data1==''):
                    data1='31/12/2023'
                d = data1.replace('/', '-')
                data1 = datetime.strptime(d, '%d-%m-%Y')

                ema=lista[coluna_dados['e-mail'] - 1]

            except:
                print('erro')

    dicionario = {}
    with st.form(key='usuarios'):
        Nome = st.text_input('Nome',value=nom)
        dicionario['Nome'] = Nome

        Status = st.selectbox('Status',['Ativo','Não Ativo'],index=['Ativo','Não Ativo'].index(stat))
        dicionario['Status'] = Status

        # Fluxo = st.text_area('Descrição do executado', value=Descricao)
        Vinculo = st.selectbox('Vínculo', ['Estagiário','Servidor'], index=['Estagiário','Servidor'].index(vinc))
        dicionario['Vínculo'] = Vinculo

        DataFinalizacao = st.date_input('Data de Finalização (se Estágio)',value=data1)
        data = DataFinalizacao
        data_formatada = str(data.day) + '/' + str(data.month) + '/' + str(data.year)
        dicionario['Data de Finalização'] = data_formatada

        Email = st.text_input('E-mail',value=ema)
        dicionario['e-mail'] = Email.strip()

        s=st.text_input('Senha', value="", type="password")

        col11,col22 = st.columns(2)
        botao1 = col11.form_submit_button('Cadastrar Novo')
        botao_atualiza1 = col22.form_submit_button('Atualizar Existente')

        if botao1 == True and s == '456':
            with st.spinner('Cadastrando dados de usuário...Aguarde!'):
                try:
                    linha = proxima_linha_vazia(sheet)
                    for chave, valor in dicionario.items():
                        atualiza_celula(sheet, linha, coluna_dados[chave], valor)
                    st.success('Dados Cadastrados!')
                except:
                    st.error('Erro ao cadastrar dados!')
        elif botao_atualiza1==True and s=='456':
            with st.spinner('Atualizando dados de usuário...Aguarde!'):
                try:
                    linha=cod.index(codigo)+2
                    for chave,valor in dicionario.items():
                        atualiza_celula(sheet, linha, coluna_dados[chave], valor)
                    st.success('Dados Atualizados!')
                except:
                    st.error('Ocorreu um erro ao tentar atualizar os dados!')
elif (pg=='Dados Padrões'):
    #conectar na planilha
    sheet, dados, df = conexao(pasta="Atividades - Estagiários",aba='Dados')

    unidades = [df['Unidades de Medida'][n] for n in df.index]
    categorias = [df['Categorias'][n] for n in df.index]

    #página
    st.markdown(cabecalho,unsafe_allow_html=True)
    st.subheader(pg)

    with st.form(key='usuarios'):

        s = st.text_input('Senha', value="", type="password")

        dicionario = {}
        with st.expander('Unidades de Medida'):
            Unidade = st.selectbox('Unidades de Medida cadastradas', unidades)
            unid = st.text_input('Unidade de Medida',value=Unidade)
            dicionario['Unidades de Medida']=unid
            col1, col2 = st.columns(2)
            bot1 = col1.form_submit_button('Cadastrar Novo')
            bot2 = col2.form_submit_button('Atualizar Existente')

        with st.expander('Categorias'):
            Categoria = st.selectbox('Categorias cadastradas', categorias)
            categ = st.text_input('Categoria',value=Categoria)
            dicionario['Categorias']=categ
            col11, col22 = st.columns(2)
            bot11 = col11.form_submit_button('Cadastrar Novo_')
            bot22 = col22.form_submit_button('Atualizar Existente_')

        bot=st.form_submit_button('')
        if bot1 == True and s == '456':
            del dicionario['Categorias']
            with st.spinner('Cadastrando dados...Aguarde!'):
                try:
                    linha = str(int(proxima_linha_vazia(sheet,10))-1)

                    for chave, valor in dicionario.items():
                        atualiza_celula(sheet, linha, coluna_dados[chave], valor)
                    st.success('Dados Cadastrados!')
                except:
                    st.error('Erro ao cadastrar dados!')
        elif bot2==True and s=='456':
            del dicionario['Categorias']
            with st.spinner('Atualizando dados...Aguarde!'):
                try:
                    linha=unidades.index(Unidade)+2
                    for chave,valor in dicionario.items():
                        atualiza_celula(sheet, linha, coluna_dados[chave], valor)
                    st.success('Dados Atualizados!')
                except:
                    st.error('Ocorreu um erro ao tentar atualizar os dados!')
        elif bot11 == True and s == '456':
            del dicionario['Unidades de Medida']
            with st.spinner('Cadastrando dados...Aguarde!'):
                try:
                    linha = str(int(proxima_linha_vazia(sheet,11))-1)
                    for chave, valor in dicionario.items():
                        atualiza_celula(sheet, linha, coluna_dados[chave], valor)
                    st.success('Dados Cadastrados!')
                except:
                    st.error('Erro ao cadastrar dados!')
        elif bot22==True and s=='456':
            del dicionario['Unidades de Medida']
            with st.spinner('Atualizando dados...Aguarde!'):
                try:
                    linha=categorias.index(Categoria)+2
                    for chave,valor in dicionario.items():
                        atualiza_celula(sheet, linha, coluna_dados[chave], valor)
                    st.success('Dados Atualizados!')
                except:
                    st.error('Ocorreu um erro ao tentar atualizar os dados!')
elif (pg=='Acompanhamento'):

    #página
    st.markdown(cabecalho,unsafe_allow_html=True)
    st.subheader(pg)

    #conectar na planilha
    sheet, dados, df = conexao(pasta="Atividades - Estagiários",aba='Dados')
    #nomes = [df['Nome'][n] for n in df.index]
    sheet, dados, df_dados = conexao(pasta="Atividades - Estagiários",aba='Dados')

    nomes, unidades, categorias = preencheBase()

    sheet, dados, df = conexao(pasta="Atividades - Estagiários", aba='Atividades')
    cod = [df['Código'][n] for n in df.index]
    ativ = [df['Atividade'][n] for n in df.index]
    tot = [df['Total'][n] for n in df.index]
    execut = [df['Executado'][n] for n in df.index]
    data_entrega = [df['Data de Entrega'][n] for n in df.index]
    stat = [df['Status'][n] for n in df.index]
    datas = [df['mes_ano'][n] for n in df.index]

    mes_ano = list(set(datas))
    mes_ano.append('Todos')

    status_prov=status_lista
    status_prov.append('Todos')

    listas = []
    nome_filtro = st.selectbox('Nome na atividade:', sorted(nomes))
    responsaveis = [df['Responsável'][n] for n in df.index]
    designados = [df['Designado por'][n] for n in df.index]
    todos = st.radio('Filtro',['Todos','Responsável','Designado por'])
    statusSelecionado = st.multiselect('Status',status_prov)
    #print(statusSelecionado)
    data_sel = st.selectbox('Mês/Ano de entrega',sorted(mes_ano))
    col=[]
    n=0
    for i in range(len(cod)):
        if (((nome_filtro == responsaveis[i]) or (nome_filtro == designados[i])) and (stat[i] in statusSelecionado or statusSelecionado==['Todos']) and (todos == 'Todos') and (datas[i] in data_sel or data_sel=='Todos')):
            col.append('')
            col.append('')
            col[n],col[n+1] = st.columns(2)
            col[n] = st.text(cod[i] + '-' + ativ[i] + ' [' + data_entrega[i] + ']')
            print(tot[i])
            print(execut[i])
            calculo = int(execut[i])/int(tot[i])
            col[n+1] = st.progress(calculo)
            n += 1
        elif ((nome_filtro == responsaveis[i]) and (stat[i] in statusSelecionado or statusSelecionado==['Todos']) and (todos == 'Responsável') and (datas[i] in data_sel or data_sel=='Todos')):
            col.append('')
            col.append('')
            col[n],col[n+1] = st.columns(2)
            col[n] = st.text(cod[i] + '-' + ativ[i] + ' [' + data_entrega[i] + ']')
            print(tot[i])
            print(execut[i])
            calculo = int(execut[i])/int(tot[i])
            col[n+1] = st.progress(calculo)
            n += 1
        elif ((nome_filtro == designados[i]) and (stat[i] in statusSelecionado or statusSelecionado==['Todos']) and (todos == 'Designado por') and (datas[i] in data_sel or data_sel=='Todos')):
            col.append('')
            col.append('')
            col[n],col[n+1] = st.columns(2)
            col[n] = st.text(cod[i] + '-' + ativ[i] + ' [' + data_entrega[i] + ']')
            print(tot[i])
            print(execut[i])
            calculo = int(execut[i])/int(tot[i])
            col[n+1] = st.progress(calculo)
            n += 1
