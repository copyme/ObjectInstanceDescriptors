import os
import glob
import re
import subprocess
from pathlib import Path
import numpy as np

################################################   GIN   ################################################                    

# Python script to create symlink between the data repository in my user repository respecting the lists provided on the github
# That's why I use 3 functions, one per list: one for the train set, one for the test set, and the last for the val set
################################################################################################

# Input :

input_path_train = "/data/taguilar/scannetv2/Donnees/scans/"

input_path_test = "/data/taguilar/scannetv2/Donnees/scans_test/"

input_path_val = "/data/taguilar/scannetv2/Donnees/scans_val/"


################################################################################################

# Output :

output_path_train = "/data/taguilar/scannetv2/Donnees/PointGroup_dataset/train/"

output_path_val = "/data/taguilar/scannetv2/Donnees/PointGroup_dataset/val/"

output_path_test = "/data/taguilar/scannetv2/Donnees/PointGroup_dataset/test/"


################################################################################################   

def copy_train_data(input_path,output_path):
    cpt=0
    for (dirpath, dirnames, filenames) in os.walk(input_path):
        
        for file in filenames:
        
            if "vh_clean_2" in file:
                print(os.path.join(dirpath, file))
                os.symlink(os.path.join(dirpath, file),os.path.join(output_path, file))
            if "aggregation" in file and "vh_clean" not in file:
                os.symlink(os.path.join(dirpath, file),os.path.join(output_path, file))
                cpt+=1
                print(os.path.join(dirpath, file))
    print(cpt)
        

def copy_test_data(input_path,output_path):
    cpt=0
    for (dirpath, dirnames, filenames) in os.walk(input_path):
        for file in filenames:
            if "vh_clean_2" in file :
                print(os.path.join(dirpath, file))
                print(dirpath)

                os.symlink(os.path.join(dirpath, file),os.path.join(output_path, file))
                cpt+=1
    print(cpt)
    
    
def copy_val_data(input_path,output_path):
    cpt=0
    for (dirpath, dirnames, filenames) in os.walk(input_path):
        
        for file in filenames:
        
            if "vh_clean_2" in file:
                print(os.path.join(dirpath, file))
                os.symlink(os.path.join(dirpath, file),os.path.join(output_path, file))

            if "aggregation" in file and "vh_clean" not in file:
                cpt+=1
                print(os.path.join(dirpath, file))
                os.symlink(os.path.join(dirpath, file),os.path.join(output_path, file))

    print(cpt)




if __name__ == '__main__':

    ## Create Symlinks
    copy_train_data(input_path_train, output_path_train)
    
    copy_test_data(input_path_test, output_path_test)
    
    copy_val_data(input_path_val, output_path_val)