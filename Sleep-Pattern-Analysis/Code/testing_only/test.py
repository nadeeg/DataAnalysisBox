"""
Test script for dbscan.py
"""

import numpy as np
import dbscan as db
from sklearn.cluster import DBSCAN 
from sklearn.preprocessing import StandardScaler
from math import pi


data = np.genfromtxt('data.csv', delimiter=',')
print("Data input size", len(data))
"""
cluster = db.dbscan(data, 60, 7)

# print to file(s):
for i in cluster.keys():
	file_name = "cluster_" + str(i)
	X = np.array(cluster[i])
	np.savetxt(file_name + '.csv', X, delimiter=',')
"""
"""
Testing with scikit-learn
"""

eps = 60
min_pts = 7
db2 = DBSCAN(eps=((eps / (24*60)) * 2 * pi ), 
	min_samples=min_pts, metric='precomputed')

rad = np.vectorize(db.convert_to_radian)
data_rad = rad(data)
X = data_rad[None,:] - data_rad[:,None]
X[((X > pi) & (X <= (2*pi)))] = X[((X > pi) & (X <= (2*pi)))] -(2*pi)
X[((X > (-2*pi)) & (X <= (-1*pi)))] = X[((X > (-2*pi)) & (X <= (-1*pi)))] + (2*pi) 
X = abs(X)
# print(X)

#fit data
db2.fit(X)
#get labels
labels = db2.labels_
print(labels)
# total there are n clusters + noise in labels. 
# - 1 if -1 exist in labels because -1 is used to denote noise
no_clusters = len(set(labels)) - (1 if -1 in labels else 0)
components = db2.components_
#csi = core sample indices
csi = db2.core_sample_indices_

print('No. Of Clusters: ', no_clusters)
print(len( np.nonzero(labels == 0)[0] ))
print(np.nonzero(labels == 0))
print(len(np.nonzero(labels == 1)[0] ))
# print(components)
# print(csi)
