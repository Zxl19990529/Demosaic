# Before using
Make sure you have install anaconda, and create the environment with the following arg:
```sh
conda env create -f environment.yaml
```
## Evaluation

This folder contains python files for evaluating PSNR, part_PSNR, SSIM, part_SSIM of mosaiced_images and orginal_images.  
Here is the config.yaml :

```yml
#average mosaic paramters
block: 20
mosaic_area: 100
#region:center,random
region: 'random'
region_record: 'region.txt'
# image A and B,
imageA: './original_image'
imageB: './mosaiced_image'
# method: PSNR, part_PSNR, SSIM, part_SSIM, Perceptual_loss
method: 'PSNR'
```

### Usage

If the **region** is random:
 - make sure there is region.txt(created by Mosaicing)
 - python evaluate.py
If the **region** is center:
 - python evaluate.py

 ## Mosaicing

This folder contains python files for mosaicing, here I haver implemented four methods:*averaging, one-color-fill-max, one-color-fill-random, nearest_neibour_sampling*  
Here is the config.yaml: 
```yml
#average mosaic paramters
block: 20
mosaic_area: 100
#region:center,random
region: 'random'
image_path: './original_images'
save_path: './mosaiced_images'
#strategy: averaging, one-color-fill-max, one-color-fill-random, nearest_neibour_sampling
strategy: 'nearest_neibour_sampling'
```

### Usage
```sh
python mosaic.py
```
If you choose **region: random**, it will create a **region.txt** file, which records the region of the mosaic area. And**region.txt** will be used for evulation