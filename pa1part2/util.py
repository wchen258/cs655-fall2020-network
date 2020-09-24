#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 11:17:34 2020

@author: kokoro
"""

import argparse
import socket

MAX_BYTE = 1024


def base_parser(with_address: bool):
    parser = argparse.ArgumentParser()
    if with_address:
        parser.add_argument('host', type=str, action='store')
    parser.add_argument('port', type=int, action='store')
    return parser

def read_line(s: socket):
    data = ''
    while True:
        data += s.recv(MAX_BYTE).decode()
        if data[-1] == '\n':
            break
    return data

def write_line(s: socket, line: str):
    s.sendall(line.encode() + b'\n')
