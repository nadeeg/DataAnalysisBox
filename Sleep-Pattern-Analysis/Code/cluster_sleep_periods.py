"""
AUTHOR  : TAN WEI JIE AMOS
EMAIL   : amos.tan.2014@sis.smu.edu.sg
DATE    : 03-08-2016
TITLE   : cluster_sleep_periods.py
"""

###########################################IMPRORTS#########################################
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
import helper_adl as h
import eps_min_pts as eps_And_MinPts
from sklearn.cluster import DBSCAN
from sklearn.neighbors import DistanceMetric
###########################################IMPRORTS#########################################

# Returns output from sklearn DBSCAN method 
def dbscan(eps, min_pts, X, metric='precomputed'):
    db = DBSCAN(eps, min_pts, metric)
    db.fit(X)
    return db.labels_, db.components_, db.core_sample_indices_


def return_clusters(file_name):
    # Get dataframe containing readings from sensor reading, exclude 
    df = pd.read_csv(file_name, delimiter=',', usecols=[x for x in range(0,7)])

    #print(df.head())

    # X is a distance matrix.
    # Set 'X1' as sleep_start timings
    X1,X1_rad_series = h.get_x_from_df(df['time_start'])

    # Set 'X2' as sleep_end timings
    X2,X2_rad_series = h.get_x_from_df(df['time_end'])

    #print(X1_rad_series)
    #print(X2_rad_series)
    # Create X3 DataFrame from X1 and X2
    # Data has already been processed from 'get_x_from_df'; Values are in radian, and shortest distances
    # to each point have been assigned.
    X3 = pd.DataFrame()
    X3['sleep_start'] = X1_rad_series
    X3['sleep_end'] = X2_rad_series

    # Generate eps and minpts values
    distance = DistanceMetric.get_metric('euclidean')
    print(X3)
    X3_dist_matrix = distance.pairwise(X3)
    print(X3_dist_matrix)
    print(X3_dist_matrix.shape)
    #print(len(X3_dist_matrix.flatten()))
    eps_X3, min_pts_X3 = eps_And_MinPts.knee_calculate_eps_minPts(X3_dist_matrix)

    # DBSCAN
    db3 = DBSCAN(eps_X3, min_pts_X3, metric='precomputed').fit(X3_dist_matrix)
    X3_label, X3_components, X3_csi = db3.labels_, db3.components_, db3.core_sample_indices_

    # Flatten matrix to extract clusters
    X3_matrix = X3.as_matrix().T

    # EXTRACTION OF CLUSTERS
    ###########################################
    output_dict = {
        'cluster':[],
        'std':[],
        'variance':[],
        'centroid':[],
        'start_end':[]
    }
    cluster_dict_ = h.extract_clusters(X3_label, X3_matrix)
    cluster_dict_keys_ = cluster_dict_.keys()
    for key in cluster_dict_keys_:
        cluster = cluster_dict_[key][0]
        output_dict['cluster'].append(np.asscalar(key))
        output_dict['std'].append(h.format_mins(h.radian_to_mins(np.std(cluster))))
        output_dict['variance'].append(h.format_mins(h.radian_to_mins(np.var(cluster))))
        output_dict['centroid'].append(h.format_mins(h.radian_to_mins(np.median(cluster))))
        output_dict['start_end'].append('start')

        cluster = cluster_dict_[key][1]
        output_dict['cluster'].append(np.asscalar(key))
        output_dict['std'].append(h.format_mins(h.radian_to_mins(np.std(cluster))))
        output_dict['variance'].append(h.format_mins(h.radian_to_mins(np.var(cluster))))
        output_dict['centroid'].append(h.format_mins(h.radian_to_mins(np.median(cluster))))
        output_dict['start_end'].append('end')

    return output_dict