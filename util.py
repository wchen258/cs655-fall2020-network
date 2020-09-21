#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 11:17:34 2020

@author: kokoro
"""

import argparse

def base_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-host', type=str, action='store')
    parser.add_argument('-port', type=int, action='store')
    return parser