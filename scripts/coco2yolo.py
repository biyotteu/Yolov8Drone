import json
import argparse
import pandas as pd
import os
from tqdm import tqdm

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--coco_path', type=str, help='path of coco annotation file')
    parser.add_argument('--save_path', type=str, help='path of save directory')
    
    opt = parser.parse_args()
		
		os.makedirs(opt.save_path, exist_ok=True)

    with open(opt.coco_path ,"r") as f:
        coco = json.load(f)
    
    images = pd.DataFrame(coco['images'])
    annotations = pd.DataFrame(coco['annotations'])

    for idx, image in tqdm(images.iterrows(),total=images.shape[0]):
        image_id = image['id']
        file_name = image['file_name']
        width = image['width']
        height = image['height']

        image_annotations = annotations[annotations['image_id'] == image_id]
        image_annotations = image_annotations.reset_index(drop=True)

        with open(os.path.join(opt.save_path, file_name.split('.')[0] + '.txt'), 'w') as f:
            for idx, annotation in image_annotations.iterrows():
                category_id = annotation['category_id']
                bbox = annotation['bbox']
                x_center = bbox[0] + bbox[2]/2
                y_center = bbox[1] + bbox[3]/2
                x_center /= width
                y_center /= height
                bbox_width = bbox[2] / width
                bbox_height = bbox[3] / height
                f.write(f'{category_id} {x_center} {y_center} {bbox_width} {bbox_height}\n')