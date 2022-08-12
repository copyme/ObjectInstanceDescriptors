import os
import sys
import argparse
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import pandas as pd
import open3d as o3d
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
import numpy as np
import math as m



#######################################################################################
####################################  Description  ####################################

# Ce fichier va créer deux fichier pour le LIDAR:
# 1) l'un sera composé des points qui appartiennent aux BB du fichier IFC
# 2) l'autre contiendra les points détectés comme étant du bruit

#######################################################################################
# Fichiers : 
Path = "C:\\Users\\taguilar\\Documents\\CaseStudy_files\\Ply_format_CaseStudy_fix\\fbx-ply-export-Case_Study6_all\\"

LIDAR_DATA = "C:\\Users\\taguilar\\Documents\\Project\\data\\CaseStudy6_PC _subsampled_01.ply" 
#######################################################################################

def Increase_BB(coordinates_BB, ratio):
    output = np.zeros((8, 3))


    # MAX_value :
    MAX_X = np.max(coordinates_BB[:,0])
    MAX_Y = np.max(coordinates_BB[:,1])
    MAX_Z = np.max(coordinates_BB[:,2])
    
    # MIN_value :
    MIN_X = np.min(coordinates_BB[:,0])
    MIN_Y = np.min(coordinates_BB[:,1])
    MIN_Z = np.min(coordinates_BB[:,2])
    MIN_value = [MIN_X, MIN_Y, MIN_Z]
    
    output[0,:] = [MIN_X - ratio, MIN_Y - ratio, MIN_Z - ratio]
    output[1,:] = [MAX_X + ratio, MIN_Y - ratio, MIN_Z - ratio]
    output[2,:] = [MAX_X + ratio, MIN_Y - ratio, MAX_Z + ratio]
    output[3,:] = [MIN_X - ratio, MIN_Y - ratio, MAX_Z + ratio]
    
    output[4,:] = [MIN_X - ratio, MAX_Y + ratio, MIN_Z - ratio]
    output[5,:] = [MAX_X + ratio, MAX_Y + ratio, MIN_Z - ratio]
    output[6,:] = [MAX_X + ratio, MAX_Y + ratio, MAX_Z + ratio]
    output[7,:] = [MIN_X - ratio, MAX_Y + ratio, MAX_Z + ratio]
        
    return output





def In_BB_Or_Not(Coordo_BB, Points):



    # Transforme les coordonnées de la Bounding Box en array pour pouvoir les utiliser : 
    # BB_Points = np.asarray(Coordo_BB.get_box_points())
    
    # Récuperer les valeurs max et min pour la Bounding Box :
    X_BB = []
    Y_BB = []
    Z_BB = []
    for j in Coordo_BB:
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





def create_data_to_learn(dossier, NB_Of_Points, LIDAR_ply_file):
    DATA = []
    Noise = []
    
    ## Big PC with unlabelled data
    PCD = o3d.io.read_point_cloud(LIDAR_ply_file)

    Points_List = np.asarray(PCD.points)
    Points_List = Points_List.tolist()
    for (dirpath, dirnames, filenames) in os.walk(dossier):
        cpt = 0
        for file in filenames:
            cpt +=1
            print(cpt)
            
            # Générer les Points du nuage : 
            mesh = trimesh.load(dossier + file)
           
            Points = mesh.sample(NB_Of_Points)


            # Generate Bounding Box :
            pcd = o3d.geometry.PointCloud()
            pcd.points = o3d.utility.Vector3dVector(Points)
            axis_aligned_bounding_box = pcd.get_axis_aligned_bounding_box()
            
            
            BB_Points = np.asarray(axis_aligned_bounding_box.get_box_points())  
            
            # Increase_BB
            bboxpoints = Increase_BB(BB_Points, 0.1)
            
            
            
            # Detect DATA and Noise:
            L = In_BB_Or_Not(bboxpoints, Points_List)
            DATA += L
            
            # for i in L:
                # Points_List.remove(i)
            
    
            
    return DATA


    
if __name__ == "__main__":
        DaTa = create_data_to_learn(Path, 10000, LIDAR_DATA)
        
        Output = "D:\\Test_11_08_2022\\Troisieme\\Data_No_Noise\\CS6_No_Noise.txt"
        import pdb
        pdb.set_trace()
        DaTa = np.asarray(DaTa)
        np.savetxt(Output, DaTa, delimiter=' ')