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

# get parameters
user = sys.argv[1]
host = sys.argv[2]
port = int(sys.argv[3])


def validate_run(msg):
    """Validate the command and run the apropiate function."""
    # Define a dictionary of valid commands and their number of parameters
    valid_commands = {
        'SUBSCR': (2, None),
        'CANCEL': (1, None),
        'STATUS': (1, None),
        'INFOS':  (1, ('M', 'K')),
        'STATIS': (('L', 2), ('ALL', 1)),
        'SLEEP':  (1, None),
        'EXIT':   (0, None)
    }
    local_commands = ['SLEEP', 'EXIT']

    # Parse the input string into a command and its parameters
    parts = msg.split()
    command = parts[0]
    parameters = parts[1:]

    # Check if the command is valid and has the right number of parameters
    if command in valid_commands:
        param_info = valid_commands[command]
        if isinstance(param_info[0], str) and parameters[0] == param_info[0]:
            num_params = param_info[1]
        elif isinstance(param_info[1], str) and parameters[0] == param_info[1]:
            num_params = param_info[0]
        else:
            num_params = param_info[0]

        if len(parameters) == num_params:
            if command in local_commands:
                print('command to execute locally')
            else:
                print('command to send server')
                conn.send_receive(msg.encode('utf-8'))
        else:
            print("MISSING-ARGUMENTS")
    else:
        print("UNKNOWN-COMMAND")


# connect to server
conn = server_connection(host, port)
conn.connect()

# send message
msg = input('>> ')
validate_run(msg)

conn.close()
