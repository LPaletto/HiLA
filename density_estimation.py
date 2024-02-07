import argparse
import torch
import src
import pandas as pd
from src.metrics import PerformanceDisplay
from src.dataset2 import WebOfScience, DBPedia, AmazonHTC, Books
from src.scoring_functions import PriorScoresZeroShooting
from src.encoders import ZeroShooterZSTC, ZeroshooterBART_2, ZeroshooterTARS
from src.utils import FileIO
from globals import Globals, Paths

from sentence_transformers.util import cos_sim
import numpy as np

from sklearn.neighbors import KernelDensity
def dist_mia(x):
    dist = cos_sim(x,x).numpy()
    return dist
def dist_comp(mat, fai_cos=False): #l'input non deve essere per forza matrice
    if fai_cos:
        mat = dist_mia(mat)
    #return (mat.sum()-mat.diagonal().sum())/(mat.shape[0]**2-mat.shape[0])
    tutted = np.unique(mat)
    tutted = tutted[tutted<0.99]
    model = KernelDensity(bandwidth=2, kernel='gaussian')
    tutted = tutted.reshape((len(tutted), 1))
    model.fit(tutted)
    values = np.array([value for value in np.linspace(0,0.8)])
    values = values.reshape((len(values), 1))
    probabilities = np.exp(model.score_samples(values))
    return values[probabilities.argmax()]
def moda(tutted):
    model = KernelDensity(bandwidth=2, kernel='gaussian')
    tutted = tutted.reshape((len(tutted), 1))
    model.fit(tutted)
    values = np.array([value for value in np.linspace(0,0.8)])
    values = values.reshape((len(values), 1))
    probabilities = np.exp(model.score_samples(values))
    return values[probabilities.argmax()]
def find_mode_continuous(values, num_bins = 0):
    if num_bins==0:
        num_bins = max(values.shape)+1
    hist, bin_edges = np.histogram(values, bins=num_bins)
    bin_index = np.argmax(hist)
    mode_start = bin_edges[bin_index]
    mode_end = bin_edges[bin_index + 1]
    mode = (mode_start + mode_end) / 2  
    return mode, values.mean()
def moda2(mat, bins=0):
    tutted = np.unique(mat.round(5))
    tutted = tutted[tutted<0.99]
    return find_mode_continuous(tutted)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dataset", help='Name of the dataset to examine, ex. WebOfScience', type=str,
                        default='WebOfScience', required=True)
    args = parser.parse_args()

    model_name = 'all-mpnet-base-v2'
    DATASETS = {'WebOfScience': WebOfScience, 'DBPedia': DBPedia, 'AmazonHTC': AmazonHTC, 'Books':Books}
    data_test = DATASETS[args.dataset]('test', topn=None)
    zste_model = ZeroShooterZSTC(model_name=model_name)
    scores_zs = PriorScoresZeroShooting(zste_model, data_test.tax_tree, data_test.labels_flat)
    res = scores_zs.compute_prior_scores(data_test.abstracts)
    
    def visit_tree(tree: dict, depth=0):
        if depth == 0:
            indice_primo_livello = [zste_model.label2id[el] for el in tree.keys()]
            dist_media_l1 = moda2(dist_mia(zste_model.labels_embs[indice_primo_livello]))
            print("columns names = ['parent node' ,' depth', 'similarity among children','similarity with children']")
            print("[['fathers' ,", depth, ",", dist_media_l1[1], ", ],")
    
        if isinstance(tree,dict) and not tree:
            return
        
        for key, subtree in tree.items():        
            if isinstance(subtree, dict) and subtree:
                ramo = [zste_model.label2id[key]]+[zste_model.label2id[el2] for el2 in subtree.keys()]
                label = moda2(dist_mia(zste_model.labels_embs[ramo])[1:,0])
                figli = moda2(dist_mia(zste_model.labels_embs[ramo])[1:,1:])
                print("['"+zste_model.id2label[ramo[0]]+"',",depth,",", figli[1],",", label[1], "],")
                
                visit_tree(subtree,depth=depth+1)
    
    visit_tree(data_test.tax_tree)






