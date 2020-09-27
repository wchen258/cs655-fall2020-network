#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 26 22:17:19 2020

@author: kokoro
"""

import seaborn as sns
import numpy as np
import os
import matplotlib.pyplot as plt

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

def genplot(exp_type:str, delay:int, exp_name:str, probes=15):
    x_label = 'msg_size (byte)' if exp_type=='rtt' else 'msg_size (KB)'
    y_label = 'avg_rtt (ms)' if exp_type=='rtt' else 'avg_tput (kbps)'
    x,y,y_err = get_npy(exp_type, delay, exp_name)
    if exp_type=='tput':
        x = x/1000
        y = x / y * (1024/1000)
        y_err = x / y_err * (1024/1000)
    
    plt.plot(x, y, 'or')
    plt.plot(x, y, '-', color='red')
    plt.fill_between(x, y - y_err, y + y_err,color='gray', alpha=0.2)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    fname = '_'.join([exp_type, str(delay), exp_name, str(probes)]) + '.png'
    path = os.path.join('plots', fname)
    plt.savefig(path)
    return plt
    



if __name__=='__main__':
    
    ## config
    exp_name = 'exp1'
    plt.style.use(['seaborn-darkgrid'])
    
    ## make plots directory
    if not os.path.exists('./plots'):
        os.makedirs('./plots')
        
    genplot('tput', 0, 'exp1')
    
