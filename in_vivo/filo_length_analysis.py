#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 10:45:59 2018

@author: Alyssa
"""

# 180123
# Analyze matlab results from CellGeo
# calculate average filopodia length depending on cell treatment
# compare for different constraints for length and width of filopodia

import os
import scipy.io as sio
from scipy import stats
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
#from scipy.stats import ttest_ind

def average_filo_per_perimeter(filepath, element):
    """
    Given a matlab result file return average number of filopodia/perimeter
    """
    matdata = sio.loadmat(filepath)
    y_single = matdata[element][0][0]
    return y_single
    
def get_data(path2, files, element):
    """
    Given path and list of files for each file get y and x data and return
    """
    y_singleframe = []
    unit_x = []
    for file in files:
        if file != ".DS_Store" and file != "matlab_5.mat":
            y_single = average_filo_per_perimeter(''.join([path2, file]), element)
            y_singleframe.append(y_single)
            unit_x.append(file)
    y_series = pd.Series(y_singleframe)
    
    return unit_x, y_series

def set_folders(path, element):
    '''
    Given a folder path with subfolders of constant_folders, which then have 
    subfolders of folders, call get_data
    '''
    # These are length_width (opposite of Filotrack order)
    constant_folders = ['6_7/', '6_6/', '6_75/', '55_7/', '7_7/', '7_6/']
    all_data = pd.DataFrame()
    folders = ['ControlAO/','ActinOnly/', 'Dimer/', 'Trimer/', 'Tetramer/']
    for c_folder in constant_folders:
        const = c_folder.split('/')[0]
        # Go through each folder and get data to calulcate mean and stdev
        df_single = pd.DataFrame()
        for folder in folders:
            path2 = ''.join([path, c_folder, folder])
            folder_files = os.listdir(path2)
            x, y_series = get_data(path2, folder_files, element)
            name = folder.split('/')[0]
            data = pd.DataFrame({'constants': np.repeat(const, len(y_series)), 'cells': np.repeat(name, len(y_series)), element: y_series})
            df_single = df_single.append(data)
        all_data = all_data.append(df_single)
    return all_data

def get_plots(all_data, element):
    '''
    Given all data from folders, group and plot into two figures
    '''
    grouped = all_data.groupby('constants')
    fig = plt.figure()
    fig.subplots_adjust(hspace = 0.4, wspace = 0.4)
    for (title, group), i in zip(grouped, range(1, 7)):
        ax = plt.subplot(2, 3, i)    
        ax = sns.boxplot(x = 'cells', y = element, data = group, palette = "Spectral")
        ax = sns.swarmplot(x = 'cells', y = element, data = group, color = "black", size = 4)
        #ax.set_ylim([0, 0.07])
        plt.xticks(rotation = 90) 
        plt.xlabel(title)
    
    fig.set_size_inches(10, 8)
    fig.show()
    fig.savefig('/Test_Constants/diff_const_length')
    
    grouped2 = all_data.groupby('cells')
    fig2 = plt.figure()
    #fig2.subplots(sharey = True)
    fig2.subplots_adjust(hspace = 0.4, wspace = 0.4)
    for (title, group), i in zip(grouped2, range(1, 7)):
        ax = plt.subplot(2, 3, i)    
        ax = sns.boxplot(x = 'constants', y = element, data = group, 
                         palette = "Spectral")
        #ax.set_ylim([0, 0.07])
        plt.xticks(rotation = 90)
        plt.xlabel(title)
    fig2.set_size_inches(10, 8)
    fig2.savefig('/Test_Constants/diff_cells_length')

def get_stat_data(all_data, element):
    '''
    Calculate students ttest on pairwise comparisons
    '''
    grouped = all_data.groupby('constants')
    stat_data = []
    sig_data = []
    for title, group in grouped:
        ao = [group[group['cells'] == 'ActinOnly'][element]]
        cao = [group[group['cells'] == 'ControlAO'][element]]
        rd = [group[group['cells'] == 'Dimer'][element]]
        rtr = [group[group['cells'] == 'Trimer'][element]]
        rtet = [group[group['cells'] == 'Tetramer'][element]]
        all_cells = [('ao', ao), ('cao', cao), ('rd', rd), ('rtr', rtr), ('rtet', rtet)]
        update_cells = [('ao', ao), ('cao', cao), ('rd', rd), ('rtr', rtr), ('rtet', rtet)]
        for name1, cell1 in all_cells:
            for name2, cell2 in update_cells:
                if name1 != name2:
                    #print(name1, name2)
                    stat = stats.ttest_ind(cell1[0], cell2[0], axis = 0, equal_var = False)
                    stat_data.append((title, name1, name2, stat[1]))
                    if stat[1] < 0.05:
                        sig_data.append((title, name1, name2, stat[1]))
            update_cells = update_cells[1:]
    return stat_data, sig_data

def go():
    '''
    Run script
    '''
    # Get all files in path directory, change path here
    path = "/Test_Constants/"
    element = "mL"
    all_data = set_folders(path, element)
    get_plots(all_data, element)
    stat_data, sig_data = get_stat_data(all_data, element)
    return stat_data, sig_data

if __name__ == '__main__':
   go()
    