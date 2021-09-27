from pyModbusTCP.server import ModbusServer, DataBank
from time import sleep

# Criando conexão TCP na solicitação de requisição do modbus
server = ModbusServer("", 502, no_block=True)

try:
    print("Iniciando servidor")
    server.start()
    print("Inicialização feita com suceso")

    #Inicializar todas as suas palavras e bits em 0 em uma classe de dados
    state = [0]
    for i in range(7):
        DataBank.set_words(i,[0])
        state = DataBank.get_words(i)
        print(f'O valor do registrador {i} agora é ' + str(state))

    #Mapeando as variáveis:
        # B1 = 0
        # B2 = 1
        # NIVEL = 2
        # S1 = 3
        # S2 = 4
        # VAZAO1 = 5
        # VAZAO2 = 6

    #OBS.: funcionamento: capacidade máxima = 100L  

    #Enquanto estiver funcionando, mostrar a atualização dos valores
    while True:
        b1 = DataBank.get_bits(0)
        b2 = DataBank.get_bits(1)
        nivel = DataBank.get_words(2)
        s1 = DataBank.get_bits(3)
        s2 = DataBank.get_bits(4)
        vazao1 = DataBank.get_words(5)
        vazao2 = DataBank.get_words(6)

        print(f"b1 = {b1} b2 = {b2} nivel = {nivel} s1 = {s1} s2 = {s2} vazao1 = {vazao1} vazao2 = {vazao2}")

        #Caso a bomba 1 esteja ligada e a bomba 2 não esteja ligada
        if str(b1) == "[True]" and str(b2) == "[False]":

            tam_nivel = len(str(nivel))
            tam_vazao1 = len(str(vazao1))
            
            nivel = str(nivel)
            vazao1 = str(vazao1)

            nivelok = nivel[1:tam_nivel-1]
            nivelok = float(nivelok)
            vazao1ok = vazao1[1:tam_vazao1-1]
            vazao1ok = float(vazao1ok)

            print(f"nivel = {nivelok}")
            if nivelok+vazao1ok <= 100:
                DataBank.set_words(2, [nivelok+vazao1ok])
        
        #Caso a bomba 1 não esteja ligada e a bomba 2 esteja ligada
        if str(b1) == "[False]" and str(b2) == "[True]":
            tam_nivel = len(str(nivel))
            tam_vazao2 = len(str(vazao2))
            
            nivel = str(nivel)
            vazao2 = str(vazao2)

            nivelok = nivel[1:tam_nivel-1]
            nivelok = int(nivelok)
            vazao2ok = vazao2[1:tam_vazao2-1]
            vazao2ok = int(vazao2ok)
            if nivelok-vazao2ok >= 0:
                DataBank.set_words(2, [nivelok-vazao2ok])
        
        #Caso as 2 bombas estejam ligadas
        if str(b1) == "[True]" and str(b2) == "[True]":
            tam_nivel = len(str(nivel))
            tam_vazao1 = len(str(vazao1))
            tam_vazao2 = len(str(vazao2))
            
            nivel = str(nivel)
            vazao1 = str(vazao1)
            vazao2 = str(vazao2)

            nivelok = nivel[1:tam_nivel-1]
            nivelok = int(nivelok)
            vazao1ok = vazao1[1:tam_vazao1-1]
            vazao1ok = int(vazao1ok)
            vazao2ok = vazao2[1:tam_vazao2-1]
            vazao2ok = int(vazao2ok)

            if nivelok+vazao1ok-vazao2ok >=0 and nivelok+vazao1ok-vazao2ok <= 100:
                DataBank.set_words(2, [nivelok+vazao1ok-vazao2ok])
        
        tam_nivel = len(str(nivel))
        nivel = str(nivel)
        nivelok = nivel[1:tam_nivel-1]
        nivelok = int(nivelok)

        #Conferindo se o nível chegou a 90%
        if nivelok >= 90 and nivelok <= 99:
            print("Perto de chegar à capacidade máxima!")
            DataBank.set_bits(3, [True])
            #DataBank.set_bits(0, [False])
        
        #Conferindo se atingiu a capacidade máxima
        elif nivelok == 100:
            print("Capacidade máxima atingida!!")
            DataBank.set_bits(3, [True])
            #DataBank.set_bits(0, [False])
        
        #Conferindo se o nível chegou a 10%
        elif nivelok < 10 and nivelok >= 1:
            print("Perto de secar!")
            DataBank.set_bits(4, [False])
            #DataBank.set_bits(1, [False])
        
        #Conferindo se atingiu a capacidade mínima
        elif nivelok == 0:
            print("Secou!")
            DataBank.set_bits(4, [False])
            #DataBank.set_bits(1, [False])

        else:
            DataBank.set_bits(3, [False])
            DataBank.set_bits(4, [True]) 
            print("Entre 10 e 90% da capacidade, tudo ok!")

        for i in range(7):
            if(state != DataBank.get_words(i)):
                state = DataBank.get_words(i)
                print(f'O valor do registrador {i} agora é ' + str(state))
        sleep(2)
except:
    print("Desligando servidor")
    server.stop()
    print("Servidor desligado")