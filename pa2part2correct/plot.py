import numpy as np
import pandas as pd
import seaborn as sns

if __name__ == '__main__':
    sns.set_style("darkgrid", {"axes.facecolor": ".9"})

    data = pd.read_csv('corrupt_exp', names=['ave_cmt', 'prob', 'rands'])
    data = data.iloc[:, :2]
    plot = sns.pointplot('prob', 'ave_cmt', data=data, dodge=True, join=True)
    fig = plot.get_figure()
    fig.savefig('output_corrupt.png')

    fig.clf()

    data = pd.read_csv('drop_exp', names=['ave_cmt', 'prob', 'rands'])
    data = data.iloc[:, :2]
    plot = sns.pointplot('prob', 'ave_cmt', data=data, dodge=True, join=True)
    fig = plot.get_figure()
    fig.savefig('output_drop.png')
