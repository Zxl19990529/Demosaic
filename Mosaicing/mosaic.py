import numpy as np 
from PIL import Image
from argparse import ArgumentParser
from utils.tools import get_config,get_w_h,get_w_h_byrate,save_imge,list_all_files,save_iamge_byrate
from utils.tools import averaging, one_color_fill_max, one_color_fill_random,nearest_neibour_sampling
# from utils.tools import *
# import time
import os
import gc
parser=ArgumentParser()
parser.add_argument('--config',type=str,default='config.yaml',
                                help="config for mosaic details")

args = parser.parse_args()
config = get_config(args.config)

# block_size = config['block']
block_size_rate = config['block_rate_byshort']

mosaic_area = config['mosaic_area']
mosaic_area_rate = config['mosaic_area_rate']
# imge_path_root = config['image_path']
save_path_root = config['save_path']
region = config['region']


for line in open('record.txt','r'):
        line = line.replace(' \n','')
        filepath = line # ./Dataset/data_256/b/bamboo_forest/00000528.jpg
        spt = line.split('/')
        # print(spt)
        # ['.', 'Dataset', 'data_256', 'b', 'bamboo_forest', '00000528.jpg']
        spt[1] = save_path_root#['.', './nearset_neibour_sampling_Dataset', 'data_256', 'b', 'bamboo_forest', '00000528.jpg']
        filename = spt[-1]
        # print(filename)
        spt.pop(0)
        spt.pop()
        tmp ='/'
        tmp =tmp.join(spt)
        # ./nearset_neibour_sampling_Dataset/data_256/b/bamboo_forest
        save_image_root = tmp
        # print(save_image_root)
        # break

# for filename in os.listdir(imge_path_root):
        img = Image.open(filepath).convert('RGB')
        # img=Image.open(imge_path_root+"/"+ filename).convert('RGB')
        width, height = img.size
        # width_left,width_right,height_up,height_down = get_w_h(width,height,mosaic_area,region)
        width_left,width_right,height_up,height_down = get_w_h_byrate(width,height,mosaic_area_rate,region)
        block_size = int(min(width_right - width_left,height_down - height_up)*block_size_rate)
        if block_size == 0:
                block_size = 1
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
        # save_imge(img,save_image_root,filename,config['region'],width_left,height_up,mosaic_area,width_right)
        save_iamge_byrate(img,save_image_root,filename,config['region'],width_left,height_up,width_right,height_down)
        ## 如果width_right == 0 说明mosaic_area 超出了imge的大小
