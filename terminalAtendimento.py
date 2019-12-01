import socket
import sys

while True:
    try:
        # Criando socket TCP 
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Conecta o socket à porta em que o servidor está escutando
        server_address = ('localhost', 10001)

        input("Aperte qualquer tecla pra chamar a próxima senha\n")
        sock.connect(server_address)

        # Envia a solicitação da próxima senha ao servidor
        message = 'proxima'.encode()
        print('Chamando nova senha...\n')
        sock.sendall(message)

        # Olha a resposta
        amount_received = 0
        amount_expected = 1

        while amount_received < amount_expected:
            data = sock.recv(16)
            amount_received += len(data)
            if(data.decode() == "0"):
                print("Filas vazias")
            else:
                print('Senha recebida {}\n'.format(data.decode()))

    finally:
        # Fecha o socket
        sock.close()