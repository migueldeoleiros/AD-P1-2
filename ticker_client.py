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

# Programa principal

# connect to server
user = sys.argv[1]
host = sys.argv[2]
port = int(sys.argv[3])

conn = server_connection(host, port)
conn.connect()

# send message
msg = input('>> ')
conn.send_receive(msg.encode('utf-8'))

conn.close()
