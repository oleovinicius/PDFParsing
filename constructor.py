import tabula
import pandas as pd


def file_extract(PATH):
    #declare the path of your file
    file_path = PATH
    #Convert your file
    df = tabula.read_pdf(file_path, pages='all',multiple_tables=True)
    return df

def df_construct(df):
    dfFinal = pd.DataFrame( columns= ['ra', 'nome_aluno','data_nascimento','rg_aluno','cpf_aluno','curso','periodo','expCarteirinha','valCarteirinha','faculdade','rua','telefone','',''])
    for i in range(len(df)):
        ##CORREÇÕES##
        ra_error = df[i].iloc[8][0]
        ra_error = [ra_error.split()]
        ra= ra_error[0][1]
        erro7 = df[i].loc[7][0] # periodo ra tg palavra cpf
        erro7 = [erro7.split()]
        expedicao = df[i].loc[9][0]
        expedicao = [expedicao.split()]
        curso = curso = df[i].loc[5][0] +  df[i].loc[6][0]
        faculdade = nome_faculdade = df[i].loc[0][0] + df[i].loc[2][0]

        ############## construção Banco #############
        #Dados Aluno
        ra = ra # ra do aluno nome data nascimento
        nome_aluno = df[i].loc[4][0] # Nome do Aluno
        data_nascimento = df[i].loc[8][1] # data de nascimento real
        rg_aluno = erro7[0][3] #RG Real
        cpf_aluno= df[i].loc[7][1] # cpf completo
        #Dados Curso
        curso = df[i].loc[5][0] # Curso completo
        periodo= erro7[0][2] # Periodo real
        #Dados Carteirinha
        expCarteirinha = expedicao[0][1] # expedição carteirinha
        valCarteirinha = df[i].loc[9][1] # validade da carteirinha
        #Dados Fatec
        faculdade # Nome da faculdade 
        rua = "RUA ARIOVALDO SILVEIRA FRANCO, 567 - JD 31 DE MARÇO" # rua da faculdade
        cep = "CEP: 13801-005 - Mogi Mirim/SP" # cep e cidade faculdade
        telefone = "Tel: 19 3806-3139" # telefone faculdade
        listaAluno = [(ra, nome_aluno,data_nascimento,rg_aluno,cpf_aluno,curso,periodo,expCarteirinha,valCarteirinha,faculdade,rua,telefone,'','')]
        dfNovoAluno = pd.DataFrame(listaAluno, columns=['ra', 'nome_aluno','data_nascimento','rg_aluno','cpf_aluno','curso','periodo','expCarteirinha','valCarteirinha','faculdade','rua','telefone','',''])
        dfFinal = pd.concat([dfFinal,dfNovoAluno],ignore_index=True)
    return dfFinal


def execution(PATH):
    dfReceive = file_extract(PATH)
    database = df_construct(dfReceive) 