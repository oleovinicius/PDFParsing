import mysql.connector

class conexaoBancodeDados:
    def __init__(self,server,username,passwod,df):
        self.server = server
        self.username = username
        self.password = passwod
        self.conexao = None
        self.cursor = None
        self.dataframe = df

    def conectandoaoBD(self):
        self.conexao= mysql.connector.connect(
            host=self.server,
            user=self.username,
            password=self.password)
        self.cursor = self.conexao.cursor()
        
    def createDb(self):
        var = """CREATE DATABASE FatecMM2020"""
        self.cursor.execute(var)

    def useDB(self):
        var = """USE FatecMM2020"""
        self.cursor.execute(var)

    def criandoTabelaAlunos(self):
        self.cursor.execute("""
        CREATE TABLE Alunos (
        ra varchar(255) PRIMARY KEY,
	senha varchar(255), 
        nome_aluno varchar(255),
        data_nascimento varchar(255),
        rg_aluno varchar(255),
        cpf_aluno varchar(255),
        curso varchar(255),
        periodo varchar(255),
        expCarteirinha varchar(255),
        valCarteirinha varchar(255),
        faculdade varchar(255),
        rua varchar(255),
        telefone varchar(255),
        foto varbinary(20000),
        qrcode varbinary(20000));
        """)
        self.conexao.commit()

    def inserindoDF(self):
        for i in range(len(self.dataframe)):
            sql = "INSERT INTO Alunos (ra, nome_aluno, data_nascimento, rg_aluno, cpf_aluno, curso, periodo, expCarteirinha, valCarteirinha, faculdade, rua, telefone, foto, qrcode) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            val = (self.dataframe.iloc[i,0],self.dataframe.iloc[i,1],self.dataframe.iloc[i,2],self.dataframe.iloc[i,3],self.dataframe.iloc[i,4],self.dataframe.iloc[i,5],self.dataframe.iloc[i,6],self.dataframe.iloc[i,7],self.dataframe.iloc[i,8],self.dataframe.iloc[i,9],self.dataframe.iloc[i,10],self.dataframe.iloc[i,11],self.dataframe.iloc[i,12],self.dataframe.iloc[i,13])
            self.cursor.execute(sql,val)
        self.conexao.commit()