import Utils.imageExtractor as imageExtractor
import Utils.constructor as constructor
import Utils.banco as banco
from PySimpleGUI import PySimpleGUI as sg
import shutil
import os

class teladoprogrma:
    def __init__(self):
        self.window = None
        self.pathPdf = None
        self.server = None
        self.database = None
        self.username = None
        self.password = None
        self.dataframe = None
        self.bdinstance = None


    def addlog(self, string):
        self.window['mylog'].update(string+'\n', append=True)

    def rodandoprograma(self):
         # Passo 1: Extração das imagens do pdf
        print("Iniciando a extração de imagens")
        self.addlog("Iniciando a extração de imagens")
        execution = imageExtractor.extratorImagens(self.pathPdf)
        print("Gerando as Imagens")
        self.addlog("Gerando as imagens")
        execution.imageGenerator()
        print("Pegando os caminhos")
        self.addlog("Pegando os caminhos")
        execution.ImageDir()
        print("Limpando o lixo")
        self.addlog("Limpando o lixo")
        execution.unusableImgClean()
        print("Pegando o caminho de novo para separar as imagens")
        self.addlog("Pegando o caminho de novo para separar as imagens")
        execution.ImageDir()
        print("separando as imagens")
        self.addlog("separando as imagens")
        execution.photosandqr()
        print("Finalizando o extrator de imagens")
        self.addlog("Finalizando o extrator de imagens")
        # Passo 2: Extração das informações do pdf para um Pandas DataFrame
        executor = constructor.constructorTables(self.pathPdf)
        print('Extrair Dados do PDF')
        self.addlog("Extrair Dados do PDF")
        executor.file_extract()
        print('Montando o DataFrame')
        self.addlog("Montando o DataFrame")
        executor.df_construct()
        print('Pegando as fotos')
        self.addlog("Pegando as fotos")
        executor.ImageDirFoto()
        print('Convertendo as fotos para base64')
        self.addlog("Convertendo as fotos para base64")
        executor.convertendoImagemBase64() 
        print('Adicionando as fotos base64 ao DF')
        self.addlog("Adicionando as fotos base64 ao DF")
        executor.adicionandoImagemBase64aoDFFoto()
        print('Pegando o caminho dos QRcode')
        self.addlog("Pegando o caminho dos QRcode")
        executor.ImageDirQrcode()
        print('Convertendo os QRcode para base64')
        self.addlog("Convertendo os QRcode para base64")
        executor.convertendoImagemBase64()
        print('Adicionando QR code de base64 ao DF')
        self.addlog("Adicionando QR code de base64 ao DF") 
        executor.adicionandoImagemBase64aoDFQrcode()
        self.dataframe = executor.dataframe
    
    def bdConexao(self):
         # Passo 3: conexão com banco de dados
         # https://www.youtube.com/watch?v=U8T16HpcS5E
        self.addlog("Criando instancia banco") 
        self.bdinstance = banco.conexaoBancodeDados(self.server,self.database,self.username,self.password,self.dataframe)
        self.addlog("Conectando ao banco") 
        self.bdinstance.conectandoaoBD()
        
    def bdCriarTabela(self):
        self.addlog("Criando tabelas banco") 
        self.bdinstance.criandoTabelaAlunos()

    def bdInserir(self):
        self.addlog("Inserindo DF ao banco de dados") 
        self.bdinstance.inserindoDF()

    def deleteDir(self):
        cwd = os.getcwd() + "\\foto"
        shutil.rmtree(cwd)
        cwd = os.getcwd() + "\\qrcode"
        shutil.rmtree(cwd)
        

    def criacaoTela(self):
        # Tema
        sg.theme('Reddit')
        # Layout do programa
        layout =[   [sg.Text('Path PDF:'), sg.Input(key='pathpdf'),sg.FileBrowse(key='selecionar_path')],
                    [sg.Text('Server SQL:'), sg.Input(key='serversql')],
                    [sg.Text('Database:'), sg.Input(key='database')],
                    [sg.Text('Username:'), sg.Input(key='usuario')],
                    [sg.Text('Password:'), sg.Input(key='senha', password_char='*')],
                    [sg.Text('Log:')],
                    [sg.Multiline(size=(70,10),autoscroll=True,key='mylog')],
                    [
                    #sg.Button('Conferir',key='conferir'),
                    sg.Button('Executar',key='execute'),
                    sg.Button('Conectar BD',key='bd'),
                    sg.Button('Criar Tabela',key='bdcreate'),
                    sg.Button('Inserir',key='bdinserir')]
                    ]
        # Janela
        self.window = sg.Window('Tela de Login',layout)

    def rodandoTela(self):
        # Ler os eventos
        while True:
            

            event, values = self.window.read()
            if event == sg.WIN_CLOSED:
                break
            # if event == 'conferir':
            #     sg.popup('pathpdf',
            #                 values['pathpdf'],
            #                 'serversql', 
            #                 values['serversql'],
            #                 'database',  
            #                 values['database'],
            #                 'usuario',
            #                 values['usuario'],
            #                 'password',
            #                 values['senha'])
                

            if event == 'execute':
                self.pathPdf = values['pathpdf']
                self.server = values['serversql']
                self.database = values['database']
                self.username = values['usuario']
                self.password = values['senha']
                try:
                    self.rodandoprograma()
                    sg.popup('Comcluido')
                    print(self.dataframe)
                except:
                    sg.popup('Erro ao executar')
            
            if event == 'bd':
                self.pathPdf = values['pathpdf']
                self.server = values['serversql']
                self.database = values['database']
                self.username = values['usuario']
                self.password = values['senha']
                try:
                    self.bdConexao()
                    sg.popup('Conectado')
                except(RuntimeError, TypeError, NameError):
                    sg.popup('Erro banco de dados',
                    'runtime error:',RuntimeError,
                    'TypeError:',TypeError,
                     'Name Error:',NameError )
                     
            if event == 'bdcreate':
                self.pathPdf = values['pathpdf']
                self.server = values['serversql']
                self.database = values['database']
                self.username = values['usuario']
                self.password = values['senha']
                try:
                    self.bdCriarTabela()
                except(RuntimeError, TypeError, NameError):
                    sg.popup('Erro banco de dados',
                    'runtime error:',RuntimeError,
                    'TypeError:',TypeError,
                     'Name Error:',NameError )

            if event == 'bdinserir':  
                self.pathPdf = values['pathpdf']
                self.server = values['serversql']
                self.database = values['database']
                self.username = values['usuario']
                self.password = values['senha']
                try:
                    sg.popup('inserido')
                    self.bdInserir()
                    self.deleteDir()
                    sg.popup('Tudo limpo e pronto')
                except(RuntimeError, TypeError, NameError):
                    sg.popup('Erro banco de dados',
                    'runtime error:',RuntimeError,
                    'TypeError:',TypeError,
                     'Name Error:',NameError )
        self.window.close()



janela = teladoprogrma()
janela.criacaoTela()
janela.rodandoTela()