from sklearn import datasets
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
from sklearn.cluster import KMeans


df = datasets.load_iris()
y = df.target
yframe=pd.DataFrame(y)
dfr = pd.DataFrame(data=df.data, 
                  columns=df.feature_names)
dfr["target"] = yframe
dfr


kmeans_model =KMeans(n_clusters=3)
y_kmeans = kmeans_model.fit(dfr[['sepal length (cm)','target']])
dfr['kmeans_3']=kmeans_model.labels_
dfr

plt.scatter(x=dfr['sepal length (cm)'],y=dfr['target'],c = dfr['kmeans_3'])


#Intrinsic Method
from sklearn.metrics import silhouette_score
silhouette_score(dfr[['sepal length (cm)','target']], dfr['kmeans_3'], metric = 'euclidean')


#Adjusted Rand Index
from sklearn.metrics.cluster import adjusted_rand_score
adjusted_rand_score(df['target'], dfr['kmeans_3'])


#Mutual Information
from sklearn.metrics.cluster import normalized_mutual_info_score
normalized_mutual_info_score(df['target'], dfr['kmeans_3'])