#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações Distribuídas - Projeto 1 - ticker_server.py
Grupo: 37
Números de aluno: 58645, 59436
"""

# Imports necessários
import socket as s
import sys
import random


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

    def subscribe(self, client_id, time_limit):
        """Subcrebe cliente por um time_limit."""
        if client_id in self.Subscribers:
            return False
        else:
            self.Subscribers += [client_id]
            return True

    def unsubscribe(self, client_id):
        """Remove subscrição do cliente."""
        if client_id in self.Subscribers:
            self.Subscribers.remove(client_id)
            return True
        else:
            return False

    def status(self, client_id):
        """Retorna o estado de um cliente."""
        return client_id in self.Subscribers

    def __repr__(self):
        """Retorna a lista de subscritores do recurso."""
        output = "R {} {}".format(self.ID,len(self.Subscribers))
        for x in self.Subscribers:
            output += " {}".format(x)
        return output


###############################################################################

class resource_pool:
    """Classe que representa uma pool de recursos que podem ser subscritos por clientes."""

    def __init__(self, N, K, M):
        """Inicializa a classe com parâmetros para funcionamento futuro."""
        self.maxSubcriptions = K
        self.maxSubscribers = N
        self.Resources = {}
        while len(self.Resources) < M:
            id = random.randint(100,200)
            while id in self.Resources:
                id = random.randint(100,200)
            oneResource = resource(id)
            self.Resources[id] = oneResource


    def clear_expired_subs(self):
        """Remove os subscritores que expiraram."""
        pass  # Remover esta linha e fazer implementação da função

    def subscribe(self, resource_id, client_id, time_limit):
        """Subscreve o cliente ao recurso com um limite de tempo para expiração."""
        if resource_id not in self.Resources:
            return "UNKNOWN RESOURCE"
        else:
            x = self.Resources[resource_id].subscribe(client_id,time_limit)
            if x:
                return "OK"
            else:
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
            if self.status(x,client_id):
                result += [x]
        if option == "M":
            return result
        else:
            return self.maxSubcriptions - len(result)



    def statis(self, option, resource_id):
        """Lista informações sobre os recursos e seus subscritores."""
        if option == "L":
            if resource_id not in self.Resources:
                return "UNKNOWN RESOURCE"
            else:
                return len(self.Resources[resource_id].Subscribers)
        else:
            return self.__repr__()


    def __repr__(self):
        """Retorna uma lista de subscritores dos recursos."""
        output = ""
        for x in self.Resources:
            output += x.__repr__() + "\n" 
        return output


###############################################################################

# código do programa principal

host = sys.argv[1]
port = int(sys.argv[2])

sock = s.socket(s.AF_INET, s.SOCK_STREAM)
sock.bind((host, port))

while True:
    sock.listen(1)
    (conn_sock, (addr, port)) = sock.accept()
    print('ligado a %s no porto %s' % (addr, port))

    msg = conn_sock.recv(1024)
    print(msg.decode())

    conn_sock.sendall(b'test send from server')
    conn_sock.close()

sock.close()
