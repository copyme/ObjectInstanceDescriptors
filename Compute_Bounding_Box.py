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
###############################

# File :

Ply_File = "C:\\Users\\taguilar\\Documents\\Python Scripts\\Mesh.ply"


###############################

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
        
    
    

if __name__ == "__main__":
    
    pcd, axis_aligned_bounding_box, mes_points = compute_bounding_box(Ply_File)
    
    p1 = [[3,-7,-0.5],[3.01,-6.9,-1],[-400, 1, 1]]
    
    
    # Récuperer les 8 points de la bounding box :
    BB_Points = np.asarray(axis_aligned_bounding_box.get_box_points())  
    
    
    # points = o3d.utility.Vector3dVector(BB_Points)
    # bbox = o3d.geometry.OrientedBoundingBox.create_from_points(points)
    
        
    L = In_BB_Or_Not(axis_aligned_bounding_box, mes_points)
    print(L)
    
    # Visualisation 3D avec open3D :
    # o3d.visualization.draw([pcd, axis_aligned_bounding_box])  
