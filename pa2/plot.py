import numpy as np
import pandas as pd
import seaborn as sns
import os
import warnings

warnings.filterwarnings("ignore")


def conf_interval(arr, Z=1.96):
    mean = np.average(arr)
    std = np.std(arr, ddof=1)
    upper = mean + Z * std / np.sqrt(20)
    lower = mean - Z * std / np.sqrt(20)
    return f'{lower:.2f}', f'{upper:.2f}'


def cout_conf_interval(df, Z=1.96, col=1):
    d = {}
    for i in range(10):
        start = i*20
        arr = df.iloc[start:(start+20), col]
        inter = conf_interval(arr, Z)
        d[f'0.{i}'] = inter
        print(f'0.{i}', inter)
    return d


if __name__ == '__main__':

    if not os.path.exists('../plots'):
        os.makedirs('../plots')

    namelist=['ave_cmt', 'prob', 'rands', 'rtt', 'retrans','tput','gput']

    sns.set_style("darkgrid", {"axes.facecolor": ".9"})

    data = pd.read_csv('corrupt_exp', names=namelist)
    data = data.iloc[:, :2]
    print("SR corruption vs communication time")
    cout_conf_interval(data,col=0)
    plot = sns.pointplot('prob', 'ave_cmt', data=data, dodge=True, join=True)
    fig = plot.get_figure()
    fig.savefig('../plots/p1plot_cor_cmt.png')

    fig.clf()

    data = pd.read_csv('drop_exp', names=namelist)
    data = data.iloc[:, :2]
    print("SR loss vs communication time")
    cout_conf_interval(data,col=0)
    plot = sns.pointplot('prob', 'ave_cmt', data=data, dodge=True, join=True)
    fig = plot.get_figure()
    fig.savefig('../plots/p1plot_drop_cmt.png')

    fig.clf()

    data = pd.read_csv('drop_exp', names=namelist)
    data.fillna(0, inplace=True)
    data = data.iloc[:, [1,3]]
    print("SR loss vs RTT")
    cout_conf_interval(data)
    plot = sns.pointplot('prob', 'rtt', data=data, dodge=True, join=False)
    fig = plot.get_figure()
    fig.savefig('../plots/p1plot_drop_rtt.png')

    fig.clf()

    data = pd.read_csv('corrupt_exp', names=namelist)
    data = data.iloc[:, [1,3]]
    data.fillna(0, inplace=True)
    print("SR corrupt vs RTT")
    cout_conf_interval(data)
    plot = sns.pointplot('prob', 'rtt', data=data, dodge=True, join=False)
    fig = plot.get_figure()
    fig.savefig('../plots/p1plot_cor_rtt.png')


    fig.clf()

    data = pd.read_csv('drop_exp', names=namelist)
    data = data.iloc[:, [1,4]]
    print("SR loss vs num retransmission")
    cout_conf_interval(data)
    plot = sns.pointplot('prob', 'retrans', data=data, dodge=True, join=True)
    fig = plot.get_figure()
    fig.savefig('../plots/p1plot_drop_retrans.png')

    fig.clf()

    data = pd.read_csv('corrupt_exp', names=namelist)
    data = data.iloc[:, [1,4]]
    print("SR corrupt vs num retransmission")
    cout_conf_interval(data)
    plot = sns.pointplot('prob', 'retrans', data=data, dodge=True, join=True)
    fig = plot.get_figure()
    fig.savefig('../plots/p1plot_cor_retrans.png')


   ## Tput 

    fig.clf()

    data = pd.read_csv('drop_exp', names=namelist)
    data = data.iloc[:, [1,5]]
    print("SR loss vs tput")
    cout_conf_interval(data)
    plot = sns.pointplot('prob', 'tput', data=data, dodge=True, join=True)
    fig = plot.get_figure()
    fig.savefig('../plots/p1plot_drop_tput.png')

    fig.clf()

    data = pd.read_csv('corrupt_exp', names=namelist)
    data = data.iloc[:, [1,5]]
    print("SR corrupt vs tput")
    cout_conf_interval(data)
    plot = sns.pointplot('prob', 'tput', data=data, dodge=True, join=True)
    fig = plot.get_figure()
    fig.savefig('../plots/p1plot_cor_tput.png')


    # gput

    fig.clf()

    data = pd.read_csv('drop_exp', names=namelist)
    data = data.iloc[:, [1,6]]
    print("SR loss vs gput")
    cout_conf_interval(data)
    plot = sns.pointplot('prob', 'gput', data=data, dodge=True, join=True)
    fig = plot.get_figure()
    fig.savefig('../plots/p1plot_drop_gput.png')

    fig.clf()

    data = pd.read_csv('corrupt_exp', names=namelist)
    data = data.iloc[:, [1,6]]
    print("SR corrupt vs gput")
    cout_conf_interval(data)
    plot = sns.pointplot('prob', 'gput', data=data, dodge=True, join=True)
    fig = plot.get_figure()
    fig.savefig('../plots/p1plot_cor_gput.png')
