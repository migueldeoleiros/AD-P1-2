#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações Distribuídas - Projeto 1 - ticker_client.py
Grupo: 37
Números de aluno: 58645, 59436
"""
# Zona para fazer imports
from net_client import server_connection
import sys
import time

# get parameters
user = sys.argv[1]
host = sys.argv[2]
port = int(sys.argv[3])


def validate_run(msg):
    """
    Validate the command and run the apropiate function.

    Returns:
        True if the command needs to continue
        False if the command needs to exit
    """
    # Define a dictionary of valid commands and their number of parameters
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

    # Parse the input string into a command and its parameters
    parts = msg.split()
    command = parts[0]
    parameters = parts[1:]

    # Check if the command is valid
    if command not in valid_commands:
        print("UNKNOWN-COMMAND")
        return True

    param_info = valid_commands[command]  # get info about the parameters

    num_params = None  # in case command is neither of the two options below

    # checks number of parameters for long commands
    if isinstance(param_info[0], tuple):
        for option in param_info:
            if parameters[0] in option:
                num_params = option[1]
                break
    else:  # checks number of parameters for normal commands
        num_params = param_info[0]

    if len(parameters) != num_params:
        print("MISSING-ARGUMENTS")
        return True

    # Check if the command is local or has to be run on the server
    if command in local_commands:
        return run_local_command(msg)
    else:
        server_request(msg)
        return False


def server_request(msg):
    """Envia os comandos ao servidor."""
    conn = server_connection(host, port)
    conn.connect()

    conn.send_receive(msg.encode())

    conn.close()


def run_local_command(msg):
    """Executa os comandos locais."""
    parts = msg.split()
    if parts[0] == 'SLEEP':
        time.sleep(int(parts[1]))
        return True
    else:
        return False


run = True
while run:
    msg = input('comando> ')
    run = validate_run(msg)
