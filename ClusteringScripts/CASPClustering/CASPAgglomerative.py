import time
import matplotlib.pyplot as plt
import numpy as np
import os
import CASP12Utilities as util
from sklearn.cluster import AgglomerativeClustering
from sklearn.neighbors import kneighbors_graph

def agglo(structure, measure1, measure2, values1, values2):

    algorithm = 'agg'

    path = "D:/Dados/casp12/clustering_results/"

    tmp = list(zip(values1, values2))        
    X = np.array(tmp)

    # Create a graph capturing local connectivity. Larger number of neighbors
    # will give more homogeneous clusters to the cost of computation
    # time. A very large number of neighbors gives more evenly distributed
    # cluster sizes, but may not impose the local manifold structure of
    # the data
    knn_graph = kneighbors_graph(X, 10, include_self=False)
    for n_clusters in (3,4,5,6,7,8):
        for connectivity in (None, knn_graph):
            for linkage in ['average','complete','ward']:
                try:
                        #plt.subplot(1, 3, index + 1)
                    plt.xlabel(measure1)
                    plt.ylabel(measure2)

                    model = AgglomerativeClustering(linkage=linkage,
                                                        connectivity=connectivity,
                                                        n_clusters=n_clusters)

                    model.fit(X)
            
                    plt.scatter(X[:, 0], X[:, 1], c=model.labels_,
                                cmap='jet',s=10)

                    plt.axis('on')

                    ce = util.clusterEvaluationNoLabels(X,model.labels_)
                    
                    n = linkage+'_'+str(n_clusters)

                    plt.title("Agglomerative: "+linkage+' '+str(n_clusters))
                    print("Agglomerative: "+linkage+' '+str(n_clusters))
                    util.saveCASPResults(structure, algorithm, n, measure1, measure2, ce)
                    util.saveImage(plt, path+structure+'/', 'plot_'+structure+'_'+measure1+'_'+measure2+'_'+algorithm+'_'+str(n))
                except Exception:
                    pass 


    