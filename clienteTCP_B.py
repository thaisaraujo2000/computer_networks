from socket import *

serverName = 'localhost'
serverPort = 50000
clientSocket = socket(AF_INET,SOCK_STREAM) #tipo e serviço que o socket está operando (stream) 
clientSocket.connect((serverName,serverPort))

sentence = input('Comando: ')
clientSocket.send(sentence.encode('utf-8')) #envia o texto para o servidor
modifiedSentence = clientSocket.recv(1026) #recebe do servidor a resposta
print ('O servidor (\'%s\', %d) respondeu com: %s' % (serverName, serverPort, modifiedSentence.decode('utf-8')))
clientSocket.close()