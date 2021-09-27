from socket import *
import subprocess

serverName = ''
serverPort = 50000 #1024-65535
serverSocket = socket(AF_INET,SOCK_STREAM) #tipo e serviço que o socket está operando(stream) 
serverSocket.bind((serverName,serverPort)) #porta e ip associado(ip em branco)
serverSocket.listen(1) #modo escuta 'listen'
print ('Servidor TCP esperando conexoes na porta %d ...' %(serverPort))
while 1:
    connectionSocket, addr = serverSocket.accept() #dentro de um laço para aceitar várias conecções. endereço de memória e ip e porta
    sentence = connectionSocket.recv(1026) #recebimento
    sentence = sentence.decode('utf-8')
    try:
        capitalizedSentence = subprocess.check_output(sentence, shell=True, universal_newlines=True, stderr=subprocess.STDOUT)
    except:
        capitalizedSentence = 'comando invalido'
    print ('Cliente %s enviou: %s e recebeu: %s' %(addr, sentence, capitalizedSentence))
    connectionSocket.send(capitalizedSentence.encode('utf-8')) #envio
    connectionSocket.close() #encerra o socket com o cliente

serverSocket.close() #encerra o socket com o servidor