import cv2
import numpy as np
import argparse
import os
from glob import glob
from tqdm import tqdm

#  visdrone annotation format 
#  <bbox_left>,<bbox_top>,<bbox_width>,<bbox_height>,<score>,<object_category>,<truncation>,<occlusion>

#  Yolo annotation format
#  <object-class> <x> <y> <width> <height>

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--path',type=str,default='')
    parser.add_argument('--save',type=str,default='')
    args = parser.parse_args()

    anotation_paths = glob(os.path.join(args.path,'annotations/*.txt'))
    # image_paths = glob(os.path.join(args.path,'images/*.jpg'))

    # anotation_paths = anotation_paths[:5]

    for path in tqdm(anotation_paths):
        filename = path.split('/')[-1].split('.')[0]

        with open(path) as anno:
            bboxs = anno.readlines()
            
        # img = cv2.imread(os.path.join(args.path,os.path.join('images',filename+'.jpg')),cv2.IMREAD_COLOR)
        
        new_bboxs = ['' for i in range(len(bboxs))]
        for i in range(len(bboxs)):
            bbox = bboxs[i].replace("\n","")
            if bbox[-1] == ',':
                bbox = bbox[:-1]
            bbox = bbox.split(',')
            try:
                bbox = list(map(int,bbox))
            except:
                print(filename,bboxs[i])
            
            bbox = list(map(int,bbox))
            new_bboxs[i] = '%d %d %d %d %d\n' % (bbox[5],bbox[0]+bbox[2]//2,bbox[1]+bbox[3]//2,bbox[2],bbox[3])
        
            # img = cv2.rectangle(img,(bbox[0],bbox[1]),(bbox[0]+bbox[2],bbox[1]+bbox[3]),(0,255,0),3)

        with open(os.path.join(args.save,filename+'.txt'),'w') as save:
            save.writelines(new_bboxs)
        
        # cv2.imwrite('./images/'+filename+'.jpg',img)