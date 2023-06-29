#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import json
import glob
from collections import defaultdict
from tqdm import tqdm
from PIL import Image
   
gt_dir = "/home/ubuntu/dev/datasets/DroneVSBirdOrigin/challenge/annotations/" #has to be adapted
out_dir = "/home/ubuntu/dev/datasets/DroneVSBirdOrigin/fit/labels/" 
def f(gt_list):
    img_cnt = 0
    for gt in tqdm(gt_list):
        if gt.endswith('.txt'):
            gt_file = os.path.join(gt_dir, gt)
                        
            with open(gt_file, 'r') as ann:
                line = ann.readline()  
                while line:
                    params = line.split(' ')
                    img_id = int(params[0])
                    obj_cnt = int(params[1])

                    file_name = gt[:-4] + "_%05d.jpg" % img_id

                    if not os.path.exists("/home/ubuntu/dev/datasets/DroneVSBirdOrigin/fit/images/"+file_name):
                        line = ann.readline()
                        continue

                    im = Image.open(os.path.join("/home/ubuntu/dev/datasets/DroneVSBirdOrigin/fit/images/"+file_name))
                    W, H = im.size
                    with open(os.path.join(out_dir,file_name.replace(".jpg",".txt")),'w') as save:
                        for idx in range(obj_cnt):
                            x = int(params[idx*5 + 2])
                            y = int(params[idx*5 + 3])
                            w = int(params[idx*5 + 4])
                            h = int(params[idx*5 + 5])
                            # cls = params[idx*5 +6]

                            if x + w/2 < 0 or y + h/2 < 0:
                                continue
                            
                            if x < 0:
                                w = x + w//2
                                x = 0
                            
                            if y < 0:
                                h = y + h//2
                                y = 0

                            x = (x+w/2) / W
                            y = (y+h/2) / H
                            w = w / W
                            h = h / H
                            save.write("%d %f %f %f %f\n"%(0,x,y,w,h))

                    line = ann.readline()
                            
                                     
            #save out json 
    # with open(out_dir, 'w') as outfile:
    #     json.dump(out_data, outfile)
            

   
if __name__ == '__main__':
    gt_list = os.listdir(gt_dir)

    f(gt_list)
