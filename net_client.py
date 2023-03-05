# -*- coding: utf-8 -*-
"""
Aplicações Distribuídas - Projeto 1 - net_client.py
Grupo: 37
Tiago Ramalho 58645
Miguel López 59436
"""

# zona para fazer importação

import socket as s

# definição da classe server_connection

class server_connection:
    """
    Abstrai uma ligação a um servidor TCP. Implementa métodos para: estabelecer
    a ligação; envio de um comando e receção da resposta; terminar a ligação.
    """

    def __init__(self, address, port):
        """Inicializa a classe com parâmetros para funcionamento futuro."""
        self.address = address
        self.port = port

    def connect(self):
        """Estabelece a ligação ao servidor especificado na inicialização."""
        self.sock = s.socket(s.AF_INET, s.SOCK_STREAM)
        self.sock.connect((self.address, self.port))
        print('ligado a %s no porto %s' % (self.address, self.port))

    def send_receive(self, data):
        """
        Envia os dados contidos em data para a socket da ligação,
        e retorna a resposta recebida pela mesma socket.
        """
        # send
        print(data.decode())
        self.sock.sendall(data)
        # receive
        msg = self.sock.recv(1024)
        print(msg.decode())

    def close(self):
        """Termina a ligação ao servidor."""
        self.sock.close()
        print('ligacao foi terminada')
