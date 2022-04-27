
# Code to sample ply files with the sample code from Pierre. We are using sample.exe to run this code.

#Import some libraries

import os
import glob
import re
import subprocess
from pathlib import Path


#Path for the input files
input_path = 'C:\\Users\\taguilar\\Documents\\CaseStudy_files\\Ply_format_CaseStudy_fix\\fbx-ply-export-Case_Study1_all\\' 

#Path for the output files (converted files)
output_path= 'C:\\Users\\taguilar\\Documents\\Project\\code_from_Pierre\\app\\sample\\build\\Release\\Output\\Output_case_study1\\'


##########################################################################################################################

# We need a code that take all the files names from a folder : you can use two methods

# First, if you want to take into account only one type of file format (ply in our case), use code 1 :

    
def file_name1(link):
    file_path = glob.glob(link + '*ply' )                  # link is the path 
    file_list = [i.split('\\')[-1] for i in file_path]
    return file_list                                       
 
    
##########################################################################################################################

# Second, if your folder contains only the files you need, use code 2
 

def file_name2(link):
    
    files = os.listdir(link)

    All_names=[]                            # Creation of a list containing the names of all the files in the directory

    for name in files:
        All_names.append(name)
    
    #print(All_names)                       
    return All_names


###########################################################################################################################

# Now, we want a function to execute our sample.exe file with some parameters :
# First: exe file name, 
# Second: path + input file name  
# Third: A parameter
# Fourth: path + the output file name

def execute(exe_file,input_file,parameter,output_file):
    
    args = exe_file  + " -i " + input_file + " -d " + parameter + " -o " + output_file 
    print(args)
    
    subprocess.call(args, shell=True)

# Exemple:    
# execute("sample.exe",input_path+"0762_x_2032mm_0762_x_2032mm_[147585].ply","10000",output_path+"new2.ply")


###########################################################################################################################

# Main function : Find the names of all the files in a directory, then execute our desired command line to create our new file (a point cloud)
    
def main(in_put_path, out_put_path, parametre, exe_name):
    names_list=file_name2(in_put_path)
    for i in names_list:
        file_name = Path(i).stem
        new_name= file_name+"_Point_cloud.ply"                                   # Name of the output file

        execute(exe_name, in_put_path + i, parametre, out_put_path + new_name)
    
    
    

if __name__ == "__main__":
    main(input_path, output_path, "10000","C:\\Users\\taguilar\\Documents\\Project\\code_from_Pierre\\app\\sample\\build\\Release\\sample.exe")
   
   


    