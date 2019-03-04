#!/usr/bin/env python3.7.2

import socket
from socket.socket import AF_INET, SOCK_STREAM
import time

START_TIME = time.perf_counter()


class Peer:
    __slots__ = ("conn", "addr", "conn_time",)
    def __init__(self, conn, addr):
        self.conn = conn
        self.addr = addr
        self.conn_time = time.perf_counter() - START_TIME  # time the connection was established


class Node:
    __slots__ = ("host", "port", "sock", "peers")
    def __init__(self, address=("127.0.0.1", 56342)):
        self.host, self.port = *address
        self.sock = None
        self.peers = []

    def start(self):
        self.sock = socket.socket(AF_INET, SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.sock.listen()
        self.sock.setblocking(False)

        while True:
            conn, addr = self.sock.accept()
            conn.setblocking(False)
            self.peers.append(Peer(conn, addr))
