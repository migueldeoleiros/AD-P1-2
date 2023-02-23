#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações Distribuídas - Projeto 1 - ticker_server.py
Grupo: 37
Números de aluno: 58645, 59436
"""

# Zona para fazer importação
import socket as s
import sys


###############################################################################

class resource:
    """Representa um recurso que pode ser subscrito por clientes."""

    def __init__(self, resource_id):
        """Inicializa a classe com parâmetros para funcionamento futuro."""
        pass  # Remover esta linha e fazer implementação da função

    def subscribe(self, client_id, time_limit):
        """Subcrebe cliente por um time_limit."""
        pass  # Remover esta linha e fazer implementação da função

    def unsubscribe(self, client_id):
        """Remove subscrição do cliente."""
        pass  # Remover esta linha e fazer implementação da função

    def status(self, client_id):
        """Retorna o estado de um cliente."""
        pass  # Remover esta linha e fazer implementação da função

    def __repr__(self):
        """Retorna a lista de subscritores do recurso."""
        output = ""
        # R <resource_id> <list of subscribers>
        return output


###############################################################################

class resource_pool:
    """Classe que representa uma pool de recursos que podem ser subscritos por clientes."""

    def __init__(self, N, K, M):
        """Inicializa a classe com parâmetros para funcionamento futuro."""
        pass  # Remover esta linha e fazer implementação da função

    def clear_expired_subs(self):
        """Remove os subscritores que expiraram."""
        pass  # Remover esta linha e fazer implementação da função

    def subscribe(self, resource_id, client_id, time_limit):
        """Subscreve o cliente ao recurso com um limite de tempo para expiração."""
        pass  # Remover esta linha e fazer implementação da função

    def unsubscribe(self, resource_id, client_id):
        """Cancela a subscrição do cliente ao recurso."""
        pass  # Remover esta linha e fazer implementação da função

    def status(self, resource_id, client_id):
        """Retorna se o cliente está subscrito ao recurso."""
        pass  # Remover esta linha e fazer implementação da função

    def infos(self, option, client_id):
        """Lista informações sobre os clientes e suas subscrições."""
        pass  # Remover esta linha e fazer implementação da função

    def statis(self, option, resource_id):
        """Lista informações sobre os recursos e seus subscritores."""
        pass  # Remover esta linha e fazer implementação da função

    def __repr__(self):
        """Retorna uma lista de subscritores dos recursos."""
        output = ""
        # Acrescentar no output uma linha por cada recurso
        return output


###############################################################################

# código do programa principal

host = sys.argv[1]
port = int(sys.argv[2])

sock = s.socket(s.AF_INET, s.SOCK_STREAM)
# sock.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)

sock.bind((host, port))
sock.listen(1)
(conn_sock, (addr, port)) = sock.accept()
print('ligado a %s no porto %s' % (addr, port))

msg = conn_sock.recv(1024)
print(msg.decode())

conn_sock.sendall(b'test send from server')

sock.close()
