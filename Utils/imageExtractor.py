#IMPORTS
import fitz
import os
from PIL import Image
import shutil
import cv2

"""
Classe: extratorImagens(path) -> Serve para extrair a foto e qr code dos alunos
Metodos: 
    imageGenerator(self) -> Gera todas as imagens contidas em um PDF
        -> Precisa do caminho path definido ao criar a classe
    ImageDir(self) -> pega os caminhos(Paths) de todas as imagens .png
        -> Não precisa de atributos adicionais
        -> Salva o resultado em self.pathsImage
    unusableImgClean(self) -> Exclui as imagens que não são a foto nem o qr code, apagando todas com o Height e Width maior que elas
        -> Precisa do self.pathsImage para saber aonde estão as imagens
        -> Necessario usar o ImageDir(self) antes
    photosandqr() -> Separa as fotos e qr codes cada um em uma pasta
        -> Precisa do self.pathsImage para saber aonde estão as imagens
        -> Necessario usar o ImageDir(self) antes

"""


class extratorImagens:
    def __init__(self, path):
        self.path = path
        self.pathsImage = None
        print(self.path)
        
        
    
    # Gera a imagem do pdf
    def imageGenerator(self):
        doc = fitz.open(self.path)
        for i in range(len(doc)):
            for img in doc.getPageImageList(i):
                xref = img[0]
                pix = fitz.Pixmap(doc, xref)
                if pix.n < 5:       # this is GRAY or RGB
                    pix.writePNG("%s.png" % (xref))
                else:               # CMYK: convert to RGB first
                    pix1 = fitz.Pixmap(fitz.csRGB, pix)
                    pix1.writePNG("%s.png" % (xref))
                    pix1 = None
                pix = None

    # Retorna o caminho das imagens
    def ImageDir(self):
        import os
        cwd = os.getcwd()
        paths = []
        print(cwd)
        for root, dirs, files in os.walk(cwd):
            for file in files:
                if file.endswith(".png"):
                    caminho = os.path.join(root, file)
                    print('caminho:',caminho)
                    paths.append(os.path.join(root, file))
        self.pathsImage= paths


    # Limpa as imagens que não são a Foto e o QrCode
    def unusableImgClean(self):
        filesToExpurgue = self.pathsImage
        path_dimension_height = []
        path_dimension_width = []
        test = []

        for i in range(len(filesToExpurgue)):
            # read image
            img = cv2.imread(filesToExpurgue[i])
            test.append(filesToExpurgue[i])

            # get dimensions of image
            dimensions = img.shape

            # height, width, number of channels in image
            height = img.shape[0]
            width = img.shape[1]
            channels = img.shape[2]

            if height > 226 or width >226:
                os.remove(filesToExpurgue[i]) 

    # Obtem o tamanho das imagens para separar foto de QrCode
    def getImageSize(self,image):
        im = Image.open(image)
        h, w = im.height, im.width
        im.close()
        result = h * w
        return result

    # Faz a mensuração pra separar os dois tipos de arquivos
    # Separa cada um em sua pasta
    def photosandqr(self):
        if os.path.isdir("foto"):
            print("Diretorio foto existe")
        else:
            print("Diretorio foto não existe ainda")
            os.mkdir('./foto')

        if os.path.isdir("qrcode"):
            print("Diretorio qrcode existe")
        else:
            print("Diretorio qrcode não existe ainda")
            os.mkdir('./qrcode')
        
        files = self.pathsImage
        tipos = []
        for i in range(len(files)):
            tipos.append(self.getImageSize(files[i]))
        
        cwd = os.getcwd()
        for i in range(len(tipos)):
            if tipos[i] == 14400:
                destination = cwd + "\\foto"
                shutil.move(files[i], destination)
            elif tipos[i] == 51076 :
                destination = cwd + "\\qrcode"
                shutil.move(files[i], destination)

def main():
    #Definindo Caminho
    #Criando classe
    path= r"C:\Users\Leo\Documents\code\parsiingpdftomysql\pdftoparsing.pdf"
    execution = extratorImagens(path)
    print("Gerando as Imagens")
    execution.imageGenerator()
    print("Pegando os caminhos")
    execution.ImageDir()
    print("Limpando o lixo")
    execution.unusableImgClean()
    print("Pegando o caminho de novo para separar as imagens")
    execution.ImageDir()
    print("separando as imagens")
    execution.photosandqr()
    

