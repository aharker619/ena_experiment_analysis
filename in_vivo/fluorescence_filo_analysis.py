#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 13 13:37:14 2018

@author: Alyssa
"""

# 180313
# compare fluorescence of cells versus filopodia density

import os
import scipy.io as sio
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import pearsonr


def average_filo_per_perimeter(filepath, element):
    """
    Given a matlab result file return average number of filopodia/perimeter if F/P
    Else return the element specified in go()
    """
    matdata = sio.loadmat(filepath)
    if element == "F/P":
        y_single = matdata['N'][0][0] / (matdata['Per'][0][0] * .13)
    else:
        y_single = matdata[element][0][0]
    
    return y_single
    
def get_data(path2, files, element, df):
    """
    Given path and list of files for each file get y and x data and return
    """
    y_singleframe = []
    unit_x = []
    for file in files:
        if file != ".DS_Store":
            y_single = average_filo_per_perimeter(''.join([path2, file]), element)
            y_singleframe.append(y_single)
            # get mean fluorescence background subtracted
            fluor = (df[df.code == file]['Mean'].values[0]) - (
                    df[df.code == file]['mean_b'].values[0])
            unit_x.append(fluor)
    y_series = pd.Series(y_singleframe)
    x_series = pd.Series(unit_x)
    
    return x_series, y_series

def set_folders(path, element):
    '''
    '''
    # Go through each folder and get data to calulcate mean and stdev
    # select the correct group of folders 
    #folders = [('ControlAO/', 'actin_ca.csv'), ('ActinOnly/', 'actin_ao.csv'), 
    # ('Dimer/', 'actin_di.csv'), ('Trimer/', 
    #'actin_tri.csv'), ('Tetramer/', 'actin_tet.csv')]
    folders = [('Dimer/', 'comb_results_di.csv'), ('Trimer/', 
               'comb_results_tri.csv'), ('Tetramer/', 'comb_results_tet.csv')]
    # change number of columns
    f, axs = plt.subplots(nrows=1, ncols=3, sharex = True, sharey = True, 
                          figsize=(6,4))
    count = 0
    for folder, means in folders:
        # Change Fluors or Actin depending on mcherry or actin fluorescence
        path_csv = ''.join([path, "Flours/", means])
        df = pd.read_csv(path_csv)
        path2 = ''.join([path, folder])
        folder_files = os.listdir(path2)
        x, y = get_data(path2, folder_files, element, df)
        # print out pearson correlation
        pc = pearsonr(x, y)
        print(folder, pc)
        #axs[count].scatter(x, y)
        sns.regplot(x = x, y = y, ax = axs[count], fit_reg = False)
        name = folder.split('/')[0]
        axs[count].set_title(name)
        axs[count].set_xlabel('mcherry Mean')
        axs[count].set_ylabel('Filopodia Density')
        count += 1
    f.tight_layout()
    #axs[0].set_ylabel('Filopodia Density')
    plt.show()
    #f.savefig('/RNAi_Results/actin_reg_BGintensity_3.pdf')


def get_plots(all_data, element, save, talk_figure):
    '''
    Given filopodia data, plot fluorescence mean vs filopodia density
    '''
    sns.set(style = 'ticks', rc = {'figure.figsize': (8,6)})
    dot_color = "black"
    g = sns.boxplot(x = 'cells', y = element, data = all_data, 
                    palette = "colorblind")
    g = sns.swarmplot(x = 'cells', y = element, data = all_data, 
                      color = dot_color, size = 4)
    fig = g.get_figure()
    if save:
        fig.savefig('/RNAi_Results/actin_fluor_3.pdf', 
                    transparent=True)

def go():
    '''
    '''
    # Get all files in path directory, change path here
    path = "/RNAi_Results/"
    element = "F/P"
    set_folders(path, element)
    #get_plots(all_data, element, save, talk_figure)



if __name__ == '__main__':
   go()
    