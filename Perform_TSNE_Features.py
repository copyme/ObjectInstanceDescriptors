####################################### Packages #######################################
import os
import glob
import re
import subprocess
from pathlib import Path
import numpy as np
import random
import open3d as o3d
import numpy as np
import matplotlib.pyplot as plt
import copy
import os
import sys
import argparse
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import pandas as pd
    
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn import svm

from sklearn.metrics import accuracy_score
import trimesh
from sklearn.ensemble import RandomForestClassifier
from sklearn.manifold import TSNE
import pandas as pd 
import seaborn as sns 
import plyfile

#######################################################################################
####################################  Description  ####################################


# Ce code permet d'effectuer une TSNE sur les features d'un fichier choisit, cela peut être sur le features du LIDAR ou de l'IFC.
# Il faut juste fournir les bons documents :) qui sont:
# 1) Le fichier Ply au format Ascii du fichier (LIDAR ou IFC)
# 2) Le fichier contenant les coordonnées et les labels de chaque point du fichier (pas de label pour le LIDAR)
# 3) Le fichier des features du fuchier Ply obtenu avec PointGroup et après normalisation


#######################################################################################
#####################################  Your Files #####################################

Ply_file_Ascii = "C:\\Users\\taguilar\\Documents\\Données_ScanNet\\Test_donnee_CS\\ALL_classes_sampled_ascii.ply"

Coordinates_and_label_Ply_file = "C:\\Users\\taguilar\\Documents\\Données_ScanNet\\Test_donnee_CS\\INFORMATIONS.txt"

Features_normalized_Ply_file = "C:\\Users\\taguilar\\Documents\\Données_ScanNet\\Test_donnee_CS\\CS1_color_original_model_20_classes_normalized.txt"

#######################################################################################


if __name__ == "__main__":
    
    Features_normalized_PLY_File = np.loadtxt(Features_normalized_Ply_file, delimiter = ' ')
    
    Labels_and_3D_Coordinates_IFC = np.loadtxt(Coordinates_and_label_Ply_file, delimiter = ' ')
    
    LABEL = Labels_and_3D_Coordinates_IFC[:,3]
    
    ### We take only a few number of features :
    
    number_of_elements = 10000
    
    idx = np.arange(1, len(Labels_and_3D_Coordinates_IFC), 1, dtype=int)
    
    from sklearn import utils
    
    new_idx = utils.shuffle(idx)[0:number_of_elements]
    
###################################################################
#####################       Appply TSNE       #####################

    tsne = TSNE(n_components=2, verbose=1, random_state=123)
    z = tsne.fit_transform(IFC_feats[new_idx,:])
    df = pd.DataFrame()
    df["y"] = np.array(y_train)[new_idx]
    df["comp-1"] = z[:,0]
    df["comp-2"] = z[:,1]

    
    numcolor = np.unique(y_train[new_idx]).shape[0]
    
    # import pdb
    # pdb.set_trace()
    
    sns.scatterplot(x="comp-1", y="comp-2", hue=df.y.tolist(),
                palette=sns.color_palette("hls", numcolor),
                data=df).set(title="Ply File T-SNE projection")




    plt.show()
