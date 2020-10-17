#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 26 22:17:19 2020

@author: kokoro
"""

import os

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


def get_npy(exp_type: str, delay: int, exp_name):
    fname = '_'.join([exp_type, str(delay)]) + '.csv'
    path = os.path.join('results', exp_name, fname)
    npy = np.genfromtxt(path, delimiter=',')
    x, y, y_std = npy[:, 0], npy[:, 1], npy[:, 2]
    return x, y, y_std


def genplotList(exp_type: str, delays, exp_name: str, probes=15):
    x_label = 'msg_size (byte)' if exp_type == 'rtt' else 'msg_size (B)'
    y_label = 'avg_rtt (ms)' if exp_type == 'rtt' else 'avg_tput (kbps)'
    plt.clf()
    ax = plt.gca()
    for delay in delays:
        x, y, y_err = get_npy(exp_type, delay, exp_name)
        if exp_type == 'tput':
            x = x
            y = 8*x / (y/1000) / 1000
            y_err = 8*x / (y_err/1000) / 1000
        color = next(ax._get_lines.prop_cycler)['color']
        plt.plot(x, y, 'o', color=color, label='delay ' + str(delay))
        plt.plot(x, y, '-', color=color)
        plt.fill_between(x, y - y_err, y + y_err, alpha=0.095, color=color)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.legend(loc='upper left')
    ax.set_ylim(bottom=0)
    ax.set_xlim(left=1)
    fname = '_'.join([exp_type, *list(str(d)
                                      for d in delays), exp_name, str(probes)]) + '.png'
    path = os.path.join('plots', fname)
    plt.savefig(path)
    return plt


if __name__ == '__main__':

    # config
    plt.style.use(['seaborn-darkgrid'])
    SERVER_DELAYS = (0, 1, 10, 20, 50, 100)
    NUMBER_OF_PROBES = 15

    # make plots directory
    if not os.path.exists('./plots'):
        os.makedirs('./plots')

    # genrete local-csa1 plot
    genplotList('tput', SERVER_DELAYS[:1], 'exp1')
    genplotList('rtt', SERVER_DELAYS[:1], 'exp1')
    genplotList('tput', SERVER_DELAYS[:4], 'exp1')
    genplotList('rtt', SERVER_DELAYS[:4], 'exp1')

    # generate csa1-testserver plot
    genplotList('tput', SERVER_DELAYS[:1], 'exp2')
    genplotList('rtt', SERVER_DELAYS[:1], 'exp2')
