# -*- coding: utf-8 -*-
"""
Aplicações Distribuídas - Projeto 2 - net_client.py
Grupo: 37
Tiago Ramalho 58645
Miguel López 59436
"""

# zona para fazer importação

import socket as s
import pickle as p
import struct as st

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

    def send(self, data):
        """
        Envia os dados contidos em data para a socket da ligação,
        e retorna a resposta recebida pela mesma socket.
        """
        data_bytes = p.dumps(data, -1)
        size_bytes = st.pack("i", len(data_bytes))
        self.sock.sendall(size_bytes)
        self.sock.sendall(data_bytes)
        print("enviado 4 Bytes +", len(data_bytes), "Bytes")
        print("enviado:", data)

    def receive(self):
        """Recebe os dados do servidor"""

        size_bytes = self.sock.recv(4)
        size = st.unpack("i", size_bytes)[0]
        msg_bytes = self.sock.recv(size)
        msg = p.loads(msg_bytes)
        print("recebido:", msg)

    def close(self):
        """Termina a ligação ao servidor."""
        self.sock.close()
        print('ligacao foi terminada')
