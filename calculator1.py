#!/usr/bin/env python
# coding: utf-8

# <h1><center>Reconstructing HPGe Detector Waveform Energy</center></h1>

# This notebook will guide you through problems 6 of HW4. Start out by reading the problem descriptions in the main homework assignment before you work through this notebook.
# 
# We have three imports for this assignment. Please do not import any other packages.

# In[2]:


import numpy as np
import pandas as pd
from itertools import combinations
import math


# <h2> Problem 6: Prediction Competition<h2>

# Your task is to modify the `predict` function given below, according to the rules given in the main homework assignment. Remember you can use up to three variables, and your design matrix can have up to five columns. We recommend determining your best prediction rule before implementing the `predict` function. 
# 

# In[865]:


# Use this cell (and add more as needed) to determine your best prediction rule. 
# Then implement the predict function below.
waveforms = pd.read_csv('HPGeData.csv')
waveforms = waveforms[waveforms['Max_Amp'].between(500, 7000)]
waveforms = waveforms[waveforms['tDrift50'].between(40, 100)]
waveforms = waveforms[waveforms['tDrift90'].between(40, 110)]
waveforms = waveforms[waveforms['tDrift100'].between(50, 150)]
waveforms = waveforms[waveforms['blnoise'].between(0, 5)]
waveforms = waveforms[waveforms['tslope'].between(-115, -107)]
X_T = [[1 for i in range(247)], waveforms.get('Max_Amp'), np.log(waveforms.get('blnoise')), abs(waveforms.get('tslope')) ** math.e, waveforms.get('Max_Amp') * waveforms.get('blnoise')]
X = np.transpose(X_T)
inv = np.linalg.inv(X_T@X)
w = list(inv@X_T@np.transpose(list(waveforms.get('Energy'))))
w


# In[866]:


def predict(row):
    '''Function that returns the predicted energy for a given row of the waveform features
    row will be a 1-d array of [Max_Amp, tDrift50, tDrift90, tDrift100, blnoise, tslope]
    please change the return 0 to return predicted energy given these parameters
    '''
    return w[0] + w[1] * row[0] + w[2] * np.log(row[4]) + w[3] * abs(row[5])**math.e + w[4] * (row[0] * row[4])


# Don't modify the `calculate_MSE` function given below. This tests how well your predictions perform on a given dataset.

# In[867]:


def calculate_MSE(df):
    '''Compute MSE of the predictions corresponding to each row of the given dataframe'''
    n = df.shape[0]
    total_squared_error = 0
    for i in np.arange(n):
        predicted = predict(df.iloc[i].drop("Energy"))
        actual = df.iloc[i].get('Energy')
        squared_error = (actual - predicted)**2
        total_squared_error += squared_error
    return total_squared_error/n


# You can test out your predictions on the training dataset provided. We'll also test your predictions on a hidden test dataset.

# In[868]:


waveforms = pd.read_csv('HPGeData.csv')


# In[869]:


# An example prediction
example_row = waveforms.iloc[0].drop("Energy")
predict(example_row)


# In[870]:


print(calculate_MSE(waveforms))


# <h3> To Submit </h3>
# 
# In the top left corner, in the File menu, select Download as Python (.py). 
# 
# You must save your file as `hw4code.py` for the Gradescope autograder to run. Then, upload this file to the assignment called Homework 4 Code on Gradescope. Problems 4b, 4c, and 5 will be autograded, so you don't need to turn in any written explanation for these questions.
