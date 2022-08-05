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

# Ce code permet d'effectuer une classification en utilisant un random forest(on peut changer) en utilisant les features du fichier IFC créé et les features du LIDAR

# Les fichiers sont les suivants: 
# 1) Le fichier des features du fichier IFC obtenu avec PointGroup après Normalisation
# 2) Le fichier contenant les coordonnées et les labels de chaque points du fichier IFC obtenu en créant un fichier txt lors de la phase de sous échantillonage de chaque classe. Normalement, il y a un code dans le même répertoire pour le créer.
# 3) Le fichier LIDAR sur lequel on veut tester le classifieur (format binaire)
# 4) Les features du fichier LIDAR obtenu également avec PointGroup après normalisation

#######################################################################################
#####################################  Your Files #####################################

Link_Features_normalized_IFC = "C:\\Users\\taguilar\\Documents\\Données_ScanNet\\Test_donnee_CS\\CS1_Merged_Normalized_features_and_Coordinates.txt"

Link_3D_coordinates_IFC = "C:\\Users\\taguilar\\Documents\\Données_ScanNet\\Test_donnee_CS\\INFORMATIONS.txt"

LIDAR_DATA_Binary = "C:\\Users\\taguilar\\Documents\\Project\\data\\case_1_subsampled_005.ply"

LIDAR_DATA_ASCII = "C:\\Users\\taguilar\\Documents\\Données_ScanNet\\Test_donnee_CS_LIDAR\\case_1_subsampled_005_ASCII.ply"

Link_Features_normalized_LIDAR = "C:\\Users\\taguilar\\Documents\\Données_ScanNet\\Test_donnee_CS_LIDAR\\LIDAR_Merged_Normalized_features_and_Coordinates.txt"

#######################################################################################


# Utilisation du classifieur en question :

# features_IFC, label, features_LIDAR, LIDAR_ply_file, Nb_Files_Folder


def perform_classifieur_exemple_with_one_class_features(features_IFC, label, features_LIDAR, LIDAR_ply_file):
    ##########################################
    ## Obtain 3D coordinates LIDAR:
    
    PCD = o3d.io.read_point_cloud(LIDAR_ply_file)

    Points_List = np.asarray(PCD.points)
    Points_List = Points_List.tolist()
    ##########################################
    
    X_train, X_test, y_train, y_test = train_test_split(features_IFC, label, train_size=0.80,stratify = label)  # Permet de mieux mélanger
    
    print('Len X_train: %.3i' % len(X_train))
    print('Len X_test: %.3i' % len(X_test))

    ########################### Choisir son classifieur ###############################
    # model = make_pipeline(StandardScaler(), svm.SVC(C = 0.1, kernel = 'rbf'))
    
    model = RandomForestClassifier(max_depth = 30)
    
    # model = MLPClassifier(random_state=1, max_iter=300)
    #######################################################################
    
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    
    print('Accuracy: %.3f' % accuracy_score(y_test, y_pred))
    
    ## Prediction label using the Features from the LIDAR data:
    PRED = model.predict(features_LIDAR)
    
    DICO = {}
    
    # Binary classification :
    for i in [0, 41]:
        LAB = []
        for j in range(len(PRED)):
            if PRED[j] == i: 
                LAB.append(Points_List[j])
                print(j)
        DICO[i] = LAB

    return DICO
    


def perform_classifieur_exemple_with_one_class_coordinates(coordinates_IFC, LABEL_IFC, LIDAR_ply_file):
    
    ##########################################
    ## Big PC with unlabelled data
    
    PCD = o3d.io.read_point_cloud(LIDAR_ply_file)

    Points_List = np.asarray(PCD.points)
    Points_List = Points_List.tolist()
    
    ##########################################
    
    # On va itérer sur toutes les classes, entraîner et prédire à chaque fois :
    
    X_train, X_test, y_train, y_test = train_test_split(coordinates_IFC, LABEL_IFC, train_size=0.80,stratify = LABEL_IFC)  # Permet de mieux mélanger
    
    print('Len X_train: %.3i' % len(X_train))
    print('Len X_test: %.3i' % len(X_test))
        
    ########################### Choisir son classifieur ###############################
    
    model = RandomForestClassifier()
    
    ###################################################################################
    
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    
    print('Accuracy: %.3f' % accuracy_score(y_test, y_pred))
    
################ Prédiction sur le PC #################
    PRED = model.predict(Points_List)
#######################################################
    DICO = {}
    
    # Binary classification :
    for i in [0, 41]:
        LAB = []
        for j in range(len(PRED)):
            if PRED[j] == i: 
                LAB.append(Points_List[j])
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

    LABEL[LABEL < 41] = 0
    LABEL[LABEL > 41] = 0
    
    Coordinates = Labels_and_3D_Coordinates_IFC[:,0:3]    
    
    
    
    ################# Classifieur using the features with one class:

    DICO = perform_classifieur_exemple_with_one_class_features(Features_normalized_IFC, LABEL, Features_normalized_LIDAR, LIDAR_DATA_Binary)
    
    ################# Classifieur using the 3D coordinates with one class:
    
    # DICO = perform_classifieur_exemple_with_one_class_coordinates(Coordinates, LABEL, LIDAR_DATA_Binary)
    
     
     
    # Visualization :
    Resultat = visualization_PC(DICO)
    o3d.visualization.draw(Resultat) 
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    # PCD = o3d.io.read_point_cloud(LIDAR_DATA_Binary)

    # Points_List = np.asarray(PCD.points)
    # Points_List = Points_List.tolist()
    
    # f = plyfile.PlyData().read(LIDAR_DATA_ASCII)
    # points = np.array([list(x) for x in f.elements[0]])
    
    # print(Points_List[0])
    # print(points[0])
    
    # print(len(Points_List[0]))
    # print(len(points[0]))