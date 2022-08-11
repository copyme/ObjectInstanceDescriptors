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



#######################################################################################
# File

IFC_coordinates_and_label = "D:\\Test_11_08_2022\\Troisieme\\CS2_IFC.txt"

LIDAR_DATA = "D:\\Test_11_08_2022\\Troisieme\\CS2_no_noise.ply" 

#######################################################################################



def perform_classifieur_on_LIDAR(features_IFC, label, features_LIDAR, LIDAR_data, Nb_Files_Folder):

    #######################################################################

    X_train, X_test, y_train, y_test = train_test_split(features_IFC, label, train_size=0.80,stratify = label)  # Permet de mieux mélanger
    
    print('Len X_train: %.3i' % len(X_train))
    print('Len X_test: %.3i' % len(X_test))

    ########################### Choisir son classifieur ###############################
    # model = make_pipeline(StandardScaler(), svm.SVC(C = 0.1, kernel = 'rbf'))
    
    model = RandomForestClassifier()
    
    # model = MLPClassifier(random_state=1, max_iter=300)
    #######################################################################
    
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    
    print('Accuracy: %.3f' % accuracy_score(y_test, y_pred))
    
    ## Features BIG Points Cloud
    PRED = model.predict(features_LIDAR)
    
     
    DICO = {}
    
    for i in range(1, Nb_Files_Folder + 1):
        print(i)
        LAB = []
        for j in range(len(PRED)):
            if PRED[j] == i: 
                LAB.append(LIDAR_data[j])
                # print(j)
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






from sklearn.preprocessing import normalize


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
    Export_IFC = "D:\\Test_11_08_2022\\Troisieme\\Features_IFC.txt"
    Export_LIDAR = "D:\\Test_11_08_2022\\Troisieme\\Features_LIDAR.txt"
    
    np.savetxt(Export_IFC, Features_IFC, delimiter=' ')
    np.savetxt(Export_LIDAR, Features_LIDAR, delimiter=' ')
    
    #import pdb
    #pdb.set_trace()
    
    #######################################################################################
    # Classifieur:
    DICO = perform_classifieur_on_LIDAR(Features_IFC, LABEL, Features_LIDAR, Coordinates_LIDAR, 167)
    #######################################################################################
    # Visualization :
    Resultat = visualization_PC(DICO)
    o3d.visualization.draw(Resultat)