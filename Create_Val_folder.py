import os
import glob
import re
import subprocess
from pathlib import Path

#############################################################################

input_path = "/data/taguilar/scannetv2/Donnees/scans/"

output_path = " /data/taguilar/scannetv2/Donnees/scans_val/"

txt_val = "/data/taguilar/scannetv2/Donnees/scannetv2_val.txt"

#############################################################################

def read_val_txt(file):
    f = open(file,"r",newline="\n")
    VAL = []
   
    line = f.read().splitlines()
    #line.replace('\n', '')
    VAL.append(line)

    #close file
    f.close
    return VAL[0]


def copy_files(input_path,output_path,txt_file):
    folder = os.listdir(input_path)
    for i in folder:
        if i in txt_file:
            print(i)
            args = "mv "  + input_path + i + output_path + i  
            subprocess.call(args, shell=True)
        
        
if __name__ == '__main__': 
    
    liste_val = read_val_txt(txt_val)
        
    copy_files(input_path, output_path, liste_val)
    
