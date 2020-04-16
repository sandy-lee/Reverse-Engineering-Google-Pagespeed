#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 16:28:20 2020

@author: sandylee
"""


def correlation_matrix(df = None):
    
    """
    This returns a nicely formatted correlation matrix using Seasborn when a Pandas DataFrame is passed in
    """
    
    import seaborn as sns
    import matplotlib.pyplot as plt
    import numpy as np

    sns.set(style="white")
    corr = df.corr()
    mask = np.triu(np.ones_like(corr, dtype=np.bool))
    f, ax = plt.subplots(figsize=(11, 9))
    cmap = sns.diverging_palette(240, 10, as_cmap=True)
    heatmap = sns.heatmap(corr, mask=mask, cmap=cmap, vmax=.3, center=0,
              square=True, linewidths=.5, cbar_kws={"shrink": .5})
    return(heatmap)

        
 