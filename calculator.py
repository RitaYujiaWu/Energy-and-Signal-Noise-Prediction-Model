#!/usr/bin/env python
# coding: utf-8

# <h1><center>Classifying Neutrino Signal from Noise in HPGe Detector</center></h1>

# This notebook will guide you through the second extra credit opportunity. Start out by reading the problem descriptions in the main homework assignment before you work through this notebook.
# 
# We have three imports for this assignment. Please do not import any other packages.

# In[1]:


import numpy as np
import pandas as pd
from itertools import combinations


# <h2> Problem 6: Prediction Competition<h2>

# Your task is to modify the `predict` function given below. 
# 

# In[2]:


waveforms = pd.read_csv('training_classification.csv')
waveforms = waveforms[waveforms['Current_Amplitude'].between(0.0225, 0.04)]
waveforms = waveforms[waveforms['tDrift50'].between(20, 140)]
waveforms = waveforms[waveforms['tDrift90'].between(25, 150)]
waveforms = waveforms[waveforms['tDrift100'].between(50, 180)]
waveforms = waveforms[waveforms['blnoise'].between(0, 7)]
waveforms = waveforms[waveforms['tslope'].between(-115, -110)]
waveforms = waveforms[waveforms['Energy'].between(500, 2700)]


# In[3]:


# column_names = waveforms.columns.tolist()
# for name in column_names:
#     waveforms.plot(kind = 'scatter', x = name, y = 'Energy')


# In[4]:


def cal(f, c):
    parameters = {}
    for i in [0.0,1.0]:
        f_c = f[c == i]
        parameters[i] = {'mean': f_c.mean(axis=0), "std": f_c.std(axis=0)}
    return parameters


# In[5]:


f = np.array(waveforms.drop('Label', axis = 1).values)
c = np.array(waveforms.get('Label'))
parameter = cal(f, c)


# In[6]:


def pdf_e(f, mean, std):
    lambd = 1/(mean - std)
    return lambd * np.exp(-lambd * f)


# In[7]:


def predict(row):
    '''Function that returns the predicted score for a given row of the waveform features
    row will be a 1-d array of [tDrift50, tDrift90, tDrift100, blnoise, tslope, Energy, Current_Amplitude]
    please change the return 0 to return a prediction score where:
    * Higher score means the data point is more likely to be a signal (label 1)
    * Lower score means the data point is more likely to be a noise (label 0)
    Note the score doesn't have to be between 0 and 1
    '''
    of_01 = []
    for i in [0.0, 1.0]:
        prior = np.sum(c == i) / len(c)
        likelihood_e = pdf_e(row, parameter[i]['mean'], parameter[i]['std'])
        likeli = (likelihood_e[0] + 0.1) * (likelihood_e[3] + 6) * (likelihood_e[4] + 5) * (likelihood_e[6] + 4) \
    / (likelihood_e[2] + 0.1)
        posterior = prior * likeli
        of_01.append(posterior)
    return (of_01[1] + 1) / ((of_01[0]) ** 2)


# Don't modify the functions given below. This tests how well your predictions perform on a given dataset.

# In[8]:


def roc_auc(label, score):
    score = np.array(score)
    label = np.array(label)
    dsize = len(score)
    minscore = min(score)
    maxscore = max(score)
    if minscore == maxscore:
        return 0.5
    tpr = []
    fpr = []
    sigscore = score[label==1]
    bkgscore = score[label==0]
    for thr in np.linspace(minscore,maxscore,10000):
        tpr.append(np.sum(sigscore>=thr)/len(sigscore))
        fpr.append(np.sum(bkgscore>=thr)/len(bkgscore))
    
    return np.trapz(tpr,1-np.array(fpr))


# In[9]:


def calculate_AUC(df):
    '''Compute ROC_AUC_score of the predictions corresponding to each row of the given dataframe'''
    n = df.shape[0]
    total_squared_error = 0
    pred_array = []
    label_array = np.array(df.get('Label'))
    for i in np.arange(n):
        pred_array += [predict(df.iloc[i].drop('Label'))]
    return roc_auc(label_array, pred_array)


# You can test out your predictions on the training dataset provided. We'll also test your predictions on a hidden test dataset.

# In[10]:


waveforms = pd.read_csv('training_classification.csv')


# In[11]:


# An example prediction
example_row = waveforms.iloc[0].drop("Label")
predict(example_row)


# In[12]:


print(calculate_AUC(waveforms))


# <h3> To Submit </h3>
# 
# In the top left corner, in the File menu, select Download as Python (.py). 
# 
# You must save your file as `calculator.py` for the Gradescope autograder to run.
