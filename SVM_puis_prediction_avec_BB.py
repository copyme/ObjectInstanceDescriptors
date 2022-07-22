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

Path = "C:\\Users\\taguilar\\Documents\\CaseStudy_files\\Ply_format_CaseStudy_fix\\fbx-ply-export-Case_Study1_all_ply\\"

BIG_PC_CASE1 = "C:\\Users\\taguilar\\Documents\\Project\\data\\case_1_subsampled_005.ply"


########################################################################################

# Fonction pour sous-echantillonées toutes les classes de notre fichier IFC avec un nombre de points définit :

def create_data_to_learn(dossier,NB_Of_Points):
    DATA = []
    LABEL = []
    DICO = {}
    List_of_BB = []
    for (dirpath, dirnames, filenames) in os.walk(dossier):
        cpt = 1
        for file in filenames:
            cpt +=1
            # Générer les points du nuage : 
            mesh = trimesh.load(dossier + file)
           
            points = mesh.sample(NB_Of_Points)
            
            for i in points:
                DATA.append(i)
                ## Si je veux utiliser un bruit pour l'entrainement :
                # DATA.append([i[0] + random.uniform(-0.02, 0.02), i[1] + random.uniform(-0.02, 0.02), i[2] + random.uniform(-0.02, 0.02)])
                LABEL.append(file)
            
            DICO[cpt] = points
            cpt +=1
            
            pcd = o3d.geometry.PointCloud()
            pcd.points = o3d.utility.Vector3dVector(DATA)
            pcd.paint_uniform_color([1, 0, 0])
            axis_aligned_bounding_box = pcd.get_axis_aligned_bounding_box()
            
            info = axis_aligned_bounding_box.scale(1.01,axis_aligned_bounding_box.get_center())
            
            List_of_BB.append(info)
            
    return DATA, LABEL, DICO, cpt, List_of_BB      
           
########################################################################################
           
# Deux fonctions pour créer le dictionnaire associé à nos données sous-échantillonées : 
         
def create_dictionnary(dossier):
    DICO = {}
    cpt = 1
    for (dirpath, dirnames, filenames) in os.walk(dossier):
        for file in filenames:
            DICO[file] = cpt
            cpt +=1
    return DICO
            

def MAJ_label(mon_dico, mes_labels):
    for j in range(len(mes_labels)):
        mes_labels[j] = mon_dico[mes_labels[j]]
            
    return mes_labels
    
########################################################################################


# Savoir si des points appartiennent à une Bounding Box :

def In_BB_Or_Not(Coordo_BB, Points):

    # Transforme les coordonnées de la Bounding Box en array pour pouvoir les utiliser : 
    BB_Points = np.asarray(Coordo_BB.get_box_points())
    
    # Récuperer les valeurs max et min pour la Bounding Box :
    X_BB = []
    Y_BB = []
    Z_BB = []
    for j in BB_Points:
        X_BB.append(j[0])
        Y_BB.append(j[1])
        Z_BB.append(j[2])
    
    # Récupérer les points qui appartiennent à la Bounding Box :  
    Liste = []
    if len(Points) == 1:
        if (Points[0][0] <= max(X_BB) and Points[0][0] >= min(X_BB)) and (Points[0][1] <= max(Y_BB) and Points[0][1] >= min(Y_BB)) and (Points[0][2] <= max(Z_BB) and Points[0][2] >= min(Z_BB)):
            Liste.append(Points)
    else:
        for i in Points:
            if (i[0] <= max(X_BB) and i[0] >= min(X_BB)) and (i[1] <= max(Y_BB) and i[1] >= min(Y_BB)) and (i[2] <= max(Z_BB) and i[2] >= min(Z_BB)):
                Liste.append(i)
                
    return Liste


########################################################################################


# Utilisation du classifieur en question :

def perform_classifieur(array_Files, array_Labels, Big_PC, Nb_Files_Folder, list_of_BB):
    
    X_train, X_test, y_train, y_test = train_test_split(array_Files, array_Labels, train_size=0.75,stratify = array_Labels)  # Permet de mieux mélanger
    
    print('Len X_train: %.3i' % len(X_train))
    print('Len X_test: %.3i' % len(X_test))

    ########################### Choisir son classifieur ###############################
    # model = make_pipeline(StandardScaler(), svm.SVC(C = 0.1, kernel = 'rbf'))
    
    model = RandomForestClassifier(max_depth=2)
    
    # model = MLPClassifier(random_state=1, max_iter=300)
    #######################################################################
    
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    
    print('Accuracy: %.3f' % accuracy_score(y_test, y_pred))
    
    
    ## Big PC with unlabelled data
    PCD = o3d.io.read_point_cloud(Big_PC)

    Points_List = np.asarray(PCD.points)
    Points_List = Points_List.tolist()
    
    Resultat = []  
    
    DICO = {}
    for m in list(range(Nb_Files_Folder + 1)):
        DICO[m] = []
     
    for i in list_of_BB:
        L = In_BB_Or_Not(i, Points_List)  # Les points
        print(i)
        PRED = model.predict(L)           # Les labels prédits
        
        for j in range(len(L)):
            DICO[PRED[j]].append(L[j])
            print(j)
        
    return Points_List, PRED, DICO

        
        
        
            
    
    
def visualization_PC(dico):
    Result = []
    for i in dico.keys():
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(dico[i])
        pcd.paint_uniform_color([random.random(), random.random(), random.random()])
        Result.append(pcd)
    return Result
    

    
########################################################################################

           
if __name__ == "__main__":

    ## Create DATA from sampled mesh :
    
    data, label, DICO_ply, Number_Files, BB_liste = create_data_to_learn(Path, 10)
    
    print('Nombre de points: %.3i' % len(data))
    print('Nombre de labels: %.3i' % len(label))
    # print(data)
    
    
    ## Create Dictionnary for label :
    dico = create_dictionnary(Path)
    
    ## Update Label :
    upd_label = MAJ_label(dico, label)
    
    print('Nombre de labels MAJ: %.3i' % len(upd_label))
    # print(upd_label)
    
    
    ## Perform Classifieur : 
    BIG_PC, PREDICTION, DICT = perform_classifieur(data, upd_label, BIG_PC_CASE1, 69, BB_liste)
    
    
    ## Visualization : 
    Resultat = visualization_PC(DICT)
    o3d.visualization.draw(Resultat)
    
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
               
# def data(dossier, file1, file2):
    # pcd = o3d.io.read_point_cloud(dossier + file1)
    # Points_List = np.asarray(pcd.points)

    # print(len(Points_List))
    # pcd2 = pcd.sample_points_uniformly(number_of_points = 10000)
    # o3d.visualization.draw([pcd])
    # mesh = trimesh.load(dossier + file1)
    # mesh1 = trimesh.load(dossier + file2)
    # mesh.show()
    # points1 = mesh.sample(10000)
    # points2 = mesh1.sample(10000)
    
    # print(points1[0])
    
    
    
    # pcd2 = o3d.geometry.PointCloud()
    # pcd2.points = o3d.utility.Vector3dVector(points)
    # o3d.visualization.draw([pcd2])
