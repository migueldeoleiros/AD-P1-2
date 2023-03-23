#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações Distribuídas - Projeto 2 - ticker_skel.py
Grupo: 37
Tiago Ramalho 58645
Miguel López 59436
"""

# Imports necessários
import socket as s
import pickle
import struct
import time


def process_command(command, resources, conn_sock):
    """Executa o comando apropriado para uma mensagem.

    Args:
        command (list): Mensagem recebida do cliente.

    Returns:
        answer (str): Resposta ao comando executado.
    """
    if command[0] == 10:  # SUBSCR
        data = resources.subscribe(command[1], command[3], command[2])
        answer = [11, data]
    elif command[0] == 20:  # CANCEL
        data = resources.unsubscribe(command[1], command[2])
        answer = [21, data]
    elif command[0] == 30:  # STATUS
        data = resources.status(command[1], command[2])
        answer = [31, data]
    elif command[0] == 40:  # INFOS M
        data = resources.infosM(command[1])
        answer = [41, data]
    elif command[0] == 50:  # INFOS K
        data = resources.infosK(command[1])
        answer = [51, data]
    elif command[0] == 60:  # STATIS L
        data = resources.statisL(command[1])
        answer = [61, data]
    elif command[0] == 70:  # STATIS ALL
        data = resources.statisAll()
        answer = [71] + data

    return answer


def receive_data(sckt):
    """Recebe dados através do socket especificado.

    Args:
        sckt: o socket para receber dados.
    Returns:
        os dados recebidos.
    """
    size_bytes = sckt.recv(4)
    size = struct.unpack('i', size_bytes)[0]

    msg = b''
    start_time = time.monotonic()
    while len(msg) < size:
        remaining_time = 5 - (time.monotonic() - start_time)
        if remaining_time < 0:
            raise TimeoutError('Timeout while receiving data')
        sckt.settimeout(remaining_time)
        buf = sckt.recv(size - len(msg))
        if not buf:
            raise ConnectionError('Socket connection closed unexpectedly')
        msg += buf

    return pickle.loads(msg)


def send_data(sckt, data):
    """Envia dados através do socket especificado.

    Args:
        sckt: o socket para enviar dados.
        data: os dados a serem enviados.
    """
    data_bytes = pickle.dumps(data, -1)
    size_bytes = struct.pack('i', len(data_bytes))

    sckt.sendall(size_bytes)
    sckt.sendall(data_bytes)
