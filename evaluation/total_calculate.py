import re
import argparse
import os
parser = argparse.ArgumentParser()
parser.add_argument('--filename',type=str,help='PSNR.txt, part_PSNR.txt, SSIM.txt, part_SSIM.txt, LPIPS.txt')

arg = parser.parse_args()

count = 0
sum = 0

filename = arg.filename

if os.path.exists(filename):
    for line in open(filename):
        spt = re.split(' ',line)
        number = spt[2]
        sum += float(number)
        count +=1

print(sum/count)
