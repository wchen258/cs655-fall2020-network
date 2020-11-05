import numpy as np
import pandas as pd
import seaborn as sns
import warnings

warnings.filterwarnings("ignore")


def conf_interval(arr, Z=1.96):
    mean = np.average(arr)
    std = np.std(arr, ddof=1)
    upper = mean + Z * std / np.sqrt(20)
    lower = mean - Z * std / np.sqrt(20)
    return f'{lower:.2f}', f'{upper:.2f}'


def cout_conf_interval(df, Z=1.96):
    d = {}
    for i in range(10):
        start = i*20
        arr = df.iloc[start:(start+20), 0]
        inter = conf_interval(arr, Z)
        d[f'0.{i}'] = inter
        print(f'0.{i}', inter)
    return d


if __name__ == '__main__':
    sns.set_style("darkgrid", {"axes.facecolor": ".9"})

    data = pd.read_csv('corrupt_exp', names=['ave_cmt', 'prob', 'rands', 'rtt', 'retrans'])
    data = data.iloc[:, :2]
    print("corrupt case interval")
    cout_conf_interval(data)
    plot = sns.pointplot('prob', 'ave_cmt', data=data, dodge=True, join=True)
    fig = plot.get_figure()
    fig.savefig('../plots/p2plot_cor_cmt.png')

    fig.clf()

    data = pd.read_csv('drop_exp', names=['ave_cmt', 'prob', 'rands', 'rtt', 'retrans'])
    data = data.iloc[:, :2]
    print("loss case interval")
    cout_conf_interval(data)
    plot = sns.pointplot('prob', 'ave_cmt', data=data, dodge=True, join=True)
    fig = plot.get_figure()
    fig.savefig('../plots/p2plot_drop_cmt.png')

    fig.clf()

    data = pd.read_csv('drop_exp', names=['ave_cmt', 'prob', 'rands', 'rtt', 'retrans'])
    data = data.iloc[:, [1,3]]
    print("loss case interval")
    cout_conf_interval(data)
    plot = sns.pointplot('prob', 'rtt', data=data, dodge=True, join=True)
    fig = plot.get_figure()
    fig.savefig('../plots/p2plot_drop_rtt.png')

    fig.clf()

    data = pd.read_csv('corrupt_exp', names=['ave_cmt', 'prob', 'rands', 'rtt', 'retrans'])
    data = data.iloc[:, [1,3]]
    print("loss case interval")
    cout_conf_interval(data)
    plot = sns.pointplot('prob', 'rtt', data=data, dodge=True, join=True)
    fig = plot.get_figure()
    fig.savefig('../plots/p2plot_cor_rtt.png')


    fig.clf()

    data = pd.read_csv('drop_exp', names=['ave_cmt', 'prob', 'rands', 'rtt', 'retrans'])
    data = data.iloc[:, [1,4]]
    print("loss case interval")
    cout_conf_interval(data)
    plot = sns.pointplot('prob', 'retrans', data=data, dodge=True, join=True)
    fig = plot.get_figure()
    fig.savefig('../plots/p2plot_drop_retrans.png')

    fig.clf()

    data = pd.read_csv('corrupt_exp', names=['ave_cmt', 'prob', 'rands', 'rtt', 'retrans'])
    data = data.iloc[:, [1,4]]
    print("loss case interval")
    cout_conf_interval(data)
    plot = sns.pointplot('prob', 'retrans', data=data, dodge=True, join=True)
    fig = plot.get_figure()
    fig.savefig('../plots/p2plot_cor_retrans.png')
