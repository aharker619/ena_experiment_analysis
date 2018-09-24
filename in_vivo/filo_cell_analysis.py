# 180111
# Analyze matlab results from CellGeo
# calculate average filopodia per perimeter
# get boxplots and stats for results

import os
import scipy.io as sio
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind

def average_filo_per_perimeter(filepath, element):
    """
    Given a matlab result file return average number of filopodia/perimeter
    """
    matdata = sio.loadmat(filepath)
    if element == "F/P":
        num_filo = matdata['N'][0][0]
        perim = matdata['Per'][0][0] * .13
        y_single = (num_filo / perim) * 100
        #print(filepath, y_single, num_filo, perim)
    else:
        y_single = matdata[element][0][0]
    
    return y_single
    
def get_data(path2, files, element):
    """
    Given path and list of files for each file get y and x data and return
    """
    y_singleframe = []
    unit_x = []
    for file in files:
        if file != '.DS_Store':
            y_single = average_filo_per_perimeter(''.join([path2, file]), element)
            y_singleframe.append(y_single)
            unit_x.append(file)
    y_series = pd.Series(y_singleframe)
    
    return unit_x, y_series

def set_folders(path, element):
    '''
    '''
    # Go through each folder and get data to calulcate mean and stdev
    folders = ['ControlAO/','ActinOnly/', 'Dimer/', 'Trimer/', 'Tetramer/']
    all_data = pd.DataFrame()
    for folder in folders:
        path2 = ''.join([path, folder])
        folder_files = os.listdir(path2)
        x, y_series = get_data(path2, folder_files, element)
        name = folder.split('/')[0]
        data = pd.DataFrame({'cells': np.repeat(name, len(y_series)), 
                              element: y_series, 'movie': x})
        all_data = all_data.append(data)
    
    return all_data

def get_stat_data(data, element):
    '''
    Calculate student ttest comparing element for cells
    '''
    stat_data = []
    sig_data = []
    cao = data[data['cells'] == 'ControlAO'][element]
    ao = data[data['cells'] == 'ActinOnly'][element]
    rd = data[data['cells'] == 'Dimer'][element]
    rtr = data[data['cells'] == 'Trimer'][element]
    rtet = data[data['cells'] == 'Tetramer'][element]
    all_cells = [('ao', ao), ('cao', cao), ('rd', rd), ('rtr', rtr), ('rtet', rtet)]
    update_cells = [('ao', ao), ('cao', cao), ('rd', rd), ('rtr', rtr), ('rtet', rtet)]
    for name1, cell1 in all_cells:
        for name2, cell2 in update_cells:
            if name1 != name2:
                stat = ttest_ind(cell1, cell2, equal_var = False)
                stat_data.append((name1, name2, stat[1]))
                if stat[1] < 0.05:
                    sig_data.append((name1, name2, stat[1]))
        update_cells = update_cells[1:]
    print(sig_data)
    return stat_data, sig_data


def get_plots(all_data, element, save, talk_figure):
    '''
    Given filopodia data, plot per cell condition
    '''
    if talk_figure:
        sns.set_style("ticks", {"xtick.major.size":8, "ytick.major.size":8})
        sns.set_context("talk")
        sns.set_style("darkgrid")
        dot_color = "black"
        g = sns.boxplot(x = 'cells', y = element, data = all_data, palette = "colorblind")
        g.set_xticklabels(["Control", "RNAi Actin Only", "RNAi Dimer", "RNAi Trimer", 
                           "RNAi Tetramer"])
        g.set_ylabel("Filopodia Density (count/pixel)")
        g.set_xlabel("")

    else:
        sns.set(style = 'ticks', rc = {'figure.figsize': (8,6)})
        dot_color = "black"
        g = sns.boxplot(x = 'cells', y = element, data = all_data, palette = "colorblind")
    g = sns.swarmplot(x = 'cells', y = element, data = all_data, color = dot_color, 
                      size = 4)
    fig = g.get_figure()
    if save:
        fig.savefig('/RNAi_Results/boxplot_3solidsets.pdf', transparent=True)

def go():
    '''
    '''
    # Get all files in path directory, change path here
    path = "/RNAi_Results/"
    element = "F/P"
    save = False
    talk_figure = False
    all_data = set_folders(path, element)
    get_plots(all_data, element, save, talk_figure)
    stat_data, sig_data = get_stat_data(all_data, element)
    #print(all_data.head())
    return all_data, stat_data, sig_data

if __name__ == '__main__':
   go()
    
