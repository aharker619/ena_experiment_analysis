#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 14 15:58:55 2018

@author: Alyssa
"""
#compare fluorescence intensity to area of cells

import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

def set_folders(path, element):
    '''
    Each folder is sorted by treatment
    '''
    # Go through each folder and get data to calulcate mean and stdev
    folders = [('Dimer/', 'comb_results_di.csv'), ('Trimer/', 
               'comb_results_tri.csv'), ('Tetramer/', 'comb_results_tet.csv')]
    f, axs = plt.subplots(nrows=1, ncols=3, sharex = True, 
                          sharey = True, figsize = (6,4))
    count = 0
    for folder, means in folders:
        path_csv = ''.join([path, "Fluors/", means])
        df = pd.read_csv(path_csv)
        y = df['Area']
        x = df.Mean - df.mean_b
        # print out pearson correlation
        pc = pearsonr(x, y)
        print(folder, pc)
        axs[count].scatter(x, y)
        #sns.regplot(x = x, y = y, ax = axs[count], fit_reg = False)
        name = folder.split('/')[0]
        axs[count].set_title(name)
        axs[count].set_xlabel('Mean Fluorescence')
        axs[count].set_ylabel('Area')
        count += 1
    #axs[0].set_ylabel('Area')
    f.tight_layout()
    plt.show()
    #f.savefig('/RNAi_Results/perim_scatter_intBG_3.pdf')
    

def go():
    '''
    Run the program
    Can change element to compare: "F/P" is default for filopodia density
    '''
    # Get all files in path directory, change path here
    path = "/RNAi_Results/"
    element = "F/P"
    set_folders(path, element)
    #get_plots(all_data, element, save, talk_figure)



if __name__ == '__main__':
   go()