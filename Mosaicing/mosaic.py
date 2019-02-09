import numpy as np 
from PIL import Image
from argparse import ArgumentParser
from utils.tools import get_config,get_w_h,save_imge
from utils.tools import averaging, one_color_fill_max, one_color_fill_random,nearest_neibour_sampling
# from utils.tools import *
import time
import os
parser=ArgumentParser()
parser.add_argument('--config',type=str,default='config.yaml',
                                help="config for mosaic details")

args = parser.parse_args()
config = get_config(args.config)

block_size = config['block']
mosaic_area = config['mosaic_area']
imge_path_root = config['image_path']
save_path_root = config['save_path']
region = config['region']
if os.path.exists('region.txt'):
        os.remove('region.txt')
for filename in os.listdir(imge_path_root):
        img=Image.open(imge_path_root+"/"+ filename).convert('RGB')
        width, height = img.size
        width_left,width_right,height_up,height_down = get_w_h(width,height,mosaic_area,region)
        img = np.array(img)
        ####---start processing---####
        for h in range(height_up,height_down,block_size):
                for w in range(width_left,width_right,block_size):
                        data = img[h:h+block_size,w:w+block_size]
                        if config['strategy'] == 'averaging':
                                r,g,b = data[:,:,0],data[:,:,1],data[:,:,2]
                                r = averaging(r)
                                g = averaging(g)
                                b = averaging(b)
                                data[:,:,0],data[:,:,1],data[:,:,2] = r,g,b
                                img[h:h+block_size,w:w+block_size] = data
                        elif config['strategy'] == 'one-color-fill-max':
                                r,g,b = data[:,:,0],data[:,:,1],data[:,:,2]
                                r = one_color_fill_max(r)
                                g = one_color_fill_max(g)
                                b = one_color_fill_max(b)
                                data[:,:,0],data[:,:,1],data[:,:,2] = r,g,b
                                img[h:h+block_size,w:w+block_size] = data
                        elif config['strategy'] == 'one-color-fill-random':
                                r,g,b = data[:,:,0],data[:,:,1],data[:,:,2]
                                r = one_color_fill_random(r)
                                g = one_color_fill_random(g)
                                b = one_color_fill_random(b)
                                data[:,:,0],data[:,:,1],data[:,:,2] = r,g,b
                                img[h:h+block_size,w:w+block_size] = data
                        elif config['strategy'] == 'nearest_neibour_sampling':
                                r,g,b = data[:,:,0],data[:,:,1],data[:,:,2]
                                r = nearest_neibour_sampling(r)
                                g = nearest_neibour_sampling(g)
                                b = nearest_neibour_sampling(b)
                                data[:,:,0],data[:,:,1],data[:,:,2] = r,g,b
                                img[h:h+block_size,w:w+block_size] = data
        #####---save the imge---####
        save_imge(img,save_path_root,filename,config['region'],width_left,height_up,mosaic_area,width_right)
        ## 如果width_right == 0 说明mosaic_area 超出了imge的大小
