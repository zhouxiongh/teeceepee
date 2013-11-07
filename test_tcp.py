#!/usr/bin/env ipython

FAKE_IP = "10.0.4.4"
MAC_ADDR = "60:67:20:eb:7b:bc"
from scapy.all import srp, Ether, ARP

for _ in range(4):
    srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(psrc=FAKE_IP, hwsrc=MAC_ADDR))

import time
import tcp
from tcp import TCPSocket

def test_handshake():
    conn = TCPSocket("example.com", 80, FAKE_IP)
    initial_seq = conn.seq
    # SYN-ACK should have finished by now
    time.sleep(0.1)
    print "conn.seq", conn.seq
    assert conn.seq == initial_seq + 1
    assert conn.state == 'ESTABLISHED'

def test_send_data():
    payload = "GET / HTTP/1.0\r\n\r\n"
    conn = TCPSocket("google.com", 80, FAKE_IP)
    conn.send(payload)
    data = conn.recv()
    assert len(data) > 5

def test_open_socket():
    conn = TCPSocket("example.com", 80, FAKE_IP)
    assert (FAKE_IP, conn.src_port) in tcp.listener.open_sockets

def test_teardown():
    conn = TCPSocket("example.com", 80, FAKE_IP)
    conn.close()
    assert conn.state == 'CLOSED'
