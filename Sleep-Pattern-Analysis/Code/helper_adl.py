"""
AUTHOR  : TAN WEI JIE AMOS
EMAIL   : amos.tan.2014@sis.smu.edu.sg
DATE    : 03-08-2016
TITLE   : helper_adl.py
"""

###########################################IMPRORTS#########################################
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
from sklearn.cluster import DBSCAN
###########################################IMPRORTS#########################################


# To return value in mins / total mins in a day
def to_mins(x):
	x = pd.Timestamp(x)
	year = x.year
	month =  x.month
	day = x.day
    # (liming) return the minute number of the day
	return (x.value - pd.Timestamp(str(year)+'-'+str(month)+'-'+str(day)).value) / (60 * (10**9))

# To return total mins returned as hh:mm format
def format_mins(mins):
	return '{:02d}:{:02d}'.format(*divmod(mins,60))

# Helper method to covert radian back to minutes
def radian_to_mins(x):
  
	return int(round((x / 2 / np.pi) * (24 * 60))) 

# Helper method to convert values in minutes / total minutes in a day to radian
def convert_to_radian(x):

    return ((x / (24*60)) * 2 * np.pi)

# Get all the sleep intervals based on bedroom only data
def get_df_sleep_intervals(df):
    
    df_sleep = pd.DataFrame(columns=('sleep_start', 'sleep_end', 'sleep_duration'))
    
    sleep_start = None
    sleep_end = None
    
    for index, row in df.iterrows():
        if (row['bedroom_only'] and sleep_start is None):
            sleep_start = row['date']
        elif ((not row['bedroom_only']) and (not sleep_start is None)):
            sleep_end = row['date']
            sleep_duration = sleep_end - sleep_start
        
            payload = {}
            payload['sleep_start'] = sleep_start
            payload['sleep_end'] = sleep_end
            payload['sleep_duration'] = sleep_duration
            df_sleep = df_sleep.append(payload, ignore_index=True)
        
            sleep_start = None
            sleep_end = None
            
    # already reached end of file, sleep was snp.pilled over from last day to next month
    if not sleep_start is None:        
        sleep_end = df['date'].iloc[-1]
        sleep_duration = sleep_end - sleep_start
        
        payload = {}
        payload['sleep_start'] = sleep_start
        payload['sleep_end'] = sleep_end
        payload['sleep_duration'] = sleep_duration
        df_sleep = df_sleep.append(payload, ignore_index=True)
        
        sleep_start = None
        sleep_end = None
          
    # TODO: handle first and last entry in a more appropriate manner 
    # df_sleep.drop(df_sleep.head(1).index, inplace=True)
        
    # print(df_sleep.head())  
    # print(df_sleep.tail())  
    return df_sleep

# Returns a distance matrix (a numpy array)
def get_x_from_df(series):
    
    # Vectorizing to_mins and to_radian functions
    tmin = np.vectorize(to_mins)
    trad = np.vectorize(convert_to_radian)

    #print(tmin(series))

    # Converting series of timestamp -> minutes / total minuites in a day -> radian
    input_rad = trad(tmin(series))
    #print(input_rad)

    # Convert time to rad points 
    #print(type(input_rad))
    #print(input_rad)
    #print(input_rad[None,:])  
    #print(input_rad[:,None])
    #print(type(input_rad[:,None]))
    X = input_rad[None,:] - input_rad[:,None]
    #np.set_printoptions(precision=1)
    #print(X)
    # Assign shortest distance to each point
    X[(( X > np.pi ) & (X <= (2*np.pi)))] = X[((X > np.pi) & (X <= (2*np.pi)))] -(2*np.pi)
    X[((X > (-2*np.pi)) & (X <= (-1*np.pi)))] = X[((X > (-2*np.pi)) & (X <= (-1*np.pi)))] + (2*np.pi) 
    X = abs(X)

    return X, input_rad

# Extract clusters
def extract_clusters(labels, data):
	cluster_dict_ = {}
	clusters = set(labels)
	# print(data.shape)
	for k in clusters:
		if k != -1:
			indices_of_k_, = np.where(labels == k)
			cluster_dict_[k] = data.take(indices_of_k_,axis=1).reshape(2,len(indices_of_k_))
	return cluster_dict_

		
