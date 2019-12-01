import socket
import sys

# Criando socket TCP 
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Liga o socket a porta TCP (bind)
server_address = ('localhost', 10002)
sock.bind(server_address)

# Escutando as conexões recebidas
sock.listen(1)

while True:
    connection, client_address = sock.accept()

    try:
        data = connection.recv(16)
        print('Chamando senha: {}'.format(data.decode()))


    finally:
        # Fecha a conexão
        connection.close()