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
from sklearn.decomposition import PCA
from sklearn.neural_network import MLPClassifier
#######################################################################################
####################################  Description  ####################################

# Ce code permet d'effectuer une classification en utilisant un random forest(on peut changer) en utilisant les features du fichier IFC créé et les features du LIDAR

# Les fichiers sont les suivants: 
# 1) Le fichier des features du fichier IFC obtenu avec PointGroup après Normalisation
# 2) Le fichier contenant les coordonnées et les labels de chaque points du fichier IFC obtenu en créant un fichier txt lors de la phase de sous échantillonage de chaque classe. Normalement, il y a un code dans le même répertoire pour le créer.
# 3) Le fichier LIDAR sur lequel on veut tester le classifieur
# 4) Les features du fichier LIDAR obtenu également avec PointGroup après normalisation

#######################################################################################
#####################################  Your Files #####################################

Link_Features_normalized_IFC = "C:\\Users\\taguilar\\Documents\\Données_ScanNet\\Test_donnee_CS\\CS1_color_original_model_20_classes_normalized.txt"

Link_3D_coordinates_IFC = "C:\\Users\\taguilar\\Documents\\Données_ScanNet\\Test_donnee_CS\\INFORMATIONS.txt"

LIDAR_DATA = "C:\\Users\\taguilar\\Documents\\Project\\data\\case_1_subsampled_005.ply"

Link_Features_normalized_LIDAR = "C:\\Users\\taguilar\\Documents\\Données_ScanNet\\Test_donnee_CS_LIDAR\\LIDAR_CS1_color_original_model_20_classes_normalized.txt"

#######################################################################################


def perform_classifieur_on_LIDAR(features_IFC, label, features_LIDAR, LIDAR_ply_file, Nb_Files_Folder):


    X_train, X_test, y_train, y_test = train_test_split(features_IFC, label, train_size=0.80,stratify = label)  # Permet de mieux mélanger
    
    print('Len X_train: %.3i' % len(X_train))
    print('Len X_test: %.3i' % len(X_test))

    ########################### Choisir son classifieur ###############################
    # model = make_pipeline(StandardScaler(), svm.SVC(C = 0.1, kernel = 'rbf'))
    
    model = RandomForestClassifier(max_depth = 16)
    
    # model = MLPClassifier(random_state=1, max_iter=300)
    #######################################################################
    
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    
    print('Accuracy: %.3f' % accuracy_score(y_test, y_pred))
    
    ## Features BIG Points Cloud
    PRED = model.predict(features_LIDAR)
    
    
    
    # Read Big Points Cloud to get the 3D coordinates:
    PCD = o3d.io.read_point_cloud(LIDAR_ply_file)

    Points_List = np.asarray(PCD.points)
    Points_List = Points_List.tolist()
    
    
    
    DICO = {}
    
    for i in range(1, Nb_Files_Folder + 1):
        LAB = []
        for j in range(len(PRED)):
            if PRED[j] == i: 
                LAB.append(Points_List[j])
                print(j)
        DICO[i] = LAB

    return DICO
    




def perform_classifieur_on_IFC(features_IFC, label, Nb_Files_Folder, coordinates_IFC):


    X_train, X_test, y_train, y_test = train_test_split(features_IFC, label, train_size=0.80,stratify = label)  # Permet de mieux mélanger
    
    print('Len X_train: %.3i' % len(X_train))
    print('Len X_test: %.3i' % len(X_test))

    ########################### Choisir son classifieur ###############################
    # model = make_pipeline(StandardScaler(), svm.SVC(C = 0.1, kernel = 'rbf'))
    
    model = RandomForestClassifier(max_depth = 12)
    
    # model = MLPClassifier(random_state=1, max_iter=300)
    #######################################################################
    
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    
    print('Accuracy: %.3f' % accuracy_score(y_test, y_pred))  
    
    PRED = model.predict(features_IFC)
    
    DICO = {}
    
    for i in range(1, Nb_Files_Folder + 1):
        LAB = []
        for j in range(len(PRED)):
            if PRED[j] == i: 
                LAB.append(coordinates_IFC[j])
                print(j)
        DICO[i] = LAB

    return DICO





def visualization_PC(dico):
    Result = []
    for i in dico.keys():
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(dico[i])
        pcd.paint_uniform_color([random.random(), random.random(), random.random()])
        Result.append(pcd)
    return Result



if __name__ == "__main__":

    Features_normalized_IFC = np.loadtxt(Link_Features_normalized_IFC, delimiter = ' ')
    
    Features_normalized_LIDAR = np.loadtxt(Link_Features_normalized_LIDAR, delimiter = ' ')
    
    Labels_and_3D_Coordinates_IFC = np.loadtxt(Link_3D_coordinates_IFC, delimiter = ' ')
    
    LABEL = Labels_and_3D_Coordinates_IFC[:,3]
    
    Coordinates = Labels_and_3D_Coordinates_IFC[:,0:3]
    
    # import pdb
    # pdb.set_trace()
    
    # On LIDAR: 
    # DICO_1 = perform_classifieur_on_LIDAR(Features_normalized_IFC, LABEL, Features_normalized_LIDAR, LIDAR_DATA, len(np.unique(LABEL)))
    
    # On IFC:
    DICO_2 = perform_classifieur_on_IFC(Features_normalized_IFC, LABEL, len(np.unique(LABEL)), Coordinates)
    
    # Visualization :
    Resultat = visualization_PC(DICO_2)
    o3d.visualization.draw(Resultat)