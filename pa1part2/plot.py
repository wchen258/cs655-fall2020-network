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
    plt.fill_between(x, y - y_err, y + y_err,color='red', alpha=0.095)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    fname = '_'.join([exp_type, str(delay), exp_name, str(probes)]) + '.png'
    path = os.path.join('plots', fname)
    plt.savefig(path)
    return plt

def genplot2(exp_type:str, delay:int, delay2:int, exp_name:str, probes=15):
    x_label = 'msg_size (byte)' if exp_type=='rtt' else 'msg_size (KB)'
    y_label = 'avg_rtt (ms)' if exp_type=='rtt' else 'avg_tput (kbps)'
    x,y,y_err = get_npy(exp_type, delay, exp_name)
    x2,y2,y_err2 = get_npy(exp_type, delay2, exp_name)
    if exp_type=='tput':
        x, x2 = x/1000, x2/1000
        y, y2 = x / y * (1024/1000), x2 / y2 * (1024/1000)
        y_err, y_err2 = x / y_err * (1024/1000) , x2/y_err2 * (1024/1000)
    
    plt.plot(x, y, 'or')
    plt.plot(x, y, '-', color='red')
    plt.fill_between(x, y - y_err, y + y_err,color='red', alpha=0.095)
    plt.plot(x2, y2, 'ob')
    plt.plot(x2, y2, '-', color='blue')
    plt.fill_between(x2, y2 - y_err2, y2 + y_err2,color='blue', alpha=0.095)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    fname = '_'.join([exp_type, str(delay), str(delay2), exp_name, str(probes)]) + '.png'
    path = os.path.join('plots', fname)
    plt.savefig(path)
    return plt

def genplotList(exp_type:str, delays, exp_name:str, probes=15):
    x_label = 'msg_size (byte)' if exp_type=='rtt' else 'msg_size (KB)'
    y_label = 'avg_rtt (ms)' if exp_type=='rtt' else 'avg_tput (kbps)'
    
    ax = plt.gca()
    for delay in delays:
        x,y,y_err = get_npy(exp_type, delay, exp_name)
        if exp_type=='tput':
            x = x/1000
            y = x / y * (1024/1000)
            y_err = x / y_err * (1024/1000)
        color = next(ax._get_lines.prop_cycler)['color']
        plt.plot(x, y, 'o', color=color, label='delay ' + str(delay))
        plt.plot(x, y, '-', color=color)
        plt.fill_between(x, y - y_err, y + y_err, alpha=0.095, color=color)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.legend(loc='upper left')
    ax.set_ylim(bottom=0)
    ax.set_xlim(left=1)
    fname = '_'.join([exp_type, *list(str(d) for d in delays), exp_name, str(probes)]) + '.png'
    path = os.path.join('plots', fname)
    plt.savefig(path)
    return plt
    



if __name__=='__main__':
    
    ## config
    exp_name = 'exp1'
    plt.style.use(['seaborn-darkgrid'])
    SERVER_DELAYS = (0, 1, 10, 20, 50, 100)
    NUMBER_OF_PROBES = 15
    
    ## make plots directory
    if not os.path.exists('./plots'):
        os.makedirs('./plots')
        
    genplotList('tput', SERVER_DELAYS[:4], 'exp1')
    
