#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 26 22:17:19 2020

@author: kokoro
"""

import seaborn
import numpy as np
import os

def get_datas(expname):
    path = os.path.join('results', expname)
    onlyfiles = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    # onlyfiles = list(map(lambda x: os.path.join('results', x), onlyfiles))
    return onlyfiles

def get_npy(exp_type:str, delay:int, exp_name):
    fname = '_'.join([exp_type, str(delay)]) + '.csv'
    path = os.path.join('results', exp_name, fname)
    npy = np.genfromtxt(path, delimiter=',')
    x,y,y_std = npy[:,0], npy[:,1], npy[:,2]
    return x, y, y_std
    



if __name__=='__main__':
    exp_name = 'exp1'
    
    x, y, y_std = get_npy('rtt', 0, exp_name)