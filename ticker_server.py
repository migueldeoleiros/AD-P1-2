#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações Distribuídas - Projeto 1 - ticker_server.py
Grupo: 37
Tiago Ramalho 58645
Miguel López 59436
"""

# Imports necessários
import socket as s
import select as sel
import sys
import pickle
import struct
from ticker_pool import resource_pool


def process_command(msg, resources, conn_sock):
    """Executa o comando apropriado para uma mensagem.

    Args:
        msg (str): Mensagem recebida do cliente.

    Returns:
        answer (str): Resposta ao comando executado.
    """
    command = msg.split()

    if command[0] == 'SUBSCR':
        answer = resources.subscribe(int(command[1]), int(command[3]), int(command[2]))
    elif command[0] == 'CANCEL':
        answer = resources.unsubscribe(int(command[1]), int(command[2]))
    elif command[0] == 'STATUS':
        answer = resources.status(int(command[1]), int(command[2]))
    elif command[0] == 'INFOS':
        answer = resources.infos(command[1], int(command[2]))
    elif command[0] == 'STATIS':
        answer = resources.statis(command[1], int(command[2]))

    print(answer)
    conn_sock.sendall(answer.encode())


def receive_data(sckt):
    size_bytes = sckt.recv(4)
    size = struct.unpack('i', size_bytes)[0]

    msg_bytes = sckt.recv(size)
    msg = pickle.loads(msg_bytes)
    return msg


# código do programa principal
host = sys.argv[1]
port = int(sys.argv[2])
M = int(sys.argv[3])
K = int(sys.argv[4])
N = int(sys.argv[5])

listen_socket = s.socket(s.AF_INET, s.SOCK_STREAM)
listen_socket.bind((host, port))
listen_socket.listen(1)

try:
    resources = resource_pool(N, K, M)

    socket_list = [listen_socket]
    while True:
        R, W, X = sel.select(socket_list, [], [])  # Espera sockets com
        for sckt in R:
            if sckt is listen_socket:  # Se for a socket de escuta...
                conn_sock, addr = listen_socket.accept()
                addr, port = conn_sock.getpeername()
                print('Novo cliente ligado desde %s:%d' % (addr, port))
                socket_list.append(conn_sock)  # Adiciona ligação à lista
            else:  # Se for a socket de um cliente...
                try:
                    msg = receive_data(sckt)
                    process_command(msg, resources, sckt)
                except (EOFError, ConnectionResetError):
                    sckt.close()  # cliente fechou ligação
                    socket_list.remove(sckt)
                    print('Cliente fechou ligação')

finally:
    listen_socket.close()
    print("Socket closed")
