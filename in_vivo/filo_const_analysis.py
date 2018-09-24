# Compare different filopodia density depending on categorization values for filopodia
# Change length/width parameters for classifying filopodia, see if result changes

import os
import scipy.io as sio
from scipy import stats
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def average_filo_per_perimeter(filepath):
    """
    Given a matlab result file return average number of filopodia/perimeter
    """
    matdata = sio.loadmat(filepath)
    y_single = matdata['N'][0][0] / matdata['Per'][0][0]
    return y_single
    
def get_data(path2, files):
    """
    Given path and list of files for each file get y and x data and return for plot
    """
    y_singleframe = []
    unit_x = []
    for file in files:
        if file != ".DS_Store":
            y_single = average_filo_per_perimeter(''.join([path2, file]))
            y_singleframe.append(y_single)
            unit_x.append(file)
    y_series = pd.Series(y_singleframe)
    
    return unit_x, y_series

# Get all files in path directory, change to correct folder
path = "/Test_Constants/"
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
        x, y_series = get_data(path2, folder_files)
        name = folder.split('/')[0]
        data = pd.DataFrame({'constants': np.repeat(const, len(y_series)), 
                             'cells': np.repeat(name, len(y_series)), 
                             'F/P': y_series})
        df_single = df_single.append(data)
    all_data = all_data.append(df_single)

grouped = all_data.groupby('constants')
fig = plt.figure()
fig.subplots_adjust(hspace = 0.4, wspace = 0.4)
for (title, group), i in zip(grouped, range(1, 7)):
    ax = plt.subplot(2, 3, i)    
    ax = sns.boxplot(x = 'cells', y = 'F/P', data = group, palette = "Spectral")
    ax.set_ylim([0, 0.07])
    plt.xticks(rotation = 90) 
    plt.xlabel(title)
    # if you want specific data points use swarmplot
    #ax = sns.swarmplot(x = 'cells', y = 'F/P', data = group, color = "black", size = 4)

fig.set_size_inches(10, 8)
fig.savefig('/Test_Constants/diff_const.png')
fig.show()


grouped2 = all_data.groupby('cells')
fig2 = plt.figure()
#fig2.subplots(sharey = True)
fig2.subplots_adjust(hspace = 0.4, wspace = 0.4)
for (title, group), i in zip(grouped2, range(1, 7)):
    ax = plt.subplot(2, 3, i)    
    ax = sns.boxplot(x = 'constants', y = 'F/P', data = group, palette = "Spectral")
    ax.set_ylim([0, 0.07])
    plt.xticks(rotation = 90)
    plt.xlabel(title)
fig2.set_size_inches(10, 8)
fig2.savefig('/Test_Constants/diff_cells.png')

stat_data = []
sig_data = []
for title, group in grouped:
    ao = [group[group['cells'] == 'ActinOnly']['F/P']]
    cao = [group[group['cells'] == 'ControlAO']['F/P']]
    rd = [group[group['cells'] == 'Dimer']['F/P']]
    rtr = [group[group['cells'] == 'Trimer']['F/P']]
    rtet = [group[group['cells'] == 'Tetramer']['F/P']]
    all_cells = [('ao', ao), ('cao', cao), ('rd', rd), ('rtr', rtr), ('rtet', rtet)]
    update_cells = [('ao', ao), ('cao', cao), ('rd', rd), ('rtr', rtr), ('rtet', rtet)]
    for name1, cell1 in all_cells:
        for name2, cell2 in update_cells:
            if name1 != name2:
                stat = stats.ttest_ind(cell1[0], cell2[0], axis = 0, equal_var = False)
                stat_data.append((title, name1, name2, stat[1]))
                if stat[1] < 0.05:
                    sig_data.append((title, name1, name2, stat[1]))
        update_cells = update_cells[1:]
    
    

