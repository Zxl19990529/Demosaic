import yaml
import numpy as np 
from PIL import Image
import random
import os
def get_config(config):
    with open(config,'r') as stream:
        return yaml.load(stream) 

def list_all_files(rootdir):
    import os
    _files = []
    list = os.listdir(rootdir) #列出文件夹下所有的目录与文件
    for i in range(0,len(list)):
           path = os.path.join(rootdir,list[i])
           if os.path.isdir(path):
              _files.extend(list_all_files(path))
           if os.path.isfile(path):
              _files.append(path)
    return _files
    
###---strategy---###
def averaging(data):
        m = np.mean(data)
        return np.full(data.shape,m,int)

def one_color_fill_max(data):
        m = np.max(data)
        return np.full(data.shape,m,int)

def one_color_fill_random(data):
        tmp = np.reshape(data,(1,-1))
        tmp = np.squeeze(tmp)
        # print(tmp.shape)
        m = np.random.choice(tmp)
        return np.full(data.shape,m,int)

def nearest_neibour_sampling(data):
        m = data[0,0]
        return np.full(data.shape,m,int)

###---strategy---###

###---region---###
def get_w_h(width,height,mosaic_area,region):
        if region == 'center':
                if int(width/2-mosaic_area)<=0 or int(height/2-mosaic_area)<=0:
                        return 0,0,0,0
                width_left = int(width/2-mosaic_area)
                width_right = width_left+mosaic_area*2
                height_up = int(height/2-mosaic_area)
                height_down = height_up+mosaic_area*2 
                return width_left,width_right,height_up,height_down
        elif region == 'random':
                if width-mosaic_area*2<=0 or height-mosaic_area*2<=0:
                        return 0,0,0,0
                width_left = random.randint(0,int(width-mosaic_area*2))
                width_right = width_left+mosaic_area*2
                height_up = random.randint(0,int(height-mosaic_area*2))
                height_down = height_up+mosaic_area*2
                return width_left,width_right,height_up,height_down

def get_w_h_byrate(width,height,mosaic_area_rate,region):
        if region == 'center':
                width_left = int(width/2 - width*mosaic_area_rate)
                width_right = width_left + width*mosaic_area_rate*2
                height_up = int(height/2 - height*mosaic_area_rate )
                height_down = height_up + height*mosaic_area_rate*2
                return width_left,width_right,height_up,height_down
        elif region == 'random':
                width_left = random.randint(0,int(width-width*mosaic_area_rate*2))
                width_right = int(width_left + width*mosaic_area_rate*2)
                height_up = random.randint(0,int(height-height*mosaic_area_rate*2))
                height_down = int(height_up + height*mosaic_area_rate*2)
                return width_left,width_right,height_up,height_down


def save_imge(img,save_path_root,filename,region,width_left,height_up,mosaic_area,width_right):#如果width_right == 0 说明mosaic_area 超出了imge的大小
        img=Image.fromarray(img)
        if not os.path.exists(save_path_root):
                os.makedirs(save_path_root)
        save_path = os.path.join(save_path_root,filename)
        img.save(save_path)        
        if region == 'random' :
                if width_right == 0:
                        record = filename+' '+'Image Size ERROR '+'\n'
                else :
                        record = filename+' '+'width_left '+str(width_left)+' height_up '+str(height_up)+' mosaic_area '+str(mosaic_area)+' \n'
                save_path_root = save_path_root.split('/')
                folder_name = save_path_root[-1]
                save_path_root.pop()                
                save_path_root = '/'.join(save_path_root)
                print(save_path_root)
                # region.txt 文件放到与图片文件夹同级
                f=open(save_path_root+'/region_'+folder_name+'.txt','a')
                f.writelines(record)
                f.close()
                print(record)
        else:
                print(save_path)        

def save_iamge_byrate(img,save_path_root,filename,region,width_left,height_up,width_right,height_down):#如果width_right == 0 说明mosaic_area 超出了imge的大小
        img=Image.fromarray(img)
        if not os.path.exists(save_path_root):
                os.makedirs(save_path_root)
        save_path = os.path.join(save_path_root,filename)
        img.save(save_path)        
        if region == 'random' :
                if width_right == 0:
                        record = filename+' '+'Image Size ERROR '+'\n'
                else :
                        record = filename+' '+'width_left '+str(width_left)+' height_up '+str(height_up)+' width_right '+str(width_right)+' height_down '+str(height_down)+' \n'
                save_path_root = save_path_root.split('/')
                folder_name = save_path_root[-1]
                save_path_root.pop()                
                save_path_root = '/'.join(save_path_root)
                print(save_path_root)
                # region.txt 文件放到与图片文件夹同级
                f=open(save_path_root+'/region_'+folder_name+'.txt','a')
                f.writelines(record)
                f.close()
                print(record)
        else:
                print(save_path)        

###---region---###