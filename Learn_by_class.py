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
########################################################################################

Path = "C:\\Users\\taguilar\\Documents\\CaseStudy_files\\Ply_format_CaseStudy_fix\\fbx-ply-export-Case_Study6_all\\"

BIG_PC_CASE1 = "C:\\Users\\taguilar\\Documents\\Project\\data\\CaseStudy6_PC _subsampled_01.ply"

########################################################################################


def create_data_to_learn(dossier,NB_Of_Points):
    All_DATA = []
    All_LABEL = []
    DATA = []
    LABEL = []
    DICO = {}
 
    for (dirpath, dirnames, filenames) in os.walk(dossier):
        cpt = 1
        for file in filenames:
            lab = []
            # Génèrer les Points du nuage : 
            mesh = trimesh.load(dossier + file)
           
            Points = mesh.sample(NB_Of_Points)
            
            for i in Points:
                DATA.append(i)
                lab.append(cpt)
                LABEL.append(file)
            
            DICO[cpt] = Points
            cpt +=1

           
            All_DATA.append(Points)
            All_LABEL.append(lab)
    print("c fait 1")
    return DATA, LABEL, DICO, cpt, All_DATA, All_LABEL


def transform_DATA(x):
    NEW_DATA = []
    for i in x:
        NEW_DATA.append(i.tolist())
    print("c fait 2")
    return NEW_DATA
    
    
def transform_ALL_DATA_and_LABEL(x, y, all_lab):
    NEW_ALL_DATA = []

    for i in y:
        NEW_ALL_DATA.append(i.tolist())

    for i in range(len(x)):
        for j in range(len(NEW_ALL_DATA)):
            if x[i] not in NEW_ALL_DATA[j]:
                NEW_ALL_DATA[j].append(x[i])
                all_lab[j].append(0)
        print(i)
    return NEW_ALL_DATA, all_lab
    
    
    
    
    
# Utilisation du classifieur en question :

def perform_classifieur(array_Files, array_Labels, Big_PC, Nb_Files_Folder):
    
    ##########################################
    ## Big PC with unlabelled data
    
    PCD = o3d.io.read_point_cloud(Big_PC)

    Points_List = np.asarray(PCD.points)
    Points_List = Points_List.tolist()
    ##########################################
    
    ##########################################
    # Création du dictionnaire final :
    DICO = {}
    for m in range(1, Nb_Files_Folder + 1):
        DICO[m] = []  
    ##########################################
    
    # On va itérer sur toutes les classes, entraîner et prédire à chaque fois :

    for i in range(len(array_Files)):
        
        print(i)
        X_train, X_test, y_train, y_test = train_test_split(array_Files[i], array_Labels[i], train_size=0.75,stratify = array_Labels[i])  # Permet de mieux mélanger
    
        print('Len X_train: %.3i' % len(X_train))
        print('Len X_test: %.3i' % len(X_test))
        

    ########################### Choisir son classifieur ###############################
    
        model = RandomForestClassifier(max_depth = 10)
    
    ###################################################################################
    
        model.fit(X_train, y_train)
    
        y_pred = model.predict(X_test)
    
        print('Accuracy: %.3f' % accuracy_score(y_test, y_pred))
    
        ################ Prédiction sur le PC #################
        PRED = model.predict(Points_List)
        #######################################################

        for j in range(len(PRED)):
            if PRED[j] != 0:
                DICO[PRED[j]].append(Points_List[j])

    
        
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

    ## Create DATA from sampled mesh :
    
    data, label, DICO_ply, Number_Files, all_data, all_label = create_data_to_learn(Path, 100)

    # Tous les points des classes sous échantillonées sous forme de liste et non de tracked array
    New_data = transform_DATA(data)
    
    
    New_ALL_DATA, NEW_LABEL = transform_ALL_DATA_and_LABEL(New_data, all_data, all_label)

    
    # print(New_ALL_DATA)
    # print(len(New_ALL_DATA))
    # print(len(New_ALL_DATA[1]))
    
    ## Perform Classifieur : 
    DICT = perform_classifieur(New_ALL_DATA, NEW_LABEL, BIG_PC_CASE1, 196)
    
    
    ## Visualization : 
    Resultat = visualization_PC(DICT)
    o3d.visualization.draw(Resultat)    