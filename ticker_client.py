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


    if command == "SUBSCR":
        if len(parameters != 2):
            print("MISSING-ARGUMENTS")
            return True
        #put here whatever the stub will do (MARK)
        return True

    elif command == "CANCEL":
        if len(parameters != 1):
            print("MISSING-ARGUMENTS")
            return True
        #put here whatever the stub will do (MARK)
        return True

    elif command == "STATUS":
        if len(parameters != 1):
            print("MISSING-ARGUMENTS")
            return True
        #put here whatever the stub will do (MARK)
        return True
    
    elif command == "INFOS":
        if len(parameters != 1):
            print("MISSING-ARGUMENTS")
            return True
        elif parameters[0] == "M":
            #put here whatever the stub will do (MARK)
            return True
        elif parameters[0] == "K":
            #put here whatever the stub will do (MARK)
            return True
        else:
            print("MISSING-ARGUMENTS")
            return True
    
    elif command == "STATIS":
        if len(parameters < 1):
            print("MISSING-ARGUMENTS")
            return True
        elif parameters[0] == "L":
            if len(parameters!=2):
                print("MISSING-ARGUMENTS")
                return True
            #put here whatever the stub will do (MARK)
            return True
        elif parameters[0] == "ALL":
            if len(parameters != 1):
                print("MISSING-ARGUMENTS")
                return True
            #put here whatever the stub will do (MARK)
            return True
        else:
            print("MISSING-ARGUMENTS")
            return True
    
    elif command == "SLEEP":
        if len(parameters != 1):
            print("MISSING-ARGUMENTS")
            return True
        time.sleep(int(parameters[0]))
        return True
    
    elif command == "EXIT":
        return False
    
    else:
        print("UNKNOWN-COMMAND")
    



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
