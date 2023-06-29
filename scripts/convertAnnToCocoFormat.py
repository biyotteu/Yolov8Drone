#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import json
import glob
from collections import defaultdict
from tqdm import tqdm
from PIL import Image
   
def f(gt_list,out_dir):
    gt_dir = "/home/ubuntu/dev/datasets/DroneVSBirdOrigin/challenge/annotations/" #has to be adapted
    ann_cnt = 0
    img_cnt = 0
    out_data = {'categories': [dict(id=0, name='drone')],'images': [],'annotations': []}
    for gt in tqdm(gt_list):
        if gt.endswith('.txt'):
            gt_file = os.path.join(gt_dir, gt)
                        
            with open(gt_file, 'r') as ann:
                line = ann.readline()  
                while line:
                    params = line.split(' ')
                    img_id = int(params[0])
                    obj_cnt = int(params[1])

                    img_info = dict()
                    img_info['file_name'] = gt[:-4] + "_%05d.jpg" % img_id

                    if not os.path.exists("/home/ubuntu/dev/datasets/DroneVSBirdOrigin/challenge/images/"+img_info['file_name'] ):
                        line = ann.readline()
                        continue

                    im = Image.open(os.path.join("/home/ubuntu/dev/datasets/DroneVSBirdOrigin/challenge/images/"+img_info['file_name']))
                    W, H = im.size
                    img_info['id'] = img_cnt
                    img_info['width'] = W
                    img_info['height'] = H
                    out_data['images'].append(img_info)

                    for idx in range(obj_cnt):
                        x_left = int(params[idx*5 + 2])
                        y_top = int(params[idx*5 + 3])
                        w = int(params[idx*5 + 4])
                        h = int(params[idx*5 + 5])
                        cls = params[idx*5 +6]

                        if x_left + w/2 < 0 or y_top + h/2 < 0:
                            continue
                        
                        if x_left < 0:
                            w = x_left + w//2
                            x_left = 0
                        
                        if y_top < 0:
                            h = y_top + h//2
                            y_top = 0

                        ann_info = dict()
                        ann_info['id'] = ann_cnt
                        ann_info['iscrowd'] = 0
                        ann_info['image_id'] = img_cnt

                        ann_info['bbox'] = [x_left, y_top, w, h]
                        ann_info['area'] = w*h
                        ann_info['category_id'] = 0
                        out_data['annotations'].append(ann_info)
                
                        ann_cnt += 1
                    img_cnt += 1
                    line = ann.readline()
                            
                                     
            #save out json 
    with open(out_dir, 'w') as outfile:
        json.dump(out_data, outfile)
            
    print(img_cnt)

   
if __name__ == '__main__':
    gt_dir = "/home/ubuntu/dev/datasets/DroneVSBirdOrigin/challenge/annotations/" 
    gt_list = os.listdir(gt_dir)

    out_dir = "/home/ubuntu/dev/datasets/DroneVSBirdOrigin/challenge/coco_annotations/" 
    # f(gt_list[:65],out_dir+'train.json')
    f(gt_list[-5:],out_dir+'val.json')
    f(gt_list,out_dir+'train.json')
