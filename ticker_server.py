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
import random
import time


###############################################################################

class resource:
    """Representa um recurso que pode ser subscrito por clientes."""

    def __init__(self, resource_id):
        """Inicializa a classe com parâmetros para funcionamento futuro."""
        self.ID = resource_id
        Name = ""
        for _ in range(7):
            Name += random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        self.Name = Name
        self.Symbol = Name[:3]
        self.Subscribers = []
        self.Value = random.randint(100,200)

    def subscribe(self, client_id, time_limit):
        """Subcrebe cliente por um time_limit."""
        if (client_id, time_limit) in self.Subscribers:
            return False
        else:
            self.Subscribers.append((client_id, time.time()+time_limit))
            return True

    def unsubscribe(self, client_id):
        """Remove subscrição do cliente."""
        for i, (id, _) in enumerate(self.Subscribers):
            if id == client_id:
                self.Subscribers.pop(i)
                return True
        return False

    def status(self, client_id):
        """Retorna o estado de um cliente."""
        for (id, _) in self.Subscribers:
            if id == client_id:
                return True
        return False

    def __repr__(self):
        """Retorna a lista de subscritores do recurso."""
        output = "R {} {}".format(self.ID, len(self.Subscribers))
        for x in self.Subscribers:
            output += " {}".format(x[0])
        return output


###############################################################################

class resource_pool:
    """Classe que representa uma pool de recursos que podem ser subscritos por clientes."""

    def __init__(self, N, K, M):
        """Inicializa a classe com parâmetros para funcionamento futuro."""
        self.maxSubcriptions = K
        self.maxSubscribers = N
        self.Resources = {}
        for id in range(1, M+1):
            oneResource = resource(id)
            self.Resources[id] = oneResource

    def clear_expired_subs(self):
        """Remove os subscritores que expiraram."""
        for resource in self.Resources.values():
            for (sub, time_limit) in resource.Subscribers:
                if time_limit < time.time():
                    resource.unsubscribe(sub)

    def subscribe(self, resource_id, client_id, time_limit):
        """Subscreve o cliente ao recurso com um limite de tempo para expiração."""
        if resource_id not in self.Resources:
            return "UNKNOWN RESOURCE"
        elif int(self.infos("K", client_id)) > 0:
            if int(self.statis("L", resource_id)) < self.maxSubscribers:
                x = self.Resources[resource_id].subscribe(client_id, time_limit)
                if x:
                    return "OK"
        return "NOK"

    def unsubscribe(self, resource_id, client_id):
        """Cancela a subscrição do cliente ao recurso."""
        if resource_id not in self.Resources:
            return "UNKNOWN RESOURCE"
        else:
            x = self.Resources[resource_id].unsubscribe(client_id)
            if x:
                return "OK"
            else:
                return "NOK"

    def status(self, resource_id, client_id):
        """Retorna se o cliente está subscrito ao recurso."""
        if resource_id not in self.Resources:
            return "UNKNOWN RESOURCE"
        else:
            x = self.Resources[resource_id].status(client_id)
            if x:
                return "SUBSCRIBED"
            else:
                return "UNSUBSCRIBED"

    def infos(self, option, client_id):
        """Lista informações sobre os clientes e suas subscrições."""
        result = []
        for x in self.Resources:
            if "SUBSCRIBED" == self.status(x, client_id):
                result += [x]
        if option == "M":
            return str(result)
        else:
            return str(self.maxSubcriptions - len(result))

    def statis(self, option, resource_id):
        """Lista informações sobre os recursos e seus subscritores."""
        if option == "L":
            if resource_id not in self.Resources:
                return "UNKNOWN RESOURCE"
            else:
                return str(len(self.Resources[resource_id].Subscribers))
        else:
            return self.__repr__()

    def __repr__(self):
        """Retorna uma lista de subscritores dos recursos."""
        output = ""
        for resource in self.Resources.values():
            output += resource.__repr__() + "\n"
        return output


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


###############################################################################

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
                msg = sckt.recv(1024).decode()
                if msg:  # Se recebeu dados
                    process_command(msg, resources, sckt)
                else:  # Se não recebeu dados
                    sckt.close()  # cliente fechou ligação
                    socket_list.remove(sckt)
                    print('Cliente fechou ligação')
finally:
    listen_socket.close()
    print("Socket closed")
