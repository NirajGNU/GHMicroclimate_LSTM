from src.exception import CustomException
from src.logger import logging

import os
import pickle
import numpy as np



from matplotlib import pyplot as plt
#from IPython.core.pylabtools import figsize
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import seaborn as sns 

def timeseries(x_axis, y_axis, x_label, y_lable, title):
    plt.figure(figsize=(10,6))
    plt.plot(x_axis, y_axis, color='black')
    plt.xlabel(x_label,{ 'fontsize': 14})
    plt.ylabel(y_lable,{ 'fontsize': 14})
    plt.title(title)
    plt.show()
    
def plot_histogram(x):
    plt.hist(x, bins=20, color='blue', alpha=0.7, edgecolor='black')
    plt.title("Histogram of '{var_name}'".format(var_name = x.name))
    plt.xlable('Value')
    plt.ylabel('Frequency')
    plt.show()
    
def replace_missing(attributes):
    return attributes.fillna(attributes.median())

def replace_outliers(attribute):
    up_b = attribute.mean() + 2*attribute.std()
    low_b = attribute.mean() - 2*attribute.std()
    attribute = attribute.apply(lambda x: x if low_b < x < up_b else np.nan)
    return replace_missing(attribute)

def timeseries_unidataset(target_feature, time_steps=1):
    Xs, ys = [], []
    for i in range(len(target_feature)-time_steps):
        v = target_feature[i:i+time_steps, :]
        Xs.append(v)
        ys.append(target_feature[i+time_steps])
    return np.array(Xs), np.array(ys)

def timeseries_multidataset(Input_feature, target_feature, time_steps=1):
    Xs, ys = [], []
    for i in range(len(Input_feature)-time_steps):
        v = Input_feature[i:i+time_steps, :]
        Xs.append(v)
        ys.append(target_feature[i+time_steps])
    return np.array(Xs), np.array(ys)


    
def save_object(filepath, object):
    try:
        dir_path = os.path.dirname(filepath)
        os.makedirs(dir_path, exist_ok = True)
        
        with open(filepath, "wb") as file_obj:
            pickle.dump(object, file_obj)
    
    except Exception as e:
        raise CustomException
    