#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações Distribuídas - Projeto 2 - ticker_stub.py
Grupo: 37
Tiago Ramalho 58645
Miguel López 59436
"""

import socket as s
from net_client import server_connection

class ticker_stub:

    def __init__(self, address, port):
        self.net_client = server_connection(address, port)

    def connect(self):
        self.net_client.connect()

    def disconnect(self):
        self.net_client.close()

    def subscribe(self, IDrec, time, IDcli):
        self.net_client.send([10, IDrec, time, IDcli])
        self.net_client.receive()

    def unsubscribe(self, IDrec, IDcli):
        self.net_client.send([20, IDrec, IDcli])
        self.net_client.receive()

    def status(self, IDrec, IDcli):
        self.net_client.send([30, IDrec, IDcli])
        self.net_client.receive()

    def infos(self, type, IDcli):
        self.net_client.send([type, IDcli])
        self.net_client.receive()

    def statis(self, type, IDrec=None):
        if IDrec is not None:
            self.net_client.send([type, IDrec])
            self.net_client.receive()
        else:
            self.net_client.send([type])
            self.net_client.receive()
