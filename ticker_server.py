#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações Distribuídas - Projeto 1 - ticker_server.py
Grupo: 37
Números de aluno: 58645, 59436
"""

# Zona para fazer importação
import socket as s

###############################################################################

class resource:
    def __init__(self, resource_id):
        pass  # Remover esta linha e fazer implementação da função

    def subscribe(self, client_id, time_limit):
        pass  # Remover esta linha e fazer implementação da função

    def unsubscribe (self, client_id):
        pass  # Remover esta linha e fazer implementação da função

    def status(self, client_id):
        pass  # Remover esta linha e fazer implementação da função

    def __repr__(self):
        output = ""
        # R <resource_id> <list of subscribers>
        return output

###############################################################################

class resource_pool:
    def __init__(self, N, K, M):
        pass  # Remover esta linha e fazer implementação da função
        
    def clear_expired_subs(self):
        pass  # Remover esta linha e fazer implementação da função

    def subscribe(self, resource_id, client_id, time_limit):
        pass  # Remover esta linha e fazer implementação da função

    def unsubscribe (self, resource_id, client_id):
        pass  # Remover esta linha e fazer implementação da função

    def status(self, resource_id, client_id):
        pass  # Remover esta linha e fazer implementação da função

    def infos(self, option, client_id):
        pass  # Remover esta linha e fazer implementação da função

    def statis(self, option, resource_id):
        pass  # Remover esta linha e fazer implementação da função

    def __repr__(self):
        output = ""
        # Acrescentar no output uma linha por cada recurso
        return output

###############################################################################

# código do programa principal

host = 'localhost'
port = 9999

sock = s.socket(s.AF_INET, s.SOCK_STREAM)
# sock.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)

sock.bind((host, port))
sock.listen(1)
(conn_sock, (addr, port)) = sock.accept()
print('ligado a %s no porto %s' % (addr, port))

msg = conn_sock.recv(1024)
print(msg)

conn_sock.sendall(b'test send from server')

sock.close()
