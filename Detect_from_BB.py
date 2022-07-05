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

Path = "C:\\Users\\taguilar\\Documents\\CaseStudy_files\\Ply_format_CaseStudy_fix\\fbx-ply-export-Case_Study1_all_ply\\"

FILE = "C:\\Users\\taguilar\\Documents\\CaseStudy_files\\Ply_format_CaseStudy_fix\\fbx-ply-export-Case_Study1_all_ply\\0762_x_2032mm_0762_x_2032mm_[147585].ply"

BIG_PC_CASE1 = "C:\\Users\\taguilar\\Documents\\Project\\data\\case_1_subsampled_005.ply"

########################################################################################



def compute_bounding_box(file):
    # PC
    pcd = o3d.io.read_point_cloud(file)
    
    #BB
    axis_aligned_bounding_box = pcd.get_axis_aligned_bounding_box()
    axis_aligned_bounding_box.color = (1, 0, 0)
    
    extent = axis_aligned_bounding_box.get_max_extent()

    #print(pcd)

    Points_List = np.asarray(pcd.points)
    
    # Retourne les PCD, les coordonnées de la Bounding Box, et le nuage de points sous la forme d'array
    return pcd, axis_aligned_bounding_box, Points_List
    
    # print(extent)
    
    
    
    

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


       
    

    
def get_labelled_data(Big_PC, dossier_ply_files, NB_Of_Points):
    DICO = {}
    
    PCD = o3d.io.read_point_cloud(Big_PC)

    Points_List = np.asarray(PCD.points)
    Points_List = Points_List.tolist()
    
    for (dirpath, dirnames, filenames) in os.walk(dossier_ply_files):
        for file in filenames:
            DATA = []
            # Générer les points du nuage : 
            mesh = trimesh.load(dossier_ply_files + file)
           
            points = mesh.sample(NB_Of_Points)
            
            for i in points:
                DATA.append(i)
            # BB
            pcd = o3d.geometry.PointCloud()
            pcd.points = o3d.utility.Vector3dVector(DATA)
            pcd.paint_uniform_color([1, 0, 0])
            axis_aligned_bounding_box = pcd.get_axis_aligned_bounding_box()
            
            # info = axis_aligned_bounding_box.scale(1.01,axis_aligned_bounding_box.get_center())


            # L = In_BB_Or_Not(info, Points_List)
            L = In_BB_Or_Not(axis_aligned_bounding_box, Points_List)
            DICO[file] = L
            
    return DICO


def visualization_PC(dico):
    Result = []
    for i in dico.keys():
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(dico[i])
        pcd.paint_uniform_color([random.random(), random.random(), random.random()])
        Result.append(pcd)
    o3d.visualization.draw(Result)


if __name__ == "__main__":

    
    dico = get_labelled_data(BIG_PC_CASE1, Path, 10000)

    
    
###########################################################################
    
    ## Create fichier txt à partir du DICO : 
    # import json
  
    # compute_bounding_box(FILE)
  
    # with open('convert.txt', 'w') as convert_file:
        # convert_file.write(json.dumps(dico))
        
###########################################################################
    
    visualization_PC(dico)
        