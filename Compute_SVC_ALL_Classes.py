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


########################################################################################

Path = "C:\\Users\\taguilar\\Documents\\CaseStudy_files\\Ply_format_CaseStudy_fix\\fbx-ply-export-Case_Study2_all\\"

########################################################################################

def create_data_to_learn(dossier,NB_Of_Points):
    DATA = []
    LABEL = []
    for (dirpath, dirnames, filenames) in os.walk(dossier):
        for file in filenames:
           
            # Générer les points du nuage : 
            mesh = trimesh.load(dossier + file)
           
            points = mesh.sample(NB_Of_Points)
           
            for i in points:
                DATA.append(i)
                LABEL.append(file)
           
           
    return DATA, LABEL       
           
           
           
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
    

def perform_SVM(array_Files, array_Labels):
    
    X_train, X_test, y_train, y_test = train_test_split(array_Files, array_Labels, train_size=0.75,stratify = array_Labels)  # Permet de mieux mélanger
    
    print('Len X_train: %.3i' % len(X_train))
    print('Len X_test: %.3i' % len(X_test))

    model = make_pipeline(StandardScaler(), svm.SVC(C = 0.1, kernel = 'rbf'))
    
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    
    print('Accuracy: %.3f' % accuracy_score(y_test, y_pred))
########################################################################################

           
if __name__ == "__main__":

    ## Create DATA from sampled mesh :
    
    data, label = create_data_to_learn(Path, 10000)
    
    print('Nombre de points: %.3i' % len(data))
    print('Nombre de labels: %.3i' % len(label))
    
    ## Create Dictionnary for label :
    dico = create_dictionnary(Path)
    
    ## Update Label :
    upd_label = MAJ_label(dico, label)
    
    print('Nombre de labels MAJ: %.3i' % len(upd_label))
    
    
    ## Perform SVM : 
    perform_SVM(data, upd_label)
    
    
    ## Others (tests, Visualization ....) :
    # mesh = trimesh.load("C:\\Users\\taguilar\\Documents\\CaseStudy_files\\Ply_format_CaseStudy_fix\\fbx-ply-export-Case_Study2_all\\0762_x_2032mm_2_0762_x_2032mm_2_[151902].ply")
    # points1 = mesh.sample(10000)
    # pcd2 = o3d.geometry.PointCloud()
    # pcd2.points = o3d.utility.Vector3dVector(points1)
    # o3d.visualization.draw([pcd2])
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
               
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
