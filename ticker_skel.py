#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações Distribuídas - Projeto 2 - ticker_skel.py
Grupo: 37
Tiago Ramalho 58645
Miguel López 59436
"""

# Imports necessários
import pickle
import struct


def process_command(command, resources, conn_sock):
    """Executa o comando apropriado para uma mensagem.

    Args:
        command (list): Mensagem recebida do cliente.

    Returns:
        answer (str): Resposta ao comando executado.
    """
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

    msg_bytes = sckt.recv(size)
    msg = pickle.loads(msg_bytes)
    return msg


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
