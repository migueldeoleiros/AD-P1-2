#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações Distribuídas - Projeto 1 - ticker_client.py
Grupo: 37
Tiago Ramalho 58645
Miguel López 59436
"""
# Imports necessários
from net_client import server_connection
import sys
import time

# parâmetros recebidos pelo terminal
user = sys.argv[1]
host = sys.argv[2]
port = int(sys.argv[3])


def validate_run(msg, conn):
    """
    Validate the command and run the apropiate function.

    Returns:
        True if the command needs to continue
        False if the command needs to exit
    """
    # Define o dicionario de comandos validos, assim como o seu número de parâmetros
    valid_commands = {
        'SUBSCR': (2, None),
        'CANCEL': (1, None),
        'STATUS': (1, None),
        'INFOS':  (('M', 1), ('K', 1)),
        'STATIS': (('L', 2), ('ALL', 1)),
        'SLEEP':  (1, None),
        'EXIT':   (0, None)
    }
    local_commands = ['SLEEP', 'EXIT']

    # Divide a string entre o comando, e os seus parâmetros
    parts = msg.split()
    command = parts[0]
    parameters = parts[1:]

    # Verifica se o comando é válido
    if command not in valid_commands:
        print("UNKNOWN-COMMAND")
        return True

    param_info = valid_commands[command]  # Recebe a informação do comando

    num_params = None  # Resultado esperado caso os proximos checks falhem

    # Verifica se o comando é composto (INFOS/STATIS)
    if isinstance(param_info[0], tuple):
        for option in param_info:
            if len(parameters) == 0:
                print("MISSING-ARGUMENTS")
                return True
            elif parameters[0] in option:
                num_params = option[1]
                break
    else:  # Obtem o número de parâmetros se o comando for simples
        num_params = param_info[0]

    # Verifica se o número de parâmetros recebido é igual ao
    # número de parâmetros necessário para o comando
    if len(parameters) != num_params:
        print("MISSING-ARGUMENTS")
        return True

    # Verifica se o comando é local ou do servidor
    if command in local_commands:
        return run_local_command(msg)
    else:
        conn.send_receive((msg+" "+user).encode())
        return True


def run_local_command(msg):
    """Funcão encarregada de correr comandos locais."""
    parts = msg.split()
    if parts[0] == 'SLEEP':
        time.sleep(int(parts[1]))
        return True
    else:
        return False


# Loop para o cliente (Sempre True, até recibir a message de EXIT)
run = True
conn = server_connection(host, port)
conn.connect()
try:
    while run:
        message = input('comando>')
        run = validate_run(message, conn)
except:
    conn.close()
