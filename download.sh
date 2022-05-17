#!/bin/bash

#This code allows us to download the data necessary to use the PointGroup code by following the different sets: Train, Val and Test. 
#This code is launched on screen to perform the downloads backwards
#The txt files have been created to contain the names of the files needed for each set


#Txt files containing the names of each documents we need to download
DATA_VAL=scannetv2_val.txt
DATA_TRAIN=scannetv2_train.txt
DATA_TEST=scannetv2_test.txt

DOWNLOADER=download-scannet.py #code python to use

#Output
OUTPUT_VAL="/data/shared/taguilar/scannetv2/val"
OUTPUT_TRAIN="/data/shared/taguilar/scannetv2/train"
OUTPUT_TEST="/data/shared/taguilar/scannetv2/test"


#Loop on the txt files: -o for the output
#						--id to download a specific scan 
while read i; do
  python2.7 $DOWNLOADER -o $OUTPUT_TRAIN --id ${i}
done <${DATA_TRAIN}

while read i; do
  python2.7 $DOWNLOADER -o $OUTPUT_VAL --id ${i}
done <${DATA_VAL}

while read i; do
  python2.7 $DOWNLOADER -o $OUTPUT_TEST --id ${i}
done <${DATA_TEST}

