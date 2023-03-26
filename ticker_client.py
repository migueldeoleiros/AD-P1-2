#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações Distribuídas - Projeto 2 - ticker_client.py
Grupo: 37
Tiago Ramalho 58645
Miguel López 59436
"""
# Imports necessários
from ticker_stub import ticker_stub
import sys
import time

# parâmetros recebidos pelo terminal
user = int(sys.argv[1])
host = sys.argv[2]
port = int(sys.argv[3])


def validate_run(msg, con):
    """
    Validate the command and run the apropiate function.

    Returns:
        True if the command needs to continue
        False if the command needs to exit
    """

    # Divide a string entre o comando, e os seus parâmetros
    parts = msg.split()
    command = parts[0]
    parameters = parts[1:]

    try:
        if command == "SUBSCR":
            if len(parameters) != 2:
                print("MISSING-ARGUMENTS")
                return True
            con.subscribe(int(parameters[0]), int(parameters[1]), user)
            return True

        elif command == "CANCEL":
            if len(parameters) != 1:
                print("MISSING-ARGUMENTS")
                return True
            con.unsubscribe(int(parameters[0]), user)
            return True

        elif command == "STATUS":
            if len(parameters) != 1:
                print("MISSING-ARGUMENTS")
                return True
            con.status(int(parameters[0]), user)
            return True

        elif command == "INFOS":
            if len(parameters) != 1:
                print("MISSING-ARGUMENTS")
                return True
            elif parameters[0] == "M":
                con.infos(40, user)
                return True
            elif parameters[0] == "K":
                con.infos(50, user)
                return True
            else:
                print("MISSING-ARGUMENTS")
                return True
            
        elif command == "STATIS":
            if len(parameters) < 1:
                print("MISSING-ARGUMENTS")
                return True
            elif parameters[0] == "L":
                if len(parameters) != 2:
                    print("MISSING-ARGUMENTS")
                    return True
                con.statis(60, int(parameters[1]))
                return True
            elif parameters[0] == "ALL":
                if len(parameters) != 1:
                    print("MISSING-ARGUMENTS")
                    return True
                con.statis(70)
                return True
            else:
                print("MISSING-ARGUMENTS")
                return True

        elif command == "SLEEP":
            if len(parameters) != 1:
                print("MISSING-ARGUMENTS")
                return True
            time.sleep(int(parameters[0]))
            return True
        elif command == "EXIT":
            return False

        else:
            print("UNKNOWN-COMMAND")
            return True

    except ValueError:
        print("WRONG-ARGUMENT-TYPE")
        return True


# Loop para o cliente (Sempre True, até recibir a message de EXIT)
run = True
conn = ticker_stub(host, port)
conn.connect()
try:
    while run:
        message = input('comando>')
        run = validate_run(message, conn)
except Exception as e:
    print(e)
    conn.disconnect()
