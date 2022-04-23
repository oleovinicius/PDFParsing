import tabula
import pandas as pd
from natsort import natsorted
import PIL
import PIL.Image
import base64
from PIL import Image
from io import BytesIO

"""
Classe:
    constructorTables -> serve para construir a tabela dos alunos apartir de um pdf
                      -> Precisa do caminho do pdf
Metodos:
def file_extract(self) -> extrai todos os dados do pdf
                       -> Precisa do caminho do pdf
def df_construct(self) -> Monta o Pandas Data Frame e corrige erros de leitura
                       -> Precisa de um df com as informações do def file_extract(self)
"""


class constructorTables:
    def __init__(self, path):
        self.path = path
        self.dataframe = None
        self.paths = None
        self.imagensbase64 = None

    def file_extract(self):
        #declare the path of your file
        file_path = self.path
        #Convert your file
        df = tabula.read_pdf(file_path, pages='all',multiple_tables=True)
        self.dataframe = df

    def df_construct(self):
        df = self.dataframe
        dfFinal = pd.DataFrame( columns= ['ra', 'nome_aluno','data_nascimento','rg_aluno','cpf_aluno','curso','periodo','expCarteirinha','valCarteirinha','faculdade','rua','telefone','foto','qrcode'])
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
            dfNovoAluno = pd.DataFrame(listaAluno, columns=['ra', 'nome_aluno','data_nascimento','rg_aluno','cpf_aluno','curso','periodo','expCarteirinha','valCarteirinha','faculdade','rua','telefone','foto','qrcode'])
            dfFinal = pd.concat([dfFinal,dfNovoAluno],ignore_index=True)
        self.dataframe = dfFinal

    def ImageDirFoto(self):
        import os
        cwd = os.getcwd() + "\\foto"
        paths = []
        for root, dirs, files in os.walk(cwd):
            for file in files:
                if file.endswith(".png"):
                    paths.append(os.path.join(root, file))
        paths = natsorted(paths)
        self.paths = paths

    def ImageDirQrcode(self):
        import os
        cwd = os.getcwd() + "\\qrcode"
        paths = []
        for root, dirs, files in os.walk(cwd):
            for file in files:
                if file.endswith(".png"):
                    paths.append(os.path.join(root, file))
        paths = natsorted(paths)
        self.paths = paths

    def convertendoImagemBase64(self):
        self.imagensbase64 = []
        for i in range(len(self.paths)):
            with open(self.paths[i] , "rb") as image_file:
                self.imagensbase64.append(base64.b64encode(image_file.read()))
    
    def adicionandoImagemBase64aoDFFoto(self):
        for i in range(len(self.imagensbase64)):
            self.dataframe.iloc[i, 12] = self.imagensbase64[i]

    def adicionandoImagemBase64aoDFQrcode(self):
        for i in range(len(self.imagensbase64)):
            self.dataframe.iloc[i, 13] = self.imagensbase64[i]


def main():
    path= r"C:\Users\Leo\Documents\code\parsiingpdftomysql\pdftoparsing.pdf"
    executor = constructorTables(path)
    #Extrair Dados do PDF
    executor.file_extract()
    # Montar o DF
    executor.df_construct()
    
    executor.ImageDirFoto()
    executor.convertendoImagemBase64() 
    executor.adicionandoImagemBase64aoDFFoto()
    
    executor.ImageDirQrcode()
    executor.convertendoImagemBase64() 
    executor.adicionandoImagemBase64aoDFQrcode()
    

    print(executor.dataframe)
