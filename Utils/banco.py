import pyodbc

class conexaoBancodeDados:
    def __init__(self,server,database,username,passwod,df):
        self.server = server
        self.database = database
        self.username = username
        self.password = passwod
        self.conexao = None
        self.cursor = None
        self.dataframe = df

    def conectandoaoBD(self):
        self.conexao = pyodbc.connect(driver='{SQL Server}', host=self.server, database=self.database,
                             user=self.username, password=self.password, Trusted_Connection='no')
                            
        self.cursor = self.conexao.cursor()
        
    def criandoTabelaAlunos(self):
        self.cursor.execute("""
        CREATE TABLE Alunos (
        ra varchar(255) PRIMARY KEY, 
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
        foto varbinary(MAX),
        qrcode varbinary(MAX));
        """)
        self.conexao.commit()

    def inserindoDF(self):
        for i in range(len(self.dataframe)):
            self.cursor.execute("INSERT INTO Alunos (ra, nome_aluno, data_nascimento, rg_aluno, cpf_aluno, curso, periodo, expCarteirinha, valCarteirinha, faculdade, rua, telefone, foto, qrcode) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?)", self.dataframe.iloc[i,0],self.dataframe.iloc[i,1],self.dataframe.iloc[i,2],self.dataframe.iloc[i,3],self.dataframe.iloc[i,4],self.dataframe.iloc[i,5],self.dataframe.iloc[i,6],self.dataframe.iloc[i,7],self.dataframe.iloc[i,8],self.dataframe.iloc[i,9],self.dataframe.iloc[i,10],self.dataframe.iloc[i,11],self.dataframe.iloc[i,12],self.dataframe.iloc[i,13])
        self.conexao.commit()