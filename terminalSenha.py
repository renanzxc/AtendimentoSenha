import socket
import sys

while True:
    try:
        # Criando socket UDP
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        server_address = ('localhost', 10000)

        print("N - Normal")
        print("P - Prioritária")

        # Informa o tipo de senha
        senha = input("Qual seu tipo de senha? ").upper()
        message = senha.encode()

        # Envia a silicitação de senha para o servidor
        print('\nEnviando solicitação de senha {}'.format(message.decode()))
        sent = sock.sendto(message, server_address)

        # Recebe a senha
        print('Esperando a senha...\n')
        data, server = sock.recvfrom(4096)
        print('Sua senha é {}\n'.format(data.decode()))

    finally:
        # Fecha o socket
        sock.close()