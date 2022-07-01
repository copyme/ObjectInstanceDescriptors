############################### Package :
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


######################################################################################################################

# File :

Ply_File = "C:\\Users\\taguilar\\Documents\\Python Scripts\\Boite.ply"


######################################################################################################################

def compute_bounding_box(file):
    # PC
    pcd = o3d.io.read_point_cloud(file)
    
    #BB
    axis_aligned_bounding_box = pcd.get_axis_aligned_bounding_box()
    axis_aligned_bounding_box.color = (1, 0, 0)

    #print(pcd)

    Points_List = np.asarray(pcd.points)
    
    # Retourne les PCD, les coordonnées de la Bounding Box, et le nuage de points sous la forme d'array
    return pcd, axis_aligned_bounding_box, Points_List

    
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
    

######################################################  Pas Moi  ######################################################
import random


def give_sphere(x, y, z, r, num):
    points = []
    for i in range(0, num):
        factor = random.uniform(0, 0.05)        
        ir = r * factor
        itheta = np.arccos(np.random.uniform(-1, 1))
        iphi = np.random.uniform(0,  2 * np.pi)
        ix = x + ir * np.sin(itheta) * np.cos(iphi)
        iy = y + ir * np.sin(itheta) * np.sin(iphi)
        iz = z + ir * np.cos(itheta)
        points.append([ix, iy, iz ])
    return points   
      


def recentrer_boule(array,info_BB):
    for i in array:
        i[0] = i[0] + (min(BB_Points[:,0]) + max(BB_Points[:,0]))/2
        i[1] = i[1] + (min(BB_Points[:,1]) + max(BB_Points[:,1]))/2    
        i[2] = i[2] + (min(BB_Points[:,2]) + max(BB_Points[:,2]))/2

    return array
    
    
######################################################################################################################
######################################################################################################################


 
def perform_SVM(array_boite, array_ball):

    # LABEL :
    label_boite = []    
    label_ball = []
    for i in range(len(Points_List)):
        label_boite.append(1)
    for j in range(len(arr3)):
        label_ball.append(2)
          
    #
    array_boite = array_boite.tolist()
    array_ball = array_ball.tolist()
    
    
    for k in array_ball:
        array_boite.append(k)
    for l in label_ball:
        label_boite.append(l)
    
    X_train, X_test, y_train, y_test = train_test_split(array_boite, label_boite, train_size=0.75,stratify = label_boite)  # Permet de mieux mélanger
    
    print('Len X_train: %.3i' % len(X_train))
    print('Len X_test: %.3i' % len(X_test))
    print('Number of mesh elements in train: %.3i' % y_train.count(1))
    print('Number of noise elements in train: %.3i' % y_train.count(2))
    
    print('Number of mesh elements in test: %.3i' % y_test.count(1))
    print('Number of mesh elements in test: %.3i' % y_test.count(2))
    
    # Feature Scaling
 
    # sc = StandardScaler()
    # sc.fit(X_train)
    # X_train_std = sc.transform(X_train)
    # X_test_std = sc.transform(X_test)
    
    model = make_pipeline(StandardScaler(), svm.SVC(C = 0.1, kernel = 'rbf'))
    
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    
    print('Accuracy: %.3f' % accuracy_score(y_test, y_pred))
    
    
    
    
    
######################################################################################################################
######################################################################################################################    
if __name__ == "__main__":
    
    pcd, axis_aligned_bounding_box, Points_List = compute_bounding_box(Ply_File)
    
    # p1 = [[3,-7,-0.5],[3.01,-6.9,-1],[-400, 1, 1]]
    

    # AX SCATTER : 
    # Données : 
    arr1 = np.array(Points_List)
   
    
    points1 = give_sphere(0, 0, 0, 1, 10000)
    arr2 = np.array(points1)
    BB_Points = np.asarray(axis_aligned_bounding_box.get_box_points())  
    arr3 = recentrer_boule(arr2,BB_Points)
        
    pcd2 = o3d.geometry.PointCloud()
    pcd2.points = o3d.utility.Vector3dVector(arr3)
    
    # Add color :
    pcd2.paint_uniform_color([1, 0, 0])
    pcd.paint_uniform_color([0, 0, 1])
        
    
    perform_SVM(Points_List, arr3)
    
    
    
    

    
   
    
    ### Récuperer les 8 points de la bounding box :
    # BB_Points = np.asarray(axis_aligned_bounding_box.get_box_points())  
    
    
    
    # points = o3d.utility.Vector3dVector(BB_Points)
    # bbox = o3d.geometry.OrientedBoundingBox.create_from_points(points)
    
    
    ### Voir quels sont les points qui appartiennent à une Bounding Box :
    # L = In_BB_Or_Not(axis_aligned_bounding_box, Points_List)
    # print(L)
    
    
    
    ### Visualisation 3D avec open3D :
    # o3d.visualization.draw([pcd, axis_aligned_bounding_box])
    
    
    
    
    # o3d.visualization.draw([pcd, pcd2, axis_aligned_bounding_box])    
    
