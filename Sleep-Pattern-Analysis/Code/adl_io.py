"""
AUTHOR  : TAN WEI JIE AMOS
EMAIL   : amos.tan.2014@sis.smu.edu.sg
DATE    : 03-08-2016
TITLE   : adl_io.py
"""

from os import listdir
from os.path import isfile, join
import pandas as pd
import numpy as np
import cluster_sleep_periods as csp

def sleep_to_cluster_aggregate(path='../Data/sleep/sleep_raw/'
    ,output_path='../Data/sleep/sleep_agg_results/'):
    """
    This method writes cluster results to csv from sleep-aggregate csv files. 
    e.g (sleep-aggregate_2015-07_S001.csv)
    """

    files = [f for f in listdir(path) if isfile(join(path, f))]
    file_count = len(files)
    files_with_error = []

    # hacky code to help populate dictionary to be use in 'Sleep trends notebook'
    # comment out when not needed
    # frame_list to contain all the dataframes for concatenation
    frame_list = []
    for f in files:
        month = f[16:23]
        id = f[24:28]
        try:
            output_dict = csp.return_clusters(path + f)
            output_dict['id'] = id
            output_dict['month'] = month
            df = pd.DataFrame(output_dict)
            # print(df.columns)
            df = df[['id','month','cluster','centroid','std','variance','start_end']]
            # Adding dataframes to frame_list
            frame_list.append(df)
            df.to_csv(output_path+'cluster_'+f)
        except ValueError:
            file_count -= 1
            files_with_error.append(f)
            raise ValueError
    print('Files parsed successfully ', file_count)
    print('Files with errors: ', len(files_with_error))
    return frame_list


sleep_to_cluster_aggregate()