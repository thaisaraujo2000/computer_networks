# importacao das bibliotecas
from socket import *

# definicao das variaveis
serverName = '127.0.0.3' # ip do servidor
serverPort = 65000 # porta a se conectar
clientSocket = socket(AF_INET,SOCK_STREAM) # criacao do socket TCP
clientSocket.connect((serverName, serverPort)) # conecta o socket ao servidor

sentence = input('Digite o texto em letras minusculas: ')
clientSocket.send(sentence.encode('utf-8')) # envia o texto para o servidor
modifiedSentence = clientSocket.recv(1024) # recebe do servidor a resposta
messageOK = modifiedSentence.decode('utf-8')
print (f'O servidor ({serverName}, {serverPort}) respondeu com: {messageOK}')
clientSocket.close() # encerramento o socket do cliente