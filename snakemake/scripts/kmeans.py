#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
from sklearn.manifold import MDS
from matplotlib import pyplot as plt
import sklearn.datasets as dt
import seaborn as sns         
from sklearn.metrics.pairwise import manhattan_distances, euclidean_distances
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
## k means to find the best number of group
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans


def k_means_group():
    cost =[]
    for i in range(1, 20):
        kmeans = KMeans(n_clusters = i, max_iter = 500)
        kmeans.fit(coords)

        # calculates squared error
        # for the clustered points
        cost.append(kmeans.inertia_)    
 
    # plot the cost against K values
    fig, ax = plt.subplots(figsize=(10, 10))
    plt.plot(range(1, 11), cost, color ='g', linewidth ='3')
    plt.xlabel("Value of K")
    plt.ylabel("Squared Error (Cost)")
    #plt.show() # clear the plot

    # the point of the elbow is the
    # most optimal value for choosing k
    
    fig.savefig('k_choose.png')   # save the figure to file
    plt.close(fig)    # close the figure window    
    


## with user-defined number of K to generate a plot
def kmeans_plot():
    kmeans = KMeans(n_clusters = k, random_state = 0)
    cluster=kmeans.fit(coords)
   
    fig, ax = plt.subplots(figsize=(10, 10))
    plt.scatter(coords[:,0],coords[:,1], c=kmeans.labels_, cmap='rainbow')
    fig.savefig('k_choose.png')   # save the figure to file
    plt.close(fig)    # close the figure window    
    

def main():
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', required = True)  ## input is the netMPHpan xlsx for multiple sequence but single allel
    parser.add_argument('-k', '--ngroup', required = True) ## user choose number of K
    #parser.add_argument('-o', '--output', required=True) ## output is the mds coordiant
    args = parser.parse_args()
    #print(args.input, 'is input, ', args.output, 'output.', args.ngroup, "user defined groups")
    ## get data that generated a full matrix from distance dataframe
    data = fullmatrix(data1)
    ## perform MDS
    mds = MDS(n_components=2, dissimilarity="precomputed", random_state=0)## create mds module
    results = mds.fit(data)
    coords = results.embedding_
    strain = data.columns
    df_mds=pd.DataFrame({'strain':strain, 'mds1':coords[:, 0], 'mds2': coords[:, 1]})

    


main()


# In[ ]:





# In[ ]:




