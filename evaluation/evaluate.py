from PIL import Image
import numpy as np 
from utils.tools import get_config,get_center_area,get_random_filename_area
from utils.tools import PSNR,SSIM
import os 
import time
import re
config='./config.yaml'
config=get_config(config)

block_size = config['block']
mosaic_area = config['mosaic_area']
region = config['region']
original_image_path = config['imageA']
processed_image_path = config['imageB']
record_region_path = config['region_record']


if config['method'] == 'PSNR':
    if os.path.exists('PSNR.txt'):
        os.remove('PSNR.txt')
    for filename in os.listdir(original_image_path):# 遍历两个文件
        original_image = original_image_path + '/' + filename
        processed_image = processed_image_path + '/' + 'mosaiced_' + filename
        original_image = Image.open(original_image).convert('RGB')
        processed_image = Image.open(processed_image).convert('RGB')
        width, height = original_image.size 
        original_image = np.array(original_image)
        processed_image = np.array(processed_image)

        psnr = PSNR(original_image,processed_image)

        record = original_image_path + '/' + filename + ' PSNR '+str(psnr)+' \n'        
        f = open('PSNR.txt','a')
        f.writelines(record)
        f.close()
        print(record)
elif config['method'] == 'part_PSNR':
    if os.path.exists('part_PSNR.txt'):
        os.remove('part_PSNR.txt')
    if region == 'center':
        for filename in os.listdir(original_image_path):# 遍历两个文件
            original_image = original_image_path + '/' + filename
            processed_image = processed_image_path + '/' + 'mosaiced_' + filename
            original_image = Image.open(original_image).convert('RGB')
            processed_image = Image.open(processed_image).convert('RGB')
            width, height = original_image.size 
            original_image = np.array(original_image)
            processed_image = np.array(processed_image)     
            area = get_center_area(width,height,mosaic_area)
            original_image = original_image[area['height_up']:area['height_down'],area['width_left']:area['width_right']]
            processed_image = processed_image[area['height_up']:area['height_down'],area['width_left']:area['width_right']]

            part_psnr = PSNR(original_image,processed_image)
            
            record = original_image_path + '/' + filename + ' part_PSNR '+str(part_psnr)+' \n'
            f = open('part_PSNR.txt','a')
            f.writelines(record)
            f.close()
            print(record)
    if region == 'random':
        for line in open('region.txt'):
            original_image,processed_image, area = get_random_filename_area(line)
            original_image = original_image_path + '/' + original_image
            processed_image = processed_image_path + '/' + processed_image
            record = original_image + ' part_PSNR '
            original_image = np.array(Image.open(original_image).convert('RGB'))
            processed_image = np.array(Image.open(processed_image).convert('RGB'))
            original_image = original_image[area['height_up']:area['height_down'],area['width_left']:area['width_right']]
            processed_image = processed_image[area['height_up']:area['height_down'],area['width_left']:area['width_right']]

            part_psnr = PSNR(original_image,processed_image)
            
            record = record +str(part_psnr)+' \n'
            f = open('part_PSNR.txt','a')
            f.writelines(record)
            f.close()
            print(record)

elif config['method'] == 'SSIM':
    if os.path.exists('SSIM.txt'):
        os.remove('SSIM.txt')
    for filename in os.listdir(original_image_path):# 遍历两个文件
        original_image = original_image_path + '/' + filename
        processed_image = processed_image_path + '/' + 'mosaiced_' + filename
        original_image = Image.open(original_image).convert('RGB')
        processed_image = Image.open(processed_image).convert('RGB')
        width, height = original_image.size 
        original_image = np.array(original_image)
        processed_image = np.array(processed_image)
        
        ssim = SSIM(original_image,processed_image)

        record = original_image_path + '/' + filename + ' SSIM '+str(ssim)+' \n'        
        f = open('SSIM.txt','a')
        f.writelines(record)
        f.close()
        print(record)

elif config['method'] == 'part_SSIM':
    if os.path.exists('part_SSIM.txt'):
        os.remove('part_SSIM.txt')
    if region == 'center':
        for filename in os.listdir(original_image_path):# 遍历两个文件
            original_image = original_image_path + '/' + filename
            processed_image = processed_image_path + '/' + 'mosaiced_' + filename
            original_image = Image.open(original_image).convert('RGB')
            processed_image = Image.open(processed_image).convert('RGB')
            width, height = original_image.size 
            original_image = np.array(original_image)
            processed_image = np.array(processed_image)     
            area = get_center_area(width,height,mosaic_area)
            original_image = original_image[area['height_up']:area['height_down'],area['width_left']:area['width_right']]
            processed_image = processed_image[area['height_up']:area['height_down'],area['width_left']:area['width_right']]

            part_ssim = SSIM(original_image,processed_image)
            
            record = original_image_path + '/' + filename + ' part_SSIM '+str(part_ssim)+' \n'
            f = open('part_SSIM.txt','a')
            f.writelines(record)
            f.close()
            print(record)
    if region == 'random':
        for line in open('region.txt'):
            original_image,processed_image, area = get_random_filename_area(line)
            original_image = original_image_path + '/' + original_image
            processed_image = processed_image_path + '/' + processed_image
            record = original_image + ' part_SSIM '
            original_image = np.array(Image.open(original_image).convert('RGB'))
            processed_image = np.array(Image.open(processed_image).convert('RGB'))
            original_image = original_image[area['height_up']:area['height_down'],area['width_left']:area['width_right']]
            processed_image = processed_image[area['height_up']:area['height_down'],area['width_left']:area['width_right']]

            part_ssim = PSNR(original_image,processed_image)
            
            record = record +str(part_ssim)+' \n'
            f = open('part_SSIM.txt','a')
            f.writelines(record)
            f.close()
            print(record)
elif config['method'] == 'LPIPS':
    from models import dist_model as dm
    from utils import util
    model = dm.DistModel()
    model.initialize(model='net-lin',net='alex',use_gpu=True)

    for filename in os.listdir(original_image_path):# 遍历两个文件
        original_image = original_image_path + '/' + filename
        processed_image = processed_image_path + '/' + 'mosaiced_' + filename
        record = original_image + ' LPIPS '
        original_image = util.im2tensor(util.load_image(original_image)) # RGB image from [-1,1]
        processed_image = util.im2tensor(util.load_image(processed_image))

        perceptual_loss = model.forward(original_image,processed_image)

        record += str(perceptual_loss[0])+' \n'
        f = open('LPIPS.txt','a')
        f.writelines(record)
        print(record)
        