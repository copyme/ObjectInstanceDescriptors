import os
import glob
import re
import subprocess
from pathlib import Path
import numpy as np
import random

#####################################################################################################

# Open sampled mesh : 

file = "C:\\Users\\taguilar\\Documents\\Python Scripts\\800x1000mm_800x1000mm_[147635].off"

# New .off file :

file_off = "C:\\Users\\taguilar\\Documents\\Python Scripts\\OUI.off"

#####################################################################################################


def output_file(file):
    lines = [line.rstrip() for line in open(file)]
    lines_0 = lines[0].split('\t')
    lines = lines[1:]
    ALL_ELEMENTS = []
    ALL_ELEMENTS_Float = []
    for i in lines:
        ALL_ELEMENTS.append(i.split(' '))
        
    
    #print(len(ALL_ELEMENTS[130]))
    
    for j in ALL_ELEMENTS:
        if len(j) == 3 and '0' not in j:
            tmp = []
            for k in j:
                tmp.append(float(k))
            ALL_ELEMENTS_Float.append(tmp) 
            
        if len(j) == 4:
            tmp = []
            for k in j:
                tmp.append(int(k))
            ALL_ELEMENTS_Float.append(tmp) 
            
            
    
            
    # for i in range(121):
        # tmp = []
        # for k in ALL_ELEMENTS[i]:
            # tmp.append(float(k))
        # ALL_ELEMENTS_Float.append(tmp) 
    
    # for j in range(121,len(ALL_ELEMENTS),1):
        # tmp = []
        # for k in ALL_ELEMENTS[j]:
            # tmp.append(int(k))
        # ALL_ELEMENTS_Float.append(tmp) 
        
        
    #print(ALL_ELEMENTS[0])
    
    return ALL_ELEMENTS_Float,ALL_ELEMENTS[0]


def add_noise(Liste_points):
    New_Liste = []
    for i in range(120):
        New_Liste.append([Liste_points[i+1][0] + random.uniform(0.1, 0.01) , Liste_points[i+1][1] + random.uniform(0.1, 0.01) , Liste_points[i+1][2] + random.uniform(0.1, 0.01) ])
        
        
    return New_Liste 
        

def Create_off_file(Liste_Old_points, Liste_New_points, output_path,INFO):
    Final = [] 
    for i in range(len(Liste_New_points)):
        Liste_Old_points[i] = Liste_New_points[i]
        
        
    file = open(output_path,"w+")
    file.write('OFF\n')
    
    stringInfo = INFO[0] + ' ' + INFO[1] + ' ' + INFO[2]
    file.write(stringInfo +'\n')   
    
    for k in Liste_Old_points:
        string = ''
        for j in k:
            string += str(j) + ' ' 
        Final.append(string)
  
    
    
    for m in Final:
        file.write(m+'\n')
        
        
        
    
    
#####################################################################################################    
    
if __name__ == "__main__":            
    
        ELEMENTS_1,ELEMENTS_2 = output_file(file)
       
        
        New_liste = add_noise(ELEMENTS_1)
        
        Create_off_file(ELEMENTS_1, New_liste, file_off,ELEMENTS_2)
        