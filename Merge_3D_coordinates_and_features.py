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
import plyfile
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn import svm

from sklearn.metrics import accuracy_score
import trimesh
from sklearn.ensemble import RandomForestClassifier
from sklearn.decomposition import PCA
from sklearn.neural_network import MLPClassifier
#######################################################################################
####################################  Description  ####################################

# Ce code permet de fusionner les coordonnées XYZ d'un fichier txt avec les features obtenues avec PointGroup pour créer un nouveau fichier txt:

#######################################################################################
#####################################  Your Files #####################################

Features = "C:\\Users\\taguilar\\Documents\\Données_ScanNet\\Test_donnee_CS_LIDAR\\LIDAR_CS1_color_original_model_20_classes.txt"

Coordinates_and_Label = "C:\\Users\\taguilar\\Documents\\Données_ScanNet\\Test_donnee_CS\\INFORMATIONS.txt"

Merged_features_and_Coordinates = "C:\\Users\\taguilar\\Documents\\Données_ScanNet\\Test_donnee_CS_LIDAR\\LIDAR_Merged_features_and_Coordinates.txt"

#######################################################################################
#######################################################################################

###################### FOR the IFC  ######################
# Features :
# features = np.loadtxt(Features, delimiter = ' ')

# Coordinates and LABEL :
# Labels_and_3D_Coordinates = np.loadtxt(Coordinates_and_Label, delimiter = ' ')
 
# LABEL = Labels_and_3D_Coordinates[:,3]
    
# Coordinates = Labels_and_3D_Coordinates[:,0:3]

# MERGED = np.append(features, Coordinates, axis = 1)
    
# np.savetxt(Merged_features_and_Coordinates, MERGED, delimiter=' ')





###################### FOR the LIDAR  ######################
# Features :
features = np.loadtxt(Features, delimiter = ' ')

# Coordinates reading directly the ply in ASCII:
fn = "C:\\Users\\taguilar\\Documents\\Données_ScanNet\\Test_donnee_CS_LIDAR\\case_1_subsampled_005_ASCII.ply"

f = plyfile.PlyData().read(fn)
Coordinates = np.array([list(x) for x in f.elements[0]])


MERGED = np.append(features, Coordinates, axis = 1)
    

np.savetxt(Merged_features_and_Coordinates, MERGED, delimiter=' ')