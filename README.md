This repository contains analysis for the in vivo portion of my Ena/VASP project. 

The in_vivo folder contains scripts and MATLAB results from CellGeo analysis
Citation for CellGeo: Tsygankov, D., Bilancia, C. G., Vitriol, E. A., Hahn, K. M., Peifer, M., 
and Elston, T. C. (2014). CellGeo: A computational platform for the analysis of shape changes 
in cells with complex geometries. J Cell Biol 204, 443–460.

To analyze and plot the filopodia density (filopodia count / perimeter in microns, F/P) use filo\_cell\_analysis.py. 
This uses MATLAB results stored in ActinOnly, ControlAO, Dimer, Trimer, Tetramer folders within RNAi\_results.

To analyze and plot the difference in filopodia density using different parameters specified in 
CellGeo use filo\_const\_analysis.py. This uses MATLAB results stored in 6\_6, 6\_7, 6\_75, 
7\_6, 7\_7, 55\_7 folders within Test_Constants folder. These different folders specify the length\_width values
where 75 and 55 are 7.5 and 5.5 respectively. 

To analyze and plot the difference in filopodia length using different parameters specified in 
CellGeo use filo\_length\_analysis.py. This also uses MATLAB results stored in 6\_6, 6\_7, 6\_75, 
7\_6, 7\_7, 55\_7 folders within Test_Constants folder but calculates the mean length of filopodia (mL).

To analyze and plot the correlation between cell area and fluorescence intensity of either GFP-actin or
mcherry-Ena use area\_v\_intensity.py. To analyze and plot the correlation between filopodia
density and fluorescence intensity use fluorescence\_filo\_analysis.py. These uses fluorescence 
intensities measured by imageJ of either GFP-actin (in Actin folder) or mcherry-Ena (in Fluors folder).