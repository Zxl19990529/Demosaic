import yaml 
import numpy as np 
import os 
import random
import re
def get_config(config):
    with open(config,'r') as stream:
        return yaml.load(stream) 

def get_center_area(width,height,mosaic_area):
        width_left = int(width/2-mosaic_area)
        width_right = width_left+mosaic_area*2
        height_up = int(height/2-mosaic_area)
        height_down = height_up+mosaic_area*2 
        area = {'width_left':width_left,'width_right':width_right,'height_up':height_up,'height_down':height_down}
        return area
def get_random_filename_area(line):
        spt = str(line)
        spt = re.split(' ',spt)
        mosaic_area = int(spt[6])
        width_left = int(spt[2])
        width_right = width_left + mosaic_area
        height_up = int(spt[4])
        height_down = height_up + mosaic_area
        area = {'width_left':width_left,'width_right':width_right,'height_up':height_up,'height_down':height_down}
        filename = spt[0]
        processed_image = re.split('/',filename)[2]
        original_image = processed_image[9:]# 把mosaiced_ 这段字符串去掉
        return original_image,processed_image, area

def PSNR(original_image,processed_image):
        width,height=original_image.shape[1],original_image.shape[0]
        diff = original_image-processed_image
        MSE = (np.sum(diff*diff))/(width*height)
        if MSE == 0:
                return 0
        result = 10*np.log10(255*255/MSE)
        return result