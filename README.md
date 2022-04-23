# ParsingPDF

## 1. Introdução
O programa **ParsingPDF** desenvolvido por **LVS** tem o propósito de fazer a conversão de arquivos PDF gerados pela Fatec para um banco de dados utilizável. Essa necessidade surgiu quando ofereceram uma proposta ao meu grupo de TCC. A proposta é de criar uma carteirinha virtual para rodar um aplicativo no sistema Android e iOS, mas tínhamos essa limitação, não podíamos ter acesso ao BD do CTPS, apenas a um pdf com os dados.
Este programa possui 4 subprogramas principais:

    1. imageExtractor: Serve para extrair a foto do aluno e o qr code.
    2. constructor: Serve para extrair os dados escritos e criar um DataFrame com eles e as fotos.
    3. banco: Serve para fazer a conexão com o banco de dados, criar a tabela e fazer a inserção deles.
    4. app: Parte visual, responsável por executar as demais e excluir as pastas fotos e qrcode ao fim da execução

## 2. Instalação

Para a instalação você vai precisar do python3 instalado e de algumas dependências.
Clone ou baixe esse repositório, e depois na pasta principal do projeto abra um terminal de sua preferência e digite o comando:
```
pip install -r requirements.txt
```
ou apenas execute o **installDependences.bat** se estiver no _Windows_.

## 3. Execução

Agora se estiver no _Windows_ só execute **ParsingPDF.bat**, agora se for rodar por algum terminal use:
```
python app.py
```


### Created By: LVS
