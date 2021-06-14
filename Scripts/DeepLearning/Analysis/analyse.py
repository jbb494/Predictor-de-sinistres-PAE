from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import OneHotEncoder

import pandas as pd
import numpy as np

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, GRU, Dropout, LSTM

import tensorflow.keras.losses as losses

import matplotlib.pyplot as plt
import tensorflow as tf
import tensorflow_docs.plots as plotting
from functools import reduce
import os
import json


def plot_hist(history, metric: str):
    plt.xticks(np.linspace(1, len(history[metric].keys()), 8, dtype=np.int))
    plt.plot(history[metric].keys(), history[metric].values())
    plt.title(metric)
    plt.show()


def dual_plot_hist(history, metric1: str, metric2: str):
    plt.grid()
    plt.xticks(np.linspace(1, len(history[metric1].keys()), 8, dtype=np.int))
    plt.plot(history[metric1].keys(), history[metric1].values(), label=metric1)
    plt.plot(history[metric2].keys(), history[metric2].values(), label=metric2)
    plt.legend()
    plt.show()


def analyze(path_experiments='../MultiModels/Experiments/', path_metadata='../MultiModels/Metadata/'):
    directories = os.listdir(path_experiments)
    score_id_val_loss = {}
    score_id_loss = {}

    for dir in directories:
        with open(f'{path_experiments}/{dir}/hist.json', 'r') as hist_f:
            history = json.load(hist_f)
        metric_function = lambda metric: np.mean(list(history[metric].values())[-10:])
        score_id_val_loss[dir] = metric_function('val_loss')
        score_id_loss[dir] = metric_function('loss')

    directories.sort(key=lambda dir: score_id_val_loss[dir], reverse=True)
    for dir in directories:
        with open(f'{path_experiments}/{dir}/hist.json', 'r') as hist_f:
            history = json.load(hist_f)
        with open(f'{path_metadata}/{dir}.json', 'r') as meta_f:
            metadt = json.load(meta_f)
            title = metadt["LabelName"]
        plt.title(title)
        dual_plot_hist(history, 'loss', 'val_loss')
        plt.title(title)
        dual_plot_hist(history, 'accuracy', 'val_accuracy')



def main():
    path_input='../MultiModels/ExperimentsBinaryThreeDays'
    analyze(path_input)


if __name__ == "__main__":
    main()


