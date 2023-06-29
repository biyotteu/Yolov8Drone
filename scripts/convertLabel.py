import cv2
import numpy as np
import argparse
import os
import json
from glob import glob
from tqdm import tqdm
import pandas as pd

#  visdrone annotation format 
#  <bbox_left>,<bbox_top>,<bbox_width>,<bbox_height>,<score>,<object_category>,<truncation>,<occlusion>

#  Yolo annotation format
#  <object-class> <x> <y> <width> <height>

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--path',type=str,default='')

    args = parser.parse_args()
    
    with open(args.path, 'r') as file:
        data = json.load(file)
        images = pd.DataFrame(data['images'])
        annotations = pd.DataFrame(data['annotations'])
        # print(images.shape[0])
        # print(len(glob("/home/ubuntu/dev/datasets/SeaDroneSee/train/labels/*.jpg")))
        for i,image in tqdm(images.iterrows()):
            img_height = image['height']
            img_width = image['width']
            anno = annotations[image['id'] == annotations['image_id']]
            with open('/home/ubuntu/dev/datasets/SeaDroneSee/val/labels/'+image['file_name'].replace(".jpg",".txt"),'w') as save:
                for j, a in anno.iterrows():
                    bbox = a['bbox']
                    width = bbox[2] / img_width
                    height = bbox[3] / img_height
                    x = (bbox[0] + bbox[2]/2) / img_width 
                    y = (bbox[1] + bbox[3]/2) / img_height
                    save.write('%d %f %f %f %f\n' % (a['category_id']-1,x,y,width,height))
                    # save.write('%d %d %d % %f  \n' % (a['category_id']-1,x,y,width,height))

    # print(data)