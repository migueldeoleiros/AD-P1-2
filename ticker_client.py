#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações Distribuídas - Projeto 1 - ticker_client.py
Grupo: 37
Números de aluno: 58645, 59436
"""
# Zona para fazer imports
from net_client import server_connection

# Programa principal

conn = server_connection("localhost", 9999)

conn.connect()

conn.send_receive(b'test send from client')

conn.close()
