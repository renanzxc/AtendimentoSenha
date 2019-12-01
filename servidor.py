import socket
import sys

import threading

import datetime

def funcUDP():
    global ultimaSenhaN, ultimaSenhaP

    # Criando socket UDP 
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Liga o socket a porta UDP (bind)
    server_address = ('localhost', 10000)
    sock.bind(server_address)

    while True:
        # Recebe a solicitação do terminal de senha
        tipoSenha, address = sock.recvfrom(4096)
        tipoSenha = tipoSenha.decode()

        print('\nSolicitação de senha do tipo {} de {}'.format(tipoSenha, address))
        print(datetime.datetime.now())

        # Insere na fila 
        if(tipoSenha == 'N'):
            ultimaSenhaN += 1
            senha = tipoSenha+str(ultimaSenhaN)

            filaN.append(senha)
        else:
            ultimaSenhaP += 1
            senha = tipoSenha+str(ultimaSenhaP)

            filaP.append(senha)

        # Retorna a senha para o terminal
        sent = sock.sendto((senha).encode(), address)
        print('Enviando senha: {} para {}'.format(senha, address))

def funcTCP():
    global norAtendidos

    # Criando socket TCP 
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Liga o socket a porta TCP (bind)
    server_address = ('localhost', 10001)
    sock.bind(server_address)

    # Escutando as conexões recebidas
    sock.listen(1)

    while True:
        connection, client_address = sock.accept()

        try:

            # Recebe a solicitação de senha e envia a primeira senha da fila
            while True:
                data = connection.recv(16)
                if(data.decode() == "proxima"):

                    print('Enviado próxima senha...\n'.format(data))
                    print(datetime.datetime.now())

                    if(len(filaN) > 0 and (norAtendidos < 2 or len(filaP) == 0)):
                        norAtendidos += 1
                        senha = filaN[0]
                        print("Senha {} enviada\n".format(senha))
                        connection.sendall(senha.encode())
                        enviaTv(senha)
                        del filaN[0]
                        if(norAtendidos == 2 and len(filaP) == 0):
                            norAtendidos = 0

                    elif(len(filaP) > 0 ):
                        norAtendidos = 0
                        print("Senha {} enviada\n".format(filaP[0]))
                        senha = filaP[0]
                        connection.sendall(senha.encode())
                        enviaTv(senha)
                        del filaP[0]

                    else:
                        print("Filas vazias\n")
                        senha = "0".encode()
                        connection.sendall(senha)

                    break

        finally:
            # Fecha a conexão
            connection.close()

def enviaTv(senha):
    # Criando socket TCP 
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Conecta o socket à porta em que a tv está escutando
    server_address = ('localhost', 10002)
    sock.connect(server_address)

    try:

        # Envia a senha
        message = senha.encode()
        print('Enviando senha para tv')
        sock.sendall(message)

    finally:
        # Fecha o socket
        sock.close()


# Filas Normal e Prioritária
filaN = []
filaP = []

ultimaSenhaN = 0
ultimaSenhaP = 0

norAtendidos = 0

print(filaN, filaP)
print('\nEsperando mensangem')

# Cria as threads
tUDP = threading.Thread(target=funcUDP)
tTCP = threading.Thread(target=funcTCP)

tUDP.start()
tTCP.start()   
    
while True:
    pass