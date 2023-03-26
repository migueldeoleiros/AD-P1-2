#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações Distribuídas - Projeto 2 - ticker_server.py
Grupo: 37
Tiago Ramalho 58645
Miguel López 59436
"""

# Imports necessários
import socket as s
import select as sel
import sys
from ticker_pool import resource_pool
import ticker_skel as skel


# código do programa principal
host = sys.argv[1]
port = int(sys.argv[2])
M = int(sys.argv[3])
K = int(sys.argv[4])
N = int(sys.argv[5])

listen_socket = s.socket(s.AF_INET, s.SOCK_STREAM)
listen_socket.bind((host, port))
listen_socket.listen(1)

resources = resource_pool(N, K, M)

socket_list = [listen_socket]
try:
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
                    try:
                        msg = skel.receive_data(sckt)
                    except (TimeoutError, ConnectionError) as e:
                        print(e)
                    else:
                        print('Cliente %s:%d: recebido: %s' % (addr, port, str(msg)))
                        answer = skel.process_command(msg, resources, sckt)
                        print('enviado:', answer)
                        skel.send_data(sckt, answer)
                except:
                    sckt.close()  # cliente fechou ligação
                    socket_list.remove(sckt)
                    print('Cliente fechou ligação')

except KeyboardInterrupt:
    for sckt in socket_list:
        sckt.close()
    listen_socket.close()
    print("Servidor encerrando")
