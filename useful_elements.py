import os
import glob
import re
import subprocess
from pathlib import Path
import numpy as np
import json
import csv
from collections import Counter

# Script to list the useful Scannet scenes  for our study, i.e. the scenes that contain the elements that interest us.

###################  Input path train folder and val folder  ##################

# Nef
input_path_train = "/data/shared/taguilar/scannetv2/PointGroup_datatset/train"

#input_path_val = "/home/taguilar/PointGroup/PointGroup/dataset/scannetv2/val"

# Desktop
#input_path_train = "C:\\Users\\taguilar\\Documents\\Project\\Test\\train"

###############################################################################

# Lists of useful elements for our study :

ITEMS = ["wall","floor","door","window","ceiling","radiator","toilet","shower","stair rail","tube","cart","stairs","column","pipe","pillar"]


########################################

# The function to get useful elements:

def read_json_file(path,desired_items):
    useful_files = []
    for (dirpath, dirnames, filenames) in os.walk(path):
        
        for file in filenames:
            if "aggregation" in file:
                cpt = 0 
                element = []
                f = open(os.path.join(dirpath, file))
                data = json.load(f)
                for x in data["segGroups"]:
                    element.append(x["label"])
                for i in element:
                    if i in desired_items:
                        cpt += 1
                if cpt > 0:
                    useful_files.append(os.path.join(dirpath, file))
    print(len(useful_files))
                                  
            
            
################################################
 
tsv_file = "/user/taguilar/home/PointGroup/dataset/scannetv2/scannetv2-labels.combined.tsv"

################################################

def open_tsv_file(file):
    lines = [line.rstrip() for line in open(file)]
    lines_0 = lines[0].split('\t')
    lines = lines[1:]
    ALL_ELEMENTS=[]
    for i in range(len(lines)):
        elements = lines[i].split('\t')
        raw_name = elements[1]
        ALL_ELEMENTS.append(raw_name)
    return ALL_ELEMENTS







################################################      

csv_file = "/user/taguilar/home/PointGroup/dataset/scannetv2/useful_elements_train.csv"
 
################################################          
  
def create_csv_file_train(path , TSV_File, CSV_File):
    for (dirpath, dirnames, filenames) in os.walk(path):
        ALL_List=[]
        All_elements = open_tsv_file(TSV_File)
        for file in filenames:            
            if "aggregation" in file:
                elements = []
                f = open(os.path.join(dirpath, file))
                data = json.load(f)
                for x in data["segGroups"]:
                    elements.append(x["label"])
            
                list_to_csv = []
                for j in All_elements:
                    occurence = elements.count(j)
                    list_to_csv.append(occurence)
                    
                list_to_csv.insert(0,Path(Path(file).stem).stem)
                ALL_List.append(list_to_csv)
    
    
    #print(["Scene"] + All_elements)
    with open(CSV_File, 'w', encoding='UTF8', newline='') as f:
                    writer = csv.writer(f)
                     
                    #write Header
                    All_elements_1 = ["Scene"] + All_elements
                    writer.writerow(All_elements_1)  

                    #write row
                    for k in ALL_List:
                        writer.writerow(k)
                            
                
                                 
#####################################


if __name__ == '__main__':  

    #read_json_file(input_path_train , ITEMS)

    #open_tsv_file(tsv_file)

    create_csv_file_train(input_path_train , tsv_file, csv_file)

