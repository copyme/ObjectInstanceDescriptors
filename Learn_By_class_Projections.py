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

from sklearn.preprocessing import normalize
#######################################################################################
####################################  Description  ####################################



#######################################################################################
# File

IFC_coordinates_and_label = "D:\\Test_11_08_2022\\Troisieme\\INFORMATIONS.txt"

LIDAR_DATA = "C:\\Users\\taguilar\\Documents\\Project\\data\\case_1_subsampled_005.ply" 

#######################################################################################




    
# Utilisation du classifieur en question :

def perform_classifieur(array_Files, array_Labels, features_Lidar, Lidar_data, Nb_Files_Folder):
    
    
    
    ##########################################
    # Création du dictionnaire final :
    DICO = {}
    for m in range(1, Nb_Files_Folder + 1):
        DICO[m] = []  
    ##########################################
    
    # On va itérer sur toutes les classes, entraîner et prédire à chaque fois :

    for i in range(1, Nb_Files_Folder + 1):
    
        COPY_LAB = np.copy(array_Labels)

        COPY_LAB[COPY_LAB < i] = 0
        COPY_LAB[COPY_LAB > i] = 0
        
        # import pdb
        # pdb.set_trace()
        
        print(i)
        X_train, X_test, y_train, y_test = train_test_split(array_Files, COPY_LAB, train_size = 0.75,stratify = COPY_LAB)  # Permet de mieux mélanger
    
        print('Len X_train: %.3i' % len(X_train))
        print('Len X_test: %.3i' % len(X_test))
        

    ########################### Choisir Son Classifieur ###############################
    
        model = RandomForestClassifier(max_depth = 16)
    
    ###################################################################################
    
        model.fit(X_train, y_train)
    
        y_pred = model.predict(X_test)
    
        print('Accuracy: %.3f' % accuracy_score(y_test, y_pred))
    
        ################ Prédiction sur le PC #################
        PRED = model.predict(features_Lidar)
        #######################################################
        
        LAB = []
        for j in range(len(PRED)):
            
            if PRED[j] != 0:
                LAB.append(Lidar_data[j])
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
    #######################################################################################
    
    # LIDAR:
    f = plyfile.PlyData().read(LIDAR_DATA)
    
    INFO_LIDAR = np.array([list(x) for x in f.elements[0]])
    
    Coordinates_LIDAR = INFO_LIDAR[:,0:3]
    #######################################################################################
    
    # IFC: 
    Read_IFC = np.loadtxt(IFC_coordinates_and_label, delimiter = ' ')
    
    LABEL = Read_IFC[:,3]
    
    Coordinates = Read_IFC[:,0:3]
    #######################################################################################
    
    # Multiply:
    m2cm = 100
    Coordinates = Coordinates * m2cm
    Coordinates_LIDAR = Coordinates_LIDAR * m2cm
    
    hx = 1./30.
    hy = 1./30.
    hz = 1./30.
    
    Coordinates[:,0] = Coordinates[:,0] * hx
    Coordinates_LIDAR[:,0] = Coordinates_LIDAR[:,0] * hx
    Coordinates[:,1] = Coordinates[:,1] * hy
    Coordinates_LIDAR[:,1] = Coordinates_LIDAR[:,1] * hy
    Coordinates[:,2] = Coordinates[:,2] * hz
    Coordinates_LIDAR[:,2] = Coordinates_LIDAR[:,2] * hz
   
    #######################################################################################
    # Features:
    Features_IFC = np.round_(Coordinates)
    
    Features_LIDAR = np.round_(Coordinates_LIDAR)
    
    # Export
    Export_IFC = "D:\\Test_11_08_2022\\Troisieme\\Features_IFC_CS1.txt"
    Export_LIDAR = "D:\\Test_11_08_2022\\Troisieme\\Features_LIDAR_CS1.txt"
    
    np.savetxt(Export_IFC, Features_IFC, delimiter=' ')
    np.savetxt(Export_LIDAR, Features_LIDAR, delimiter=' ')
    
    # import pdb
    # pdb.set_trace()
    
    #######################################################################################
    
    # Classifieur:
    DICO = perform_classifieur(Features_IFC, LABEL, Features_LIDAR, Coordinates_LIDAR, 69)
    
    #######################################################################################
    
    import pdb
    pdb.set_trace()
    #######################################################################################
    # Export Point Cloud :
    
    Export_PREDICT = "D:\\Test_11_08_2022\\Troisieme\\PREDICTION_CS1.txt"
    
    # file = open("dictfile.txt","w") 
 
    # for key in dict_students.keys(): 
 
        # file.write(str(key)+"  "+str(dict_students[key])) 
        # file.write("\n") 
 
    # file.close()
    
    # np.savetxt(Features_from_ply_normalized, A_norm, delimiter=' ')
    
    #######################################################################################
    
    # Visualization :
    Resultat = visualization_PC(DICO)
    o3d.visualization.draw(Resultat)