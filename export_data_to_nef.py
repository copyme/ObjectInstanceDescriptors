import os
import glob
import re
import subprocess
from pathlib import Path
import numpy as np

# Python script to export scannetv2 data from deepsat to nef cluster respecting the lists provided on the github
# That's why I use 3 functions, one per list: one for the train set, one for the test set, and the last for the val set
################################################################################################

#input path

#Directory containing the files to link

input_path_train = "/data/shared/taguilar/scannetv2/train/scans/"

input_path_val = "/data/shared/taguilar/scannetv2/val/scans/"

input_path_test = "/data/shared/taguilar/scannetv2/test/scans_test/"

#output path


#Directories on the nef cluster that will contain the exported files
output_path_train = "taguilar@nef-frontal:/home/taguilar/PointGroup/PointGroup/dataset/scannetv2/train/"

output_path_val = "taguilar@nef-frontal:/home/taguilar/PointGroup/PointGroup/dataset/scannetv2/val/"

output_path_test = "taguilar@nef-frontal:/home/taguilar/PointGroup/PointGroup/dataset/scannetv2/test/"

################################################################################################

def copy_train_data(input_path,output_path):
    listOfFiles = list()
    cpt=0
    for (dirpath, dirnames, filenames) in os.walk(input_path):
        for file in filenames:
            args = "rsync " + "-e ssh " + os.path.join(dirpath, file) + " " + output_path 
        
            if "vh_clean_2" in file:
                ##os.symlink(os.path.join(dirpath, file),os.path.join(output_path, file))
                subprocess.call(args, shell=True)
            if "aggregation" in file and "vh_clean" not in file:
                ##os.symlink(os.path.join(dirpath, file),os.path.join(output_path, file))
                subprocess.call(args, shell=True)
                cpt+=1
    print(cpt)
        

def copy_test_data(input_path,output_path):
    listOfFiles = list()
    cpt=0
    for (dirpath, dirnames, filenames) in os.walk(input_path):
        for file in filenames:
            args = "rsync " + "-e ssh " + os.path.join(dirpath, file) + " " + output_path  
            if "vh_clean_2" in file:
                
                ##os.symlink(os.path.join(dirpath, file),os.path.join(output_path, file))
                subprocess.call(args, shell=True)
                cpt+=1
    print(cpt)
    
    
def copy_val_data(input_path,output_path):
    listOfFiles = list()
    cpt=0
    for (dirpath, dirnames, filenames) in os.walk(input_path):
        for file in filenames:
            args = "rsync " + "-e ssh " + os.path.join(dirpath, file) + " " + output_path  
        
            if "vh_clean_2" in file:
                
                ##os.symlink(os.path.join(dirpath, file),os.path.join(output_path, file))
                subprocess.call(args, shell=True)

            if "aggregation" in file and "vh_clean" not in file:
                cpt+=1
                
                ##os.symlink(os.path.join(dirpath, file),os.path.join(output_path, file))
                subprocess.call(args, shell=True)
                

    print(cpt)
                               
 
################################################################################################

 
def main():
    copy_train_data(input_path_train,output_path_train)
    
    copy_val_data(input_path_val,output_path_val)
    
    copy_test_data(input_path_test,output_path_test)
    
    
    

if __name__ == "__main__":
    main()