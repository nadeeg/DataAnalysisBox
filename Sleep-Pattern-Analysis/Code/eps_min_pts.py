"""
AUTHOR  : TAN WEI JIE AMOS
EMAIL   : amos.tan.2014@sis.smu.edu.sg
DATE    : 03-08-2016
TITLE   : eps_min_pts.py
"""
################ IMPORTS ##################
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
from math import pi
from sklearn.cluster import DBSCAN
################ IMPORTS ##################

"""
Possible improvements:
1. Explore more robust means of identifying the knee-points
2. (1) Maybe can explore vector projection
"""

# Using the 'knee' method of choosing an eps and min pts
def knee_calculate_eps_minPts(distance_matrix):
    # Flatten matrix
    X = distance_matrix.flatten()
    print("3, the flatten X is {}".format(X))

    # Get non-zeros
    X_non_zeros_ = X.nonzero()
    # Mask out non-zeroes
    X_array = X[X_non_zeros_]
    print(min(X_array))
    print("4, the none zeros X Array is {}".format(X_array))
    # Generate histogram
    #hist, bin_edges = np.histogram(X_array,density=False)
    ############################ CHANGE LOG ########################################
    # By Default, the np.histogram will divide the data into 10 bins. so it is around 2.4 hours interval
    # Here, we manualy 
    #################################################################################
    hist, bin_edges = np.histogram(X_array,np.arange(0,2*pi,2*pi/24), density=False)    
    print("the hist is {}".format(hist))
    print("the max hist is {}".format(np.max(hist)))
    print("the target is {}".format(np.where(hist==np.max(hist))))
    print("the bin is {}".format(bin_edges))
    # Arbitrarily select the knee, occasionally it falls in the 2nd or 3rd bin.
    eps = bin_edges[1]
    #print("eps is {}".format(eps))
    count_minPts = []
    for distance in distance_matrix:
        count_minPts.append(len(np.where(distance <= eps)[0]))
        #print("count_minPts is {}".format(count_minPts))
        #print("distance_matrix shape is {}".format(distance_matrix.shape))       
        #print("count_minPts is {}".format(count_minPts))
        #print("count_minPts lenth is {}".format(len(count_minPts)))    
        # Generate histogram for minpts
    hist_mp, bind_edges_mp = np.histogram(count_minPts, density=False)

        # Arbitrarily select the max bin_edge value.
        # TODO: Find a better way to select the minpts value
    minPts = np.max(count_minPts)
        #minPts = np.median(count_minPts)

        # Return eps and minPts
    return eps, minPts




